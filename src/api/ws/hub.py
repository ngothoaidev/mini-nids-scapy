from __future__ import annotations

import asyncio

from fastapi import WebSocket


class WebSocketHub:
	# A Hub to manage WebSocket connections and broadcast messages to multiple clients.
	def __init__(self):
		self._connections = set() 
		self._lock = asyncio.Lock() # To protect access to the connections set in async context

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		async with self._lock:
			self._connections.add(websocket)

	async def disconnect(self, websocket: WebSocket):
		async with self._lock:
			self._connections.discard(websocket)

	async def broadcast(self, payload):
		async with self._lock:
			clients = list(self._connections)

		stale = []
		for ws in clients:
			try:
				await ws.send_json(payload)
			except Exception:
				stale.append(ws)

		if stale: # Clean up stale connections
			async with self._lock:
				for ws in stale:
					self._connections.discard(ws)
