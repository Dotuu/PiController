from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# TERMINAL

@app.route("/terminal", methods=["POST"])
def terminal():

    command = request.json["command"]

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })

    except Exception as e:
        return jsonify({
            "output": "",
            "error": str(e)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)