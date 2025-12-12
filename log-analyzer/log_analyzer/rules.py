from collections import defaultdict
from datetime import timedelta

def detect_bruteforce(events, window_minutes=5, threshold=5):
    """
    Very simple brute-force logic:
    - count FAILED attempts per IP in a rolling window
    - if count >= threshold -> mark as brute-force
    """
    events_sorted = sorted(events, key=lambda e: e["timestamp"])
    suspicious = set()
    by_ip = defaultdict(list)

    for idx, ev in enumerate(events_sorted):
        ip = ev["ip"]
        if ev["status"].upper() != "FAILED":
            continue

        by_ip[ip].append(ev)

        # Slide window
        window_start_time = ev["timestamp"] - timedelta(minutes=window_minutes)
        recent = [e for e in by_ip[ip] if e["timestamp"] >= window_start_time]
        by_ip[ip] = recent

        if len(recent) >= threshold:
            for r in recent:
                suspicious.add(id(r))  # use object id as identifier

    return [e for e in events_sorted if id(e) in suspicious]


def flag_suspicious(events):
    """
    High-level function:
    - brute-force
    - you can add more rules later (IP blacklist, geo, etc.)
    """
    brute_force_events = detect_bruteforce(events)

    # You can add more rule sets and merge them
    suspicious_events = list({id(e): e for e in brute_force_events}.values())
    return suspicious_events
