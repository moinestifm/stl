import json, subprocess, time, os
from flask import Flask, render_template, request, redirect, url_for, flash
from functools import wraps

CONFIG_FILE = "config.json"
LIQ_TEMPLATE = "liquidsoap.liq.template"
LIQ_FILE = "liquidsoap.liq"

app = Flask(__name__)
app.secret_key = "supersecuresecretkey"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def generate_liq(config):
    with open(LIQ_TEMPLATE) as f:
        template = f.read()
    content = template.replace("{{MAIN_STREAM}}", config["main_stream"]) \
                      .replace("{{BACKUP_STREAM}}", config["backup_stream"]) \
                      .replace("{{ADMIN_PASSWORD}}", config["admin_password"])
    with open(LIQ_FILE, "w") as f:
        f.write(content)

def restart_liquidsoap():
    subprocess.call(["pkill", "-f", "liquidsoap.liq"])
    time.sleep(1)
    subprocess.Popen(["liquidsoap", LIQ_FILE])

# HTTP Basic Auth
def check_auth(username, password):
    return username == os.environ.get("ADMIN_USER", "admin") and password == os.environ.get("ADMIN_PASS", "changeme")

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return ("Could not verify your access level for that URL.\n"
                    "You have to login with proper credentials", 401,
                    {"WWW-Authenticate": 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET", "POST"])
@requires_auth
def index():
    config = load_config()
    if request.method == "POST":
        config["admin_password"] = request.form["admin_password"]
        config["main_stream"] = request.form["main_stream"]
        config["backup_stream"] = request.form["backup_stream"]
        save_config(config)
        generate_liq(config)
        restart_liquidsoap()
        flash("Configuration updated and Liquidsoap restarted!")
        return redirect(url_for("index"))

    # Load logs
    log_path = "/app/static/silence.log"
    log_content = ""
    if os.path.exists(log_path):
        with open(log_path) as f:
            log_content = "".join(f.readlines()[-100:])  # last 100 lines

    # VU levels
    vu_path = "/app/static/vu.json"
    vu_levels = {"left": 0, "right": 0}
    if os.path.exists(vu_path):
        with open(vu_path) as f:
            vu_levels = json.load(f)

    # Stream status (dummy logic, could ping streams)
    main_active = "active"
    backup_active = "inactive"
    stream_status = "online"

    return render_template("index.html",
                           config=config,
                           log_content=log_content,
                           vu_levels=vu_levels,
                           main_active=main_active,
                           backup_active=backup_active,
                           stream_status=stream_status)

if __name__ == "__main__":
    config = load_config()
    generate_liq(config)
    restart_liquidsoap()
    app.run(host="0.0.0.0", port=5000)
