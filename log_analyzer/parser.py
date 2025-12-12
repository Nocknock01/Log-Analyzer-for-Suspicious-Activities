from datetime import datetime

def parse_log_line(line: str):
    """
    Parse a single log line into a dict.
    Adjust this to match your real log format.
    """
    line = line.strip()
    if not line:
        return None

    try:
        # Split timestamp and key=value part
        ts_str, rest = line.split(" ", 1)
        # If time also present like "2025-12-08 12:00:01 ..."
        if ":" in rest.split()[0]:
            ts_str2, rest = rest.split(" ", 1)
            ts_str = ts_str + " " + ts_str2

        timestamp = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # If format doesn't match, skip
        return None

    fields = {}
    for part in rest.split():
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip()] = value.strip()

    record = {
        "timestamp": timestamp,
        "user": fields.get("user", "-"),
        "ip": fields.get("ip", "-"),
        "status": fields.get("status", "-"),
        "raw": line,
    }
    return record


def load_log_file(path: str):
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = parse_log_line(line)
            if rec:
                events.append(rec)
    return events
