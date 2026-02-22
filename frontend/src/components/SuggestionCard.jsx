export default function SuggestionCard({ suggestion, isProcessing }) {
    if (isProcessing && !suggestion) {
        return (
            <div className="card suggestion">
                <div className="card-header">
                    <div className="card-icon">💡</div>
                    <div>
                        <div className="card-title">Suggested Response</div>
                        <div className="card-subtitle">Generating...</div>
                    </div>
                </div>
                <div className="card-body">
                    <div className="suggestion-shimmer">
                        <div className="shimmer-line" />
                        <div className="shimmer-line" />
                        <div className="shimmer-line" />
                    </div>
                </div>
            </div>
        );
    }

    if (!suggestion) {
        return (
            <div className="card suggestion empty">
                <div className="empty-state">
                    <div className="empty-icon">💡</div>
                    <h3>Suggested Response</h3>
                    <p>AI-generated talking points for the agent will appear here</p>
                </div>
            </div>
        );
    }

    // Split multiple suggestions separated by double newlines into distinct bubbles
    const suggestionsList = suggestion
        .split('\n\n')
        .map(s => s.trim())
        .filter(s => s.length > 0);

    return (
        <div className="card suggestion">
            <div className="card-header">
                <div className="card-icon">💡</div>
                <div>
                    <div className="card-title">Suggested Response</div>
                    <div className="card-subtitle">Ready to use</div>
                </div>
            </div>
            <div className="card-body">
                <div className="suggestion-text">
                    {suggestionsList.map((text, idx) => (
                        <span key={idx} className="highlight-script">{text}</span>
                    ))}
                    {isProcessing && (
                        <div className="suggestion-shimmer" style={{ marginTop: '4px' }}>
                            <div className="shimmer-line" />
                            <div className="shimmer-line" />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
