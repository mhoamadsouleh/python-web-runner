
from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
running_processes = {}

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        if f and f.filename.endswith(".py"):
            file_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(file_path)
            return redirect(url_for("manage_files"))
    return render_template("index.html")

@app.route("/files")
def manage_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("files.html", files=files, running=running_processes)

@app.route("/run/<filename>")
def run_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if filename in running_processes and running_processes[filename].poll() is None:
        return redirect(url_for("manage_files"))
    process = subprocess.Popen(["python3", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    running_processes[filename] = process
    return redirect(url_for("manage_files"))

@app.route("/stop/<filename>")
def stop_file(filename):
    process = running_processes.get(filename)
    if process and process.poll() is None:
        process.terminate()
    return redirect(url_for("manage_files"))

@app.route("/delete/<filename>")
def delete_file(filename):
    stop_file(filename)
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    running_processes.pop(filename, None)
    return redirect(url_for("manage_files"))

if __name__ == "__main__":
    app.run(debug=True)
