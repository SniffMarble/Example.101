#!/bin/bash
LOGFILE="$HOME/system_analysis_$(date +%Y%m%d_%H%M%S).log"

echo "🔍 System Analysis Report - $(date)" | tee "$LOGFILE"
echo "===============================" | tee -a "$LOGFILE"

echo -e "\n🛠️ Failed Systemd Services:\n" | tee -a "$LOGFILE"
systemctl --failed | tee -a "$LOGFILE"

echo -e "\n🚨 Kernel & Boot Messages (Errors/Warnings from dmesg):\n" | tee -a "$LOGFILE"
dmesg --color=never | grep -iE "error|warn|fail" | tee -a "$LOGFILE"

echo -e "\n📋 Journalctl - Errors from system logs:\n" | tee -a "$LOGFILE"
journalctl -p 3 -xb | tee -a "$LOGFILE"

echo -e "\n📂 File System Check (root):\n" | tee -a "$LOGFILE"
sudo fsck -n / | tee -a "$LOGFILE"

echo -e "\n📦 Broken or Partially Installed Packages:\n" | tee -a "$LOGFILE"
dpkg -l | grep -E '^..r|^..i' | tee -a "$LOGFILE"
sudo apt -f install --dry-run | tee -a "$LOGFILE"

echo -e "\n🔧 Crontab Errors (user and system):\n" | tee -a "$LOGFILE"
grep -i "error" /var/log/syslog | grep -i cron | tee -a "$LOGFILE"
sudo grep -i "error" /var/log/syslog | grep -i cron | tee -a "$LOGFILE"

echo -e "\n🕳️ System Log Warnings and Errors (/var/log/syslog):\n" | tee -a "$LOGFILE"
grep -iE "warn|error|fail" /var/log/syslog | tee -a "$LOGFILE"

echo -e "\n🕳️ Authentication Failures (/var/log/auth.log):\n" | tee -a "$LOGFILE"
grep -i "fail" /var/log/auth.log | tee -a "$LOGFILE"

echo -e "\n🔐 Sudo Log Events (/var/log/auth.log):\n" | tee -a "$LOGFILE"
grep -i "sudo" /var/log/auth.log | tee -a "$LOGFILE"

echo -e "\n📄 Saved Report Path: $LOGFILE"
