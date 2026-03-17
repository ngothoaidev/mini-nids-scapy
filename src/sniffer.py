from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether

def process_packet_callback(packet):
    # Callback each time a packet is captured
    if Ether in packet and IP in packet:
        summary = packet.summary()
        print(f"[SNIFF] {summary}")
    return packet

def sniff_packets(iface="lo", timeout=None, count=0, prn=process_packet_callback, filter="ip"):
    # Sniff packets on the specified interface
    print(f"Sniffing on interface: {iface} with filter: '{filter}'")
    try:
        sniff(iface=iface, timeout=timeout, count=count, prn=prn, filter=filter)
    except KeyboardInterrupt:
        print("\nStopped sniffing")
    
if __name__ == "__main__":
    sniff_packets(iface="lo", count=100, filter="tcp or udp or icmp") 