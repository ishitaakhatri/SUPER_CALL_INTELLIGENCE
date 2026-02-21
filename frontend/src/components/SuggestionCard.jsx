export default function SuggestionCard({ suggestion, isProcessing }) {
    if (isProcessing) {
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
                    <div className="processing-indicator">
                        <div className="processing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                        Analyzing transcript and generating response...
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
                    <span className="highlight-script">{suggestion}</span>
                </div>
            </div>
        </div>
    );
}
