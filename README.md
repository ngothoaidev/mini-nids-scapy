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

## Attack Demo (2 terminals)

1) Start NIDS dashboard/sniffer:

sudo python3 main.py --iface lo --bpf "tcp or udp or icmp"

2) In another terminal, run attacks:

python3 demo/attacks.py --attack all --target 127.0.0.1

You should see alerts for port scan, SYN flood, and blacklisted source traffic.

## Tech: 
Python, Scapy
