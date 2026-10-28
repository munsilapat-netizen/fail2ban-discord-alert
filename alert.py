#!/usr/bin/env python3
# บอทแจ้งเตือน: เฝ้า Fail2ban แล้วส่ง alert เข้า Discord
import subprocess, json, os, urllib.request
from config import WEBHOOK_URL

SEEN_FILE = "seen_ips.txt"

def get_banned_ips():
    out = subprocess.run(
        ["sudo", "fail2ban-client", "status", "sshd"],
        capture_output=True, text=True).stdout
    for line in out.splitlines():
        if "Banned IP list:" in line:
            return line.split(":")[1].split()
    return []

def load_seen():
    if os.path.exists(SEEN_FILE):
        return set(open(SEEN_FILE).read().split())
    return set()

def send_discord(ip):
    msg = {"content": f"🚨 SSH brute-force detected! Banned IP: {ip}"}
    data = json.dumps(msg).encode()
    req = urllib.request.Request(WEBHOOK_URL, data=data,
    headers={"Content-Type": "application/json", "User-Agent": "fail2ban-alert-bot"})
    urllib.request.urlopen(req)

def main():
    seen = load_seen()
    banned = get_banned_ips()
    for ip in banned:
        if ip not in seen:
            send_discord(ip)
            seen.add(ip)
            print(f"Alerted: {ip}")
    open(SEEN_FILE, "w").write("\n".join(seen))

if __name__ == "__main__":
    main()
