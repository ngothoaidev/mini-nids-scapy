import argparse
import os
import subprocess
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini NIDS API runtime")
    parser.add_argument("--host", default="0.0.0.0", help="Host for API server")
    parser.add_argument("--port", type=int, default=8000, help="Port for API server")
    parser.add_argument("--iface", default="lo", help="Network interface to sniff")
    parser.add_argument("--bpf", default="tcp or udp or icmp", help="BPF capture filter")
    args = parser.parse_args()

    os.environ["NIDS_IFACE"] = args.iface
    os.environ["NIDS_BPF"] = args.bpf

    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "src.api.app:app",
            "--host",
            args.host,
            "--port",
            str(args.port),
        ],
        check=True,
    )
