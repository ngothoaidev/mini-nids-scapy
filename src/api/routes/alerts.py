from fastapi import APIRouter, Query

from src.api.ws.stream import live_state

router = APIRouter()


@router.get("")
def get_alerts(limit: int = Query(default=20, ge=1, le=100)):
	return {"alerts": live_state.get_alerts(limit=limit)}
