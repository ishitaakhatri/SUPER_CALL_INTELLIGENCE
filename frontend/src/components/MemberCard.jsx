export default function MemberCard({ member }) {
    if (!member) {
        return (
            <div className="card member empty">
                <div className="empty-state">
                    <div className="empty-icon">👤</div>
                    <h3>Policyholder Profile</h3>
                    <p>Mention a policy ID to load (e.g., CAR-100001)</p>
                </div>
            </div>
        );
    }

    const isCarPolicy = member.policyId?.startsWith('CAR');
    const isLifePolicy = member.policyId?.startsWith('LIFE');

    return (
        <div className="card member">
            <div className="card-header">
                <div className="card-icon">👤</div>
                <div>
                    <div className="card-title">{member.name}</div>
                    <div className="card-subtitle">{member.policyId}</div>
                </div>
            </div>
            <div className="card-body">
                <div className="member-grid">
                    <div className="member-field">
                        <span className="label">Policy Type</span>
                        <span className="value">
                            <span className={`member-badge ${isCarPolicy ? 'car' : 'life'}`}>
                                {isCarPolicy ? '🚗' : '🛡️'} {member.coverageType}
                            </span>
                        </span>
                    </div>
                    <div className="member-field">
                        <span className="label">Status</span>
                        <span className="value">
                            <span className="member-badge active">{member.status}</span>
                        </span>
                    </div>
                    <div className="member-field">
                        <span className="label">Coverage Amount</span>
                        <span className="value">₹{(member.coverageAmount || 0).toLocaleString('en-IN')}</span>
                    </div>
                    <div className="member-field">
                        <span className="label">Premium</span>
                        <span className="value">₹{(member.premium || 0).toLocaleString('en-IN')}/yr</span>
                    </div>

                    {/* Car-specific fields */}
                    {isCarPolicy && member.vehicle && (
                        <>
                            <div className="member-field">
                                <span className="label">Vehicle</span>
                                <span className="value">{member.vehicle.year} {member.vehicle.make} {member.vehicle.model}</span>
                            </div>
                            <div className="member-field">
                                <span className="label">License Plate</span>
                                <span className="value">{member.vehicle.licensePlate}</span>
                            </div>
                            <div className="member-field">
                                <span className="label">Deductible</span>
                                <span className="value">₹{(member.deductible || 0).toLocaleString('en-IN')}</span>
                            </div>
                            <div className="member-field">
                                <span className="label">Prior Claims</span>
                                <span className="value">{member.claimHistory?.length || 0}</span>
                            </div>
                        </>
                    )}

                    {/* Life-specific fields */}
                    {isLifePolicy && member.beneficiaries && (
                        <>
                            <div className="member-field full-width">
                                <span className="label">Beneficiaries</span>
                                <span className="value">
                                    {member.beneficiaries.map((b) => `${b.name} (${b.relationship} — ${b.share})`).join(', ')}
                                </span>
                            </div>
                            <div className="member-field">
                                <span className="label">Contestability</span>
                                <span className="value">{member.contestabilityExpired ? 'Expired ✅' : 'Active ⚠️'}</span>
                            </div>
                        </>
                    )}

                    {/* Add-ons for car */}
                    {isCarPolicy && member.addOns?.length > 0 && (
                        <div className="member-field full-width">
                            <span className="label">Add-Ons</span>
                            <span className="value">{member.addOns.join(' • ')}</span>
                        </div>
                    )}

                    <div className="member-field">
                        <span className="label">Phone</span>
                        <span className="value">{member.phone}</span>
                    </div>
                    <div className="member-field">
                        <span className="label">Email</span>
                        <span className="value">{member.email}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
