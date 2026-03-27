from scapy.layers.inet import IP, TCP, UDP, ICMP

def parse_packet(packet):
    # Extract metadata: src_ip, dst_ip, proto, ports, flag
    if not packet.haslayer(IP):
        return None
    parsed = {
        'src_ip': packet[IP].src,
        'dst_ip': packet[IP].dst,
        'proto': 'TCP' if TCP in packet else 'UDP' if UDP in packet else 'ICMP',
        'src_port': packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else None),
        'dst_port': packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else None),
        'tcp_flags': packet[TCP].flags if TCP in packet else None,
        'timestamp': packet.time
    }
    return parsed