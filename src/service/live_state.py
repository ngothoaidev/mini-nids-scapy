from __future__ import annotations

import time
from collections import deque
from datetime import datetime
from threading import RLock

from src.core.detection import DetectionEngine
from src.core.stats import StatsTracker


class LiveState:
	def __init__(self):
		self.stats = StatsTracker()
		self.detection = DetectionEngine()
		self.recent_packets = deque(maxlen=200)
		self.recent_alerts = deque(maxlen=100)
		self._lock = RLock()

	def _top_flows(self, limit=10):
		return [
			{"flow": flow, "packets": count}
			for flow, count in sorted(self.stats.flows.items(), key=lambda x: x[1], reverse=True)[:limit]
		]

	def _protocols(self):
		return dict(sorted(self.stats.proto_stats.items(), key=lambda x: x[1], reverse=True))

	def _overview(self):
		total = sum(self.stats.proto_stats.values())
		duration = max(0.001, self.stats.get_uptime())
		return {
			"total_packets": total,
			"uptime_sec": round(duration, 2),
			"packet_rate": round(total / duration, 2),
			"alert_count": len(self.recent_alerts),
		}

	def process_packet(self, parsed):
		with self._lock:
			self.stats.update(parsed)
			alert = self.detection.check(parsed)

			packet_entry = {
				"timestamp": parsed["timestamp"],
				"src_ip": parsed["src_ip"],
				"dst_ip": parsed["dst_ip"],
				"src_port": parsed["src_port"],
				"dst_port": parsed["dst_port"],
				"proto": parsed["proto"],
				"tcp_flags": str(parsed["tcp_flags"]) if parsed.get("tcp_flags") else None,
				"packet_len": parsed.get("packet_len", 0),
			}
			self.recent_packets.appendleft(packet_entry)

			if alert:
				self.recent_alerts.appendleft(
					{
						"timestamp": datetime.utcnow().isoformat() + "Z",
						"message": alert,
						"src_ip": parsed["src_ip"],
						"dst_ip": parsed["dst_ip"],
						"proto": parsed["proto"],
					}
				)

			return self.snapshot()

	def snapshot(self, max_flows=10, max_alerts=20, max_packets=50):
		with self._lock:
			return {
				"type": "traffic_update",
				"timestamp": time.time(),
				"overview": self._overview(),
				"protocols": self._protocols(),
				"top_flows": self._top_flows(limit=max_flows),
				"alerts": list(self.recent_alerts)[:max_alerts],
				"packets": list(self.recent_packets)[:max_packets],
			}

	def get_overview(self):
		with self._lock:
			return self._overview()

	def get_top_flows(self, limit=10):
		with self._lock:
			return self._top_flows(limit=limit)

	def get_alerts(self, limit=20):
		with self._lock:
			return list(self.recent_alerts)[:limit]
