from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether

from src.parser import parse_packet

def process_packet_callback(packet):
    # Callback each time a packet is captured
    parsed = parse_packet(packet)
    if parsed:
        flags_str = f"flags={parsed['tcp_flags']}" if parsed['tcp_flags'] else ""
        # print(f"[PARSED] {parsed['proto']} {parsed['src_ip']}:{parsed['src_port'] or '?'} → {parsed['dst_ip']}:{parsed['dst_port'] or '?'} {flags_str}")
    return None

def sniff_packets(iface="lo", timeout=None, count=0, prn=process_packet_callback, filter="ip"):
    # Sniff packets on the specified interface
    try:
        sniff(iface=iface, timeout=timeout, count=count, prn=prn, filter=filter)
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    sniff_packets(iface="lo", count=100, filter="tcp or udp or icmp") 