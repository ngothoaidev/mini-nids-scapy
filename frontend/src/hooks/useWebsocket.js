import { useEffect, useMemo, useRef, useState } from 'react'

const EMPTY_STATE = {
	overview: {
		total_packets: 0,
		uptime_sec: 0,
		packet_rate: 0,
		alert_count: 0,
	},
	protocols: {},
	top_flows: [],
	alerts: [],
	packets: [],
}

export default function useWebsocket(path = '/ws/live') {
	const [connected, setConnected] = useState(false)
	const [state, setState] = useState(EMPTY_STATE)
	const socketRef = useRef(null)

	const wsUrl = useMemo(() => {
		const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
		return `${protocol}//${window.location.host}${path}`
	}, [path])

	useEffect(() => {
		let cancelled = false
		const ws = new WebSocket(wsUrl)
		socketRef.current = ws

		ws.onopen = () => {
			if (!cancelled) setConnected(true)
		}

		ws.onmessage = (event) => {
			if (cancelled) return
			try {
				const payload = JSON.parse(event.data)
				setState((prev) => ({ ...prev, ...payload }))
			} catch {
				// Ignore malformed messages
			}
		}

		ws.onclose = () => {
			if (!cancelled) setConnected(false)
		}

		ws.onerror = () => {
			if (!cancelled) setConnected(false)
		}

		const heartbeat = window.setInterval(() => {
			if (ws.readyState === WebSocket.OPEN) {
				ws.send('ping')
			}
		}, 15000)

		return () => {
			cancelled = true
			window.clearInterval(heartbeat)
			ws.close()
		}
	}, [wsUrl])

	return {
		connected,
		...state,
	}
}
