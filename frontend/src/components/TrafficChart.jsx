export default function TrafficChart({ protocols = {} }) {
	const entries = Object.entries(protocols)
	const total = entries.reduce((sum, [, count]) => sum + count, 0)

	return (
		<section className="panel">
			<header className="panel-header">
				<h2>Protocol Distribution</h2>
			</header>

			{entries.length === 0 ? (
				<p className="muted">No packets captured.</p>
			) : (
				<div className="bar-list">
					{entries.map(([proto, count]) => {
						const pct = total > 0 ? (count / total) * 100 : 0
						return (
							<div key={proto} className="bar-item">
								<div className="bar-label">
									<span>{proto}</span>
									<span>{count}</span>
								</div>
								<div className="bar-track">
									<div className="bar-fill" style={{ width: `${pct}%` }} />
								</div>
							</div>
						)
					})}
				</div>
			)}
		</section>
	)
}
