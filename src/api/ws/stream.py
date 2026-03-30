from src.api.ws.hub import WebSocketHub
from src.service.live_state import LiveState
from src.service.traffic_capture import TrafficCaptureService


live_state = LiveState()
websocket_hub = WebSocketHub()
traffic_capture_service = TrafficCaptureService(live_state, websocket_hub)
