from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.live import Live


class Dashboard:
	"""Live CLI dashboard for protocol stats, top flows, and recent alerts."""

	def __init__(self, stats, refresh_per_second=4, max_flows=8, max_alerts=5):
		self.stats = stats
		self.refresh_per_second = refresh_per_second
		self.max_flows = max_flows
		self.max_alerts = max_alerts
		self._live = None

	def _build_overview_table(self):
		total = sum(self.stats.proto_stats.values())
		duration = max(0.001, self.stats.get_uptime())
		pps = total / duration

		table = Table(title=f"Mini NIDS Dashboard | Uptime: {duration:.1f}s | Total: {total} pkts | Rate: {pps:.2f} pkt/s")
		table.add_column("Protocol", style="cyan")
		table.add_column("Count", justify="right", style="magenta")
		table.add_column("Percent", justify="right", style="green")

		for proto, count in sorted(self.stats.proto_stats.items(), key=lambda x: x[1], reverse=True):
			pct = (count / total * 100) if total else 0
			table.add_row(proto, str(count), f"{pct:.1f}%")

		if not self.stats.proto_stats:
			table.add_row("-", "0", "0.0%")

		return table

	def _build_top_flows_table(self):
		table = Table(title="Top Flows")
		table.add_column("Flow", style="yellow")
		table.add_column("Packets", justify="right", style="magenta")

		for flow, count in sorted(self.stats.flows.items(), key=lambda x: x[1], reverse=True)[: self.max_flows]:
			table.add_row(flow, str(count))

		if not self.stats.flows:
			table.add_row("No traffic yet", "0")

		return table

	def _build_alerts_panel(self):
		if not self.stats.alerts:
			body = "[green]No alerts[/green]"
		else:
			recent = self.stats.alerts[-self.max_alerts :]
			body = "\n".join(f"[red]- {a}[/red]" for a in recent)
		return Panel(body, title="Recent Alerts", border_style="red")

	def _render(self):
		return Group(
			self._build_overview_table(),
			self._build_top_flows_table(),
			self._build_alerts_panel(),
		)

	def start(self):
		if self._live is not None:
			return
		self._live = Live(
			self._render(),
			refresh_per_second=self.refresh_per_second,
			console=self.stats.console,
			transient=False,
		)
		self._live.start()

	def refresh(self):
		if self._live is not None:
			self._live.update(self._render(), refresh=True)

	def stop(self):
		if self._live is not None:
			self._live.stop()
			self._live = None
