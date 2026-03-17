#!/usr/bin/env python3
"""
Mini NIDS - Network Intrusion Detection System (KB-based)
"""
from scapy.all import *
import json, time
from src.sniffer import sniff_packets
from src.parser import parse_packet
from src.detection import check_attacks
from src.dashboard import print_dashboard

if __name__ == "__main__":
    print("Mini NIDS starting... (Ctrl+C to stop)")
    sniff_packets(prn=lambda pkt: process_packet(pkt))
