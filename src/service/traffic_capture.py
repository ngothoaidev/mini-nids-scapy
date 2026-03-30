from __future__ import annotations

import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from scapy.all import AsyncSniffer

from src.api.ws.hub import WebSocketHub
from src.core.parser import parse_packet
from src.service.live_state import LiveState


class TrafficCaptureService:
	# Service to capture live traffic, parse it, update state, and broadcast to WebSocket clients.
	def __init__(self, state: LiveState, hub: WebSocketHub):
		self.state = state
		self.hub = hub
		self.iface = "lo"
		self.bpf = "tcp or udp or icmp"
		self._sniffer: AsyncSniffer | None = None # Scapy AsyncSniffer instance
		self._loop: asyncio.AbstractEventLoop | None = None

	# def configure(self, iface: str, bpf: str):
	# 	self.iface = iface
	# 	self.bpf = bpf

	def start(self, loop: asyncio.AbstractEventLoop):
		# Start the AsyncSniffer in a separate thread to capture packets without blocking the event loop.
		if self._sniffer is not None:
			return
		self._loop = loop
		self._sniffer = AsyncSniffer(
			iface=self.iface,
			filter=self.bpf,
			prn=self._on_packet,
			store=False,
		)
		self._sniffer.start()

	def stop(self):
		if self._sniffer is None:
			return
		try:
			self._sniffer.stop()
		finally:
			self._sniffer = None

	def _on_packet(self, packet):
		parsed = parse_packet(packet)
		if not parsed:
			return

		payload = self.state.process_packet(parsed)
		if self._loop and self._loop.is_running():
			asyncio.run_coroutine_threadsafe(self.hub.broadcast(payload), self._loop)

	async def websocket_handler(self, websocket: WebSocket):
		await self.hub.connect(websocket)
		try:
			await websocket.send_json(self.state.snapshot())
			while True:
				await websocket.receive_text()
		except WebSocketDisconnect:
			pass
		finally:
			await self.hub.disconnect(websocket)
