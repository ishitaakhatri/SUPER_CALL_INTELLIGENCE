import { useRef, useEffect } from 'react';

export default function SuggestionCard({ suggestion, isProcessing }) {
    const bottomRef = useRef(null);

    // Auto-scroll to the latest suggestion
    useEffect(() => {
        setTimeout(() => {
            bottomRef.current?.scrollIntoView({ behavior: 'auto', block: 'end' });
        }, 50);
    }, [suggestion, isProcessing]);

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
                        <div className="processing-indicator" style={{ marginTop: '8px' }}>
                            <div className="processing-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            Generating more...
                        </div>
                    )}
                    <div ref={bottomRef} />
                </div>
            </div>
        </div>
    );
}
