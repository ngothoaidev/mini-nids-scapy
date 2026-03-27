from scapy.all import *
import time
from src.sniffer import process_packet_callback, sniff_packets  # Callback đã có parser
from src.parser import parse_packet
from src.stats import StatsTracker
from src.detection import DetectionEngine

stats = StatsTracker()  # Initialize stats tracker
detection = DetectionEngine()

def process_packet(packet):
    """Main pipeline: sniff → parse (Ngày 3)"""
    parsed = parse_packet(packet)
    if parsed:
        stats.update(parsed)  # Update stats with parsed packet data

        alert = detection.check(parsed)
        if alert:
            print(alert)  # Console alert
            stats.alerts.append(alert)  # Dashboard
        if time.time() % 5 < 0.1:  # Print dashboard every 5 seconds
            stats.print_dashboard()
        process_packet_callback(packet)  # Print parsed
    return packet

if __name__ == "__main__":
    print("Mini NIDS v0.2 starting... (Ctrl+C stop)")
    print("Test: curl google.com or ping 8.8.8.8 in other terminal")
    sniff_packets(iface="wlp4s0", prn=process_packet, filter="tcp or udp or icmp")
