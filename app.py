from flask import Flask, render_template, request
from log_analyzer.parser import load_log_file
from log_analyzer.rules import flag_suspicious

app = Flask(__name__)

LOG_PATH = "data/sample_auth.log"

@app.route("/", methods=["GET", "POST"])
def dashboard():
    log_path = LOG_PATH

    if request.method == "POST":
        log_path = request.form.get("log_path", LOG_PATH) or LOG_PATH
        log_path = log_path.strip()
        # If user accidentally typed "Log file path: data/...", clean it
        if log_path.lower().startswith("log file path"):
            parts = log_path.split(":", 1)
            if len(parts) == 2:
                log_path = parts[1].strip()

    try:
        events = load_log_file(log_path)
    except FileNotFoundError:
        return render_template(
            "dashboard.html",
            events=[],
            suspicious=[],
            stats={
                "total_events": 0,
                "total_suspicious": 0,
                "log_path": log_path,
            },
            error=f"Log file not found: {log_path}",
        )

    suspicious = flag_suspicious(events)

    stats = {
        "total_events": len(events),
        "total_suspicious": len(suspicious),
        "log_path": log_path,
    }

    return render_template(
        "dashboard.html",
        events=events,
        suspicious=suspicious,
        stats=stats,
        error=None,
    )

if __name__ == "__main__":
    app.run(debug=True)
