import argparse
from src.sniffer import sniff_packets
from src.parser import parse_packet
from src.stats import StatsTracker
from src.detection import DetectionEngine
from src.dashboard import Dashboard

stats = StatsTracker()  # Initialize stats tracker
detection = DetectionEngine()
dashboard = Dashboard(stats)

def process_packet(packet):
    """Main pipeline: sniff → parse (Ngày 3)"""
    parsed = parse_packet(packet)
    if parsed:
        stats.update(parsed)  # Update stats with parsed packet data

        alert = detection.check(parsed)
        if alert:
            # print(alert)  # Console alert
            stats.alerts.append(alert)  # Dashboard
        dashboard.refresh()
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini NIDS runtime")
    parser.add_argument("--iface", default="lo", help="Network interface to sniff")
    parser.add_argument("--bpf", default="tcp or udp or icmp", help="BPF capture filter")
    args = parser.parse_args()

    dashboard.start()
    try:
        sniff_packets(iface=args.iface, prn=process_packet, filter=args.bpf)
    finally:
        dashboard.stop()
