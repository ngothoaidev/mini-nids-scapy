from collections import defaultdict
import time
from rich.console import Console
from rich.table import Table

class StatsTracker:
    def __init__(self):
        self.proto_stats = defaultdict(int)
        self.flows = defaultdict(int)
        self.console = Console()
        self.alerts = []
        self.start_time = time.time()

    def get_uptime(self):
        return time.time() - self.start_time
    
    def update(self, parsed):
        # Update protocol stats
        proto = parsed['proto']
        # Update flow stats
        self.proto_stats[proto] += 1 

        flow_key = f"{parsed['src_ip']}:{parsed['src_port'] or 0} -> {parsed['dst_ip']}:{parsed['dst_port'] or 0}"
        self.flows[flow_key] += 1

    def print_dashboard(self):
        # Print protocol stats
        total = sum(self.proto_stats.values()) # Get total packets

        duration = self.get_uptime()

        table = Table(title=f"Mini NIDS Dashboard (Uptime: {duration:.1f}s, Total Packets: {total})")
        table.add_column("Protocol", style="cyan")
        table.add_column("Count", style="magenta")
        table.add_column("Percentage", style="green")
        table.add_column("Top Flows", style="yellow")

        for proto in sorted(self.proto_stats, key=self.proto_stats.get, reverse=True):
            pct = (self.proto_stats[proto] / total * 100) if total else 0
            top_flows = max(self.flows.items(), key=lambda x: x[1] if proto in x[0] else 0, default=('', 0))[0][:30]
            table.add_row(proto, str(self.proto_stats[proto]), f"{pct:.1f}%", top_flows)
        
        self.console.print(table)

        if self.alerts:
            self.console.print("[red][ALERTS] Found potential threats![/red]", self.alerts[-3:])