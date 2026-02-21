import { useRef, useEffect } from 'react';

/**
 * Live transcript panel with speaker labels and timestamps.
 * Matches the architecture screenshot: [Customer 00:00:12]: "text"
 */
export default function TranscriptPanel({ transcripts }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [transcripts]);

    const getSpeakerClass = (speaker) => {
        if (!speaker) return '';
        const s = speaker.toLowerCase();
        if (s.includes('agent')) return 'speaker-agent';
        if (s.includes('customer')) return 'speaker-customer';
        return 'speaker-unknown';
    };

    return (
        <div className="transcript-panel">
            <div className="panel-header">
                <span className="icon">🎙️</span>
                Live Transcript Stream
            </div>
            <div className="transcript-messages">
                {transcripts.length === 0 && (
                    <div className="empty-state">
                        <div className="empty-icon">💬</div>
                        <h3>No Transcript Yet</h3>
                        <p>Start a call or type a message to begin</p>
                    </div>
                )}
                {transcripts.map((t) => (
                    <div
                        key={t.id}
                        className={`transcript-line ${t.is_finalized ? 'finalized' : 'partial'} ${getSpeakerClass(t.speaker)}`}
                    >
                        {t.speaker && t.is_finalized && (
                            <span className={`speaker-tag ${getSpeakerClass(t.speaker)}`}>
                                [{t.speaker} {t.timestamp || ''}]
                            </span>
                        )}
                        <span className="transcript-text">
                            {t.is_finalized ? `"${t.text}"` : t.text}
                        </span>
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
        </div>
    );
}
