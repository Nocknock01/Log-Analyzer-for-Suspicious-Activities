Log Analyzer for Suspicious Activities

Parse authentication & firewall logs and detect suspicious activity (brute-force attempts, repeated failures).
Python + Flask web dashboard that parses log files in data/, applies simple detection rules, and displays results in a browser.

Features

Parse simple timestamp user=... ip=... status=... log lines

Detect brute force style attacks (N failures within a short time window)

Web dashboard: totals, suspicious events, full event table

Easy to extend: add IP blacklist, geo IP, exports, charts

Repository layout

Log-Analyzer-for-Suspicious-Activities/
│ app.py                 # Flask app entrypoint
│ requirements.txt
│ README.md
│ .gitignore
│
├─ log_analyzer/
│   ├─ __init__.py
│   ├─ parser.py         # log parsing helpers
│   └─ rules.py          # detection rules
│
├─ data/
│   └─ sample_auth.example.log   # example/safe sample log (kept in repo)
│
├─ templates/
│   ├─ base.html
│   └─ dashboard.html
│
└─ static/
    └─ style.css


Note: Keep real/production logs out of git. The sample file uses .example.log so you can commit a template while still ignoring real logs.

Log format (example)

The default parser expects lines like:

2025-12-08 10:00:01 user=alice ip=192.168.1.10 status=FAILED
2025-12-08 10:05:00 user=alice ip=192.168.1.10 status=SUCCESS


Required fields (or parser fallbacks):

timestamp as YYYY-MM-DD HH:MM:SS

user=<username>

ip=<ip-address>

status=<FAILED|SUCCESS|...>

If your logs use a different format, paste 3–5 sample lines and update log_analyzer/parser.py (quick to adapt).

Quick start (Windows PowerShell)

Open PowerShell, then run the commands below from the project root.

Create & activate a virtual environment

python -m venv .venv
.venv\Scripts\Activate.ps1


Install dependencies

pip install -r requirements.txt


(Optional) If you want a sample log in data/:

if (!(Test-Path -Path .\data)) { New-Item -ItemType Directory -Path .\data | Out-Null }
Set-Content -Path .\data\sample_auth.example.log -Value @"
2025-12-08 10:00:01 user=alice ip=192.168.1.10 status=FAILED
2025-12-08 10:00:10 user=alice ip=192.168.1.10 status=FAILED
2025-12-08 10:05:00 user=alice ip=192.168.1.10 status=SUCCESS
"@ -Encoding UTF8


Run the app

python app.py


Open your browser:

http://127.0.0.1:5000


In the dashboard input Log file path, type:

data/sample_auth.example.log


(or data/your_real_log.log if you placed your file there)

Quick start (Linux / macOS)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# browse http://127.0.0.1:5000

Run with a custom log file

Copy your log into the data/ folder (example: data/mylog.log).

In the dashboard enter:

data/mylog.log


Click Reload.

Common troubleshooting

OSError: Invalid argument — make sure you enter only the relative path (e.g. data/sample_auth.example.log) in the dashboard input. Don’t prefix with Log file path: or supply absolute Windows paths.

FileNotFoundError — verify data/yourfile.log exists and spelling is correct.

ModuleNotFoundError — ensure pip install -r requirements.txt ran in the same Python environment (activate .venv before install).

If the page shows empty fields: check data/ file encoding (UTF-8) and line format.

How detection works (simple overview)

log_analyzer/parser.py — turns each log line into a dict: {timestamp, user, ip, status}

log_analyzer/rules.py — detect_bruteforce() counts FAILED attempts per IP in a sliding time window (configurable)

The Flask app calls the parser + rules and renders templates/dashboard.html

You can tune:

window size (minutes)

failure threshold

add other rules (IP blacklist, thresholds per user, geo checks)

Recommended improvements / next steps

Add charting (failed attempts over time) using a JS chart library (Chart.js)

GeoIP lookups (MaxMind or IPstack) to flag foreign IPs

Export suspicious events to CSV

Add authentication to the dashboard (Flask-Login) if hosting publicly

Harden file handling if accepting arbitrary paths

Git & deployment tips

Add .venv/ to .gitignore (do not commit virtual env)

Keep sample logs as *.example.log and have data/*.log ignored

To push to GitHub:

git add .
git commit -m "chore: add log analyzer"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main


For remote hosting: use a WSGI server (Gunicorn / uWSGI) behind nginx. Secure the web UI before exposing to the public.

Contributing

Fork the repo

Create a feature branch: git checkout -b feat/geoip

Commit and push, open a Pull Request

Describe changes & add tests where applicable

License

Add a license of your choice (e.g., MIT). Example: create a LICENSE file with the MIT text.

