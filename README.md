# Fail2ban Discord Alert Bot

A Python bot that watches Fail2ban and sends a real-time **Discord alert** whenever an IP is banned for an SSH brute-force attempt. Built as a follow-up to my [SSH brute-force detection lab](https://github.com/munsilapat-netizen/ssh-bruteforce-detection-lab) to add **automated alerting** — the way a real SOC gets notified instead of checking logs by hand.

<img width="1308" height="1380" alt="discord-alert" src="https://github.com/user-attachments/assets/2b28b3cb-d2ce-431a-b953-92ad8857ec86" />
<img width="1260" height="1278" alt="alert-code" src="https://github.com/user-attachments/assets/4ec5213b-cb24-40ed-b315-680edaf5e900" />
<img width="1120" height="490" alt="service-config" src="https://github.com/user-attachments/assets/203ddecb-42e0-4d6a-b7ff-0e331342b2d6" />
<img width="2010" height="591" alt="bot-run-timer" src="https://github.com/user-attachments/assets/7f85d89d-68ff-41de-beca-e446705436ff" />
<img width="920" height="430" alt="timer-config" src="https://github.com/user-attachments/assets/e64938cd-6d7e-4fa0-a26a-f39a93d013e5" />


---

##  Overview

In my first lab I had to run `fail2ban-client status` manually to see who got banned. This project automates that: a small Python script queries Fail2ban, detects newly banned IPs, and pushes an alert to a Discord channel through a webhook — running automatically every minute via a systemd timer.

## Objective

Get notified in real time, on my phone, the moment the defense blocks an attacker — without watching logs.

## ⚙️ How it works

```
Every 1 minute (systemd timer):
  1. Ask Fail2ban which IPs are currently banned
  2. Compare against IPs already alerted (stored in a file)
  3. If a new IP appears -> send a Discord alert
  4. Remember it so the same IP is not alerted twice
```

##  Tools Used

| Tool | Role |
|------|------|
| Python 3 | The bot (standard library only — no pip installs) |
| Fail2ban | Source of banned-IP data |
| Discord Webhook | Alert destination |
| systemd timer | Runs the bot automatically every minute |
| Git / GitHub | Version control, pushed via command line |

##  built

### The bot (`alert.py`)
Reads `fail2ban-client status sshd`, parses the banned IP list, and sends any new IP to Discord using `urllib` (no external dependencies). State is kept in `seen_ips.txt` to avoid duplicate alerts.

### Automation (systemd)
A `.service` + `.timer` pair runs the bot every minute, so alerting is fully hands-off.

### Secret management
The Discord webhook URL is kept in `config.py`, which is **excluded from Git** via `.gitignore`. A `config.example.py` shows the expected format without exposing the real secret. `__pycache__/` is also ignored — a compiled `.pyc` of the config can leak the secret too.

##  Result

- Bot sends a working Discord alert when an IP is banned.
- Runs automatically every minute via systemd.
- No secrets committed to the repository.

> Example alert: ` SSH brute-force detected! Banned IP: 203.0.113.99`

##  learned

- Writing a practical Python script that shells out to a system tool and parses its output.
- Calling a REST webhook from Python with `urllib` — and that Discord **rejects requests without a `User-Agent` header** (fixed a `403 Forbidden`).
- Running a task on a schedule with a **systemd service + timer**.
- Keeping secrets out of version control with `.gitignore` (including `__pycache__/`).
- Using Git from the command line: `init`, `add`, `commit`, `remote`, `push`, and authenticating with a **Personal Access Token**.
- A real operational gotcha: Fail2ban banned my own admin IP and locked me out of SSH — fixed by adding an `ignoreip` whitelist.

##  Setup

```bash
git clone https://github.com/munsilapat-netizen/fail2ban-discord-alert.git
cd fail2ban-discord-alert
cp config.example.py config.py      # then put your real webhook URL in config.py
python3 alert.py                    # test once
```
To run automatically, install the systemd `.service` and `.timer` (see the lab write-up).


##  Disclaimer

Built and tested only against my own isolated lab VM. Never target systems you do not own or have permission to test.

---

*Author: [munsilapat-netizen](https://github.com/munsilapat-netizen)*
