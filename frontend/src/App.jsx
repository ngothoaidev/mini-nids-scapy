import AlertFeed from './components/AlertFeed'
import TopFlow from './components/TopFlow'
import TrafficChart from './components/TrafficChart'
import useWebsocket from './hooks/useWebsocket'

function MetricCard({ label, value }) {
	return (
		<article className="metric-card">
			<h3>{label}</h3>
			<p>{value}</p>
		</article>
	)
}

export default function App() {
	const { connected, overview, protocols, top_flows, alerts, packets } = useWebsocket('/ws/live')

	return (
		<main className="container">
			<header className="topbar">
				<h1>Mini NIDS Web Dashboard</h1>
				<span className={`status ${connected ? 'online' : 'offline'}`}>
					{connected ? 'Live' : 'Disconnected'}
				</span>
			</header>

			<section className="metric-grid">
				<MetricCard label="Total Packets" value={overview?.total_packets ?? 0} />
				<MetricCard label="Uptime (s)" value={overview?.uptime_sec ?? 0} />
				<MetricCard label="Packets / sec" value={overview?.packet_rate ?? 0} />
				<MetricCard label="Alert Count" value={overview?.alert_count ?? 0} />
			</section>

			<section className="content-grid">
				<TrafficChart protocols={protocols} />
				<TopFlow flows={top_flows} />
			</section>

			<AlertFeed alerts={alerts} />

			<section className="panel">
				<header className="panel-header">
					<h2>Recent Packet Traffic</h2>
				</header>

				{packets?.length ? (
					<div className="table-wrap">
						<table>
							<thead>
								<tr>
									<th>Proto</th>
									<th>Source</th>
									<th>Destination</th>
									<th>Len</th>
								</tr>
							</thead>
							<tbody>
								{packets.map((pkt, idx) => (
									<tr key={`${pkt.timestamp}-${idx}`}>
										<td>{pkt.proto}</td>
										<td>{`${pkt.src_ip}:${pkt.src_port ?? 0}`}</td>
										<td>{`${pkt.dst_ip}:${pkt.dst_port ?? 0}`}</td>
										<td>{pkt.packet_len ?? 0}</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<p className="muted">No packets captured.</p>
				)}
			</section>
		</main>
	)
}
