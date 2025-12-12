if request.method == "POST":
    log_path = request.form.get("log_path", LOG_PATH) or LOG_PATH
    log_path = log_path.strip()

    # If user accidentally types "Log file path: data/sample_auth.log"
    if log_path.lower().startswith("log file path"):
        parts = log_path.split(":", 1)
        if len(parts) == 2:
            log_path = parts[1].strip()