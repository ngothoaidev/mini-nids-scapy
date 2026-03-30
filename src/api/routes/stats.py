from fastapi import APIRouter, Query

from src.api.ws.stream import live_state

router = APIRouter()


@router.get("/overview")
def get_overview():
	return live_state.get_overview()


@router.get("/protocols")
def get_protocols():
	return {"protocols": live_state.snapshot(max_alerts=0, max_packets=0)["protocols"]}


@router.get("/flows")
def get_flows(limit: int = Query(default=10, ge=1, le=100)):
	return {"top_flows": live_state.get_top_flows(limit=limit)}
