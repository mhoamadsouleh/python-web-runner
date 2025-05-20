from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
import signal

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# لتخزين العمليات النشطة
running_processes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لا يوجد ملف"
    file = request.files['file']
    if file.filename == '':
        return "لم يتم اختيار أي ملف"
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return redirect(url_for('list_files'))

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

@app.route('/run/<filename>', methods=['POST'])
def run_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if filename not in running_processes:
        process = subprocess.Popen(['python3', filepath])
        running_processes[filename] = process
    return redirect(url_for('list_files'))

@app.route('/stop/<filename>', methods=['POST'])
def stop_file(filename):
    process = running_processes.get(filename)
    if process:
        os.kill(process.pid, signal.SIGTERM)
        del running_processes[filename]
    return redirect(url_for('list_files'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if filename in running_processes:
        stop_file(filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(debug=True)
