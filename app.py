from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os

current_dir = os.path.expanduser("~")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# TERMINAL

@app.route("/terminal", methods=["POST"])
def terminal():

    global current_directory

    command = request.json["command"]

    # Handle cd separately
    if command.startswith("cd "):
        new_path = os.path.abspath(
            os.path.join(current_directory, command[3:])
        )

        if os.path.isdir(new_path):
            current_directory = new_path
            return jsonify({"output": current_directory})

        return jsonify({"error": "Directory doesn't exist."})

    result = subprocess.run(
        command,
        cwd=current_directory,
        shell=True,
        capture_output=True,
        text=True
    )

    return jsonify({
        "output": result.stdout,
        "error": result.stderr
    })

# REBOOT

@app.route("/reboot", methods=["POST"])
def reboot():

    def reboot_pi():
        os.system("sudo reboot")

    threading.Thread(target=reboot_pi).start()

    return jsonify({
        "status":"Rebooting..."
    })


# REMOTE DESKTOP

@app.route("/desktop")
def desktop():

    return """
    <h2>Remote Desktop</h2>

    Connect using RealVNC Viewer

    Address:

    192.168.1.79
    """

@app.route("/refresh", methods=["POST"])
def refresh():

    def update():

        subprocess.run(
            ["git", "pull"],
            cwd="/home/pi/raspberry_dashboard"
        )

        subprocess.run([
            "sudo",
            "systemctl",
            "restart",
            "pi-dashboard"
        ])

    threading.Thread(target=update).start()

    return jsonify({
        "status": "Updating..."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)