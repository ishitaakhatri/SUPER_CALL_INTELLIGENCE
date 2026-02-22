export default function ComplianceCard({ alerts }) {
    if (!alerts || alerts.length === 0) {
        return (
            <div className="card compliance compact-empty">
                <div className="card-header">
                    <div className="card-icon">⚖️</div>
                    <div>
                        <div className="card-title">Compliance Alerts</div>
                        <div className="card-subtitle">No active alerts</div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="card compliance">
            <div className="card-header">
                <div className="card-icon">⚖️</div>
                <div>
                    <div className="card-title">Compliance Alerts</div>
                    <div className="card-subtitle">{alerts.length} active alert{alerts.length !== 1 ? 's' : ''}</div>
                </div>
            </div>
            <div className="card-body">
                {alerts.map((alert) => (
                    <div key={alert.ruleId} className={`compliance-alert ${alert.severity}`}>
                        <div className="alert-title">
                            {alert.severity === 'critical' ? '🚨' : alert.severity === 'high' ? '⚠️' : '📋'}{' '}
                            {alert.title}
                        </div>
                        {alert.message}
                    </div>
                ))}
            </div>
        </div>
    );
}
