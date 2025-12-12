# Log Analyzer for Suspicious Activities

Parsed authentication and firewall logs to detect brute-force attempts and anomalies.  
Identified 50+ malicious login attempts in test datasets.

## Tech Stack

- Python (Flask)
- HTML + CSS dashboard

## Features

- Load log files from `data/`
- Parse login events (timestamp, user, IP, status)
- Detect brute-force login attempts within a time window
- Web dashboard with:
  - Total events
  - Total suspicious events
  - Table view of all & suspicious events

## How to Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
