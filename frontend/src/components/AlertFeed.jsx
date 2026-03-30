function formatTime(value) {
	if (!value) return '-'
	const d = new Date(value)
	if (Number.isNaN(d.getTime())) return '-'
	return d.toLocaleTimeString()
}

export default function AlertFeed({ alerts = [] }) {
	return (
		<section className="panel">
			<header className="panel-header">
				<h2>Live Alerts</h2>
				<span className="badge danger">{alerts.length}</span>
			</header>

			{alerts.length === 0 ? (
				<p className="muted">No alerts yet.</p>
			) : (
				<ul className="alert-list">
					{alerts.map((alert, index) => (
						<li key={`${alert.timestamp}-${index}`} className="alert-item">
							<div className="alert-top">
								<strong>{alert.src_ip ?? '-'}</strong>
								<span>{formatTime(alert.timestamp)}</span>
							</div>
							<p>{alert.message}</p>
						</li>
					))}
				</ul>
			)}
		</section>
	)
}
