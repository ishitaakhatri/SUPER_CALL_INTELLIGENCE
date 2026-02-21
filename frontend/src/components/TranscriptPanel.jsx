import { useRef, useEffect } from 'react';

/**
 * Live transcript panel with speaker diarization.
 * Agent = Guest-1 (cyan), Customer = Guest-2 (amber).
 * Shows [Agent 00:00:12]: "text" format with live pulse when listening.
 */
export default function TranscriptPanel({ transcripts, callActive, isListening }) {
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
                {isListening && <span className="live-badge">● LIVE</span>}
            </div>
            <div className="transcript-messages">
                {transcripts.length === 0 && (
                    <div className="empty-state">
                        <div className="empty-icon">🎧</div>
                        <h3>{callActive ? 'Listening...' : 'No Active Call'}</h3>
                        <p>
                            {callActive
                                ? 'Speak into the microphone. The agent should speak first.'
                                : 'Click "Start Call" to begin listening. Azure Speech will automatically distinguish between Agent and Customer.'}
                        </p>
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
