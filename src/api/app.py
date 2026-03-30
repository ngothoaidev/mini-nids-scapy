from __future__ import annotations

import asyncio
import os

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.api.routes.alerts import router as alerts_router
from src.api.routes.stats import router as stats_router
from src.api.ws.stream import traffic_capture_service
from src.db.base import engine


NIDS_IFACE = os.getenv("NIDS_IFACE", "lo")
NIDS_BPF = os.getenv("NIDS_BPF", "tcp or udp or icmp")

traffic_capture_service.configure(iface=NIDS_IFACE, bpf=NIDS_BPF)

app = FastAPI(title="Mini NIDS API", version="1.0.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(stats_router, prefix="/api/stats", tags=["stats"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["alerts"])


@app.get("/health")
def health():
	return {
		"status": "ok",
		"iface": NIDS_IFACE,
		"bpf": NIDS_BPF,
	}


@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
	await traffic_capture_service.websocket_handler(websocket)


@app.on_event("startup")
async def on_startup():
	# Fail fast if DB is not reachable during app boot.
	async with engine.connect() as conn:
		await conn.execute(text("SELECT 1"))

	traffic_capture_service.start(asyncio.get_running_loop())


@app.on_event("shutdown")
async def on_shutdown():
	traffic_capture_service.stop()
	await engine.dispose()
