export default function TopFlow({ flows = [] }) {
	return (
		<section className="panel">
			<header className="panel-header">
				<h2>Top Flows</h2>
			</header>

			{flows.length === 0 ? (
				<p className="muted">No traffic yet.</p>
			) : (
				<div className="table-wrap">
					<table>
						<thead>
							<tr>
								<th>Flow</th>
								<th>Packets</th>
							</tr>
						</thead>
						<tbody>
							{flows.map((flow) => (
								<tr key={flow.flow}>
									<td>{flow.flow}</td>
									<td>{flow.packets}</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
			)}
		</section>
	)
}