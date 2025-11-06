#!/usr/bin/env python3
from flask import Flask, jsonify, request
import subprocess, os, sys, time

app = Flask(__name__)

# minimal auth token to avoid accidental exposure - override via env CONTROL_TOKEN
CONTROL_TOKEN = os.environ.get("CONTROL_TOKEN", "change_me_token")
LIQUIDSOAP_CONF = "/opt/deva/liquidsoap/tx.liq"

def check_token(req):
    token = req.headers.get("X-Control-Token", "")
    return token == CONTROL_TOKEN

@app.route("/control/restart", methods=["POST"])
def restart():
    if not check_token(request):
        return jsonify({"error":"unauthorized"}), 401
    # run supervisorctl restart
    try:
        subprocess.check_call(["supervisorctl", "restart", "liquidsoap"])
    except subprocess.CalledProcessError as e:
        return jsonify({"error":"failed", "detail":str(e)}), 500
    return jsonify({"ok":True})

@app.route("/control/status", methods=["GET"])
def status():
    if not check_token(request):
        return jsonify({"error":"unauthorized"}), 401
    out = subprocess.check_output(["supervisorctl", "status", "liquidsoap"]).decode()
    return jsonify({"status": out})

@app.route("/control/readconf", methods=["GET"])
def readconf():
    if not check_token(request):
        return jsonify({"error":"unauthorized"}), 401
    if not os.path.exists(LIQUIDSOAP_CONF):
        return jsonify({"error":"missing_config"}), 404
    with open(LIQUIDSOAP_CONF, "r") as fh:
        return jsonify({"config": fh.read()})

@app.route("/control/writeconf", methods=["POST"])
def writeconf():
    if not check_token(request):
        return jsonify({"error":"unauthorized"}), 401
    data = request.json or {}
    content = data.get("content")
    if content is None:
        return jsonify({"error":"missing_content"}), 400
    with open(LIQUIDSOAP_CONF, "w") as fh:
        fh.write(content)
    # restart liquidsoap after write
    try:
        subprocess.check_call(["supervisorctl", "restart", "liquidsoap"])
    except subprocess.CalledProcessError as e:
        return jsonify({"error":"failed_restart", "detail":str(e)}), 500
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
