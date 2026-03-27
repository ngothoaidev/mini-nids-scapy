from collections import defaultdict, deque
import time
import json
from datetime import datetime



class DetectionEngine:
    def __init__(self):
        self.port_scans = defaultdict(lambda: deque(maxlen=100))
        self.syn_floods = defaultdict(int)
        self.window = 60  # 60s window
        self.last_syn = defaultdict(float)
        self.alerts = []
    
    def check_port_scan(self, parsed):
        # Only check TCP packets for port scanning
        if parsed['proto'] != 'TCP':
            return None
        src_ip = parsed['src_ip']
        dst_port = parsed['dst_port']
        
        self.port_scans[src_ip].append((time.time(), dst_port))
        unique_ports = len(set(p[1] for p in self.port_scans[src_ip] if time.time() - p[0] < self.window)) # Count unique ports in the last 60s
        
        # Alert if more than 10 unique ports are targeted in the last 60s
        if unique_ports > 30:  # Threshold for port scan alert
            alert = f"[ALERT] Port scan from {src_ip}: {unique_ports} ports/60s"
            return alert
        return None
    
    def check_syn_flood(self, parsed):
        if parsed['proto'] != 'TCP' or parsed['tcp_flags'] != 2:  # SYN=2
            return None
        src_ip = parsed['src_ip']
        now = time.time()
        self.syn_floods[src_ip] = self.syn_floods[src_ip] + 1 if now - self.last_syn[src_ip] < 30 else 1
        
        # Alert if more than 50 SYN packets from the same IP in 30s
        if self.syn_floods[src_ip] > 50:  # KB 5.2
            return f"[ALERT] SYN flood from {src_ip}"
        return None
    
    def check_blacklist(self, parsed):
        # Check blacklist in data/blacklist.txt
        try:            
            with open("data/blacklist.txt") as f:
                blacklist = set(line.strip() for line in f)
            if parsed['src_ip'] in blacklist:
                return f"[ALERT] Blacklisted IP {parsed['src_ip']} attempted connection"
        except FileNotFoundError:
            pass

        return None

    def log_alert(self, alert, parsed):
        """KB 4.6: SIEM JSON log"""
        alert_type = "port_scan" if "Port scan" in alert else "syn_flood" if "SYN flood" in alert else "unknown"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "alert_type": alert_type,
            "src_ip": parsed['src_ip'],
            "dst_ip": parsed['dst_ip'],
            "severity": "high",
            "message": alert,
            "proto": parsed['proto']
        }
        
        # Append to JSONL (one JSON/line - SIEM standard)
        with open("data/alerts.json", "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
        
        print(f"[LOGGED] {log_entry['alert_type']} → data/alerts.json")

    
    def check(self, parsed):
        alert = self.check_port_scan(parsed) or self.check_syn_flood(parsed) or self.check_blacklist(parsed)
        if alert:
            self.log_alert(alert, parsed)
            self.alerts.append(alert)
        return alert
