import os
import subprocess
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
processes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.py'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
    return redirect(url_for('manage'))

@app.route('/manage')
def manage():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('manage.html', files=files, processes=processes)

@app.route('/run/<filename>')
def run_script(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if filename in processes:
        return redirect(url_for('manage'))
    proc = subprocess.Popen(['python3', path])
    processes[filename] = proc
    return redirect(url_for('manage'))

@app.route('/stop/<filename>')
def stop_script(filename):
    proc = processes.get(filename)
    if proc:
        proc.terminate()
        processes.pop(filename)
    return redirect(url_for('manage'))

@app.route('/delete/<filename>')
def delete_script(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if filename in processes:
        processes[filename].terminate()
        processes.pop(filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('manage'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
