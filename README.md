# Mini Network Intrusion Detection System (NIDS)

Real-time packet-based IDS detecting port scans, SYN floods, suspicious IPs. 
![Architecture](Architecture.png)

## Features
- Live packet sniffing & parsing (Ethernet/IP/TCP/UDP/ICMP)
- Detect: Port scan, SYN flood, blacklist IPs
- CLI dashboard: Stats, alerts real-time
- JSON logging

## Demo

## Quick Start
```bash
git clone https://github.com/ngothoaidev/mini-nids-scapy.git
cd mini-nids-scapy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo python nids.py  # iface='lo' default
```

## Tech: 
Python, Scapy
