import { useState, useCallback, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket.js';
import { useAzureSpeech } from './hooks/useSpeechRecognition.js';
import TranscriptPanel from './components/TranscriptPanel.jsx';
import MemberCard from './components/MemberCard.jsx';
import KnowledgeCard from './components/KnowledgeCard.jsx';
import ComplianceCard from './components/ComplianceCard.jsx';
import SuggestionCard from './components/SuggestionCard.jsx';
import PostCallCard from './components/PostCallCard.jsx';

// Determine WebSocket URL
const WS_URL = import.meta.env.DEV
    ? `ws://${window.location.hostname}:8000/stream`
    : `ws://${window.location.host}/stream`;

export default function App() {
    const [inputText, setInputText] = useState('');
    const [callActive, setCallActive] = useState(false);
    const [showEvaluation, setShowEvaluation] = useState(false);

    // Speaker toggle for typed demo messages
    const [demoSpeaker, setDemoSpeaker] = useState('Customer');

    const {
        isConnected,
        isProcessing,
        transcripts,
        memberProfile,
        knowledgeDocs,
        complianceAlerts,
        suggestion,
        intent,
        postCallEvaluation,
        sendMessage,
        endCall,
        resetState,
    } = useWebSocket(WS_URL);

    // Azure Speech callback
    const onAzureTranscript = useCallback(
        (event) => {
            sendMessage(event.text, event.isFinal, event.speaker, event.offset);
        },
        [sendMessage]
    );

    // Azure Speech — token is fetched from backend, no keys in frontend
    const { isListening, error: speechError, toggleListening } = useAzureSpeech({
        onTranscript: onAzureTranscript,
    });

    // ─── Call Lifecycle ─── //
    const handleStartCall = () => {
        resetState();
        setCallActive(true);
        setShowEvaluation(false);
    };

    const handleEndCall = () => {
        if (isListening) toggleListening(); // Stop mic
        endCall(); // Request post-call evaluation from backend
        setCallActive(false);
        setShowEvaluation(true);
    };

    const handleNewCall = () => {
        resetState();
        setCallActive(false);
        setShowEvaluation(false);
    };

    // ─── Text Input (Demo Mode) ─── //
    const handleSend = () => {
        const text = inputText.trim();
        if (!text) return;
        sendMessage(text, true, demoSpeaker, 0);
        setInputText('');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Connection status
    const statusText = isProcessing
        ? 'Processing...'
        : isListening
            ? 'Listening...'
            : isConnected
                ? 'Connected'
                : 'Disconnected';

    const statusClass = isProcessing
        ? 'processing'
        : isListening
            ? 'processing'
            : isConnected
                ? ''
                : 'disconnected';

    return (
        <div className="app">
            {/* ─── Header ─── */}
            <header className="app-header">
                <h1>⚡ Super Call Intelligence — FNOL Dashboard</h1>
                <div className="header-status">
                    {intent && (
                        <span className={`intent-badge ${intent.intent}`}>
                            {intent.intent?.replace(/_/g, ' ')}
                        </span>
                    )}
                    <span className={`status-dot ${statusClass}`} />
                    <span>{statusText}</span>

                    {/* Call controls */}
                    {!callActive && !showEvaluation && (
                        <button className="btn-call start" onClick={handleStartCall} disabled={!isConnected}>
                            📞 Start Call
                        </button>
                    )}
                    {callActive && (
                        <button className="btn-call end" onClick={handleEndCall}>
                            ⏹ End Call
                        </button>
                    )}
                    {showEvaluation && (
                        <button className="btn-call new" onClick={handleNewCall}>
                            🔄 New Call
                        </button>
                    )}
                </div>
            </header>

            {/* ─── Left: Transcript Panel ─── */}
            <TranscriptPanel transcripts={transcripts} />

            {/* ─── Right: Cards Grid or Post-Call Evaluation ─── */}
            {showEvaluation && postCallEvaluation ? (
                <PostCallCard evaluation={postCallEvaluation} />
            ) : (
                <main className="cards-area">
                    <MemberCard member={memberProfile} />
                    <KnowledgeCard docs={knowledgeDocs} />
                    <ComplianceCard alerts={complianceAlerts} />
                    <SuggestionCard suggestion={suggestion} isProcessing={isProcessing} />
                </main>
            )}

            {/* ─── Input Bar ─── */}
            <div className="input-bar">
                {/* Mic button (Azure Speech) */}
                <button
                    className={`btn-mic ${isListening ? 'active' : ''}`}
                    onClick={toggleListening}
                    disabled={!callActive}
                    title={isListening ? 'Stop listening' : 'Start voice input (Azure Speech)'}
                >
                    {isListening ? '⏹' : '🎙️'}
                </button>

                {/* Speaker toggle for demo */}
                <button
                    className={`btn-speaker ${demoSpeaker.toLowerCase()}`}
                    onClick={() => setDemoSpeaker(demoSpeaker === 'Customer' ? 'Agent' : 'Customer')}
                    title={`Speaking as: ${demoSpeaker}`}
                >
                    {demoSpeaker === 'Customer' ? '👤' : '🧑‍💼'}
                </button>

                <input
                    type="text"
                    placeholder={`Type as ${demoSpeaker}... e.g. "My policy is CAR-100001, I had an accident"`}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={!isConnected || (!callActive && !showEvaluation)}
                />
                <button
                    className="btn-send"
                    onClick={handleSend}
                    disabled={!isConnected || !inputText.trim() || !callActive}
                >
                    Send ⏎
                </button>
            </div>

            {/* Speech error toast */}
            {speechError && (
                <div className="error-toast">
                    ⚠️ Azure Speech: {speechError}
                </div>
            )}
        </div>
    );
}
