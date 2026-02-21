import { useState, useRef, useCallback } from 'react';
import * as SpeechSDK from 'microsoft-cognitiveservices-speech-sdk';

/**
 * Custom hook for Azure Speech SDK with real-time transcription
 * and speaker diarization (ConversationTranscriber).
 *
 * Uses a short-lived token fetched from the backend (/api/speech-token)
 * so the API key never touches the browser.
 */
export function useAzureSpeech({ onTranscript }) {
    const [isListening, setIsListening] = useState(false);
    const [error, setError] = useState(null);
    const transcriberRef = useRef(null);

    const fetchToken = async () => {
        const baseUrl = import.meta.env.DEV
            ? `http://${window.location.hostname}:8000`
            : '';
        const res = await fetch(`${baseUrl}/api/speech-token`);
        const data = await res.json();
        if (data.error) throw new Error(data.error);
        return data; // { token, region }
    };

    const startListening = useCallback(async () => {
        try {
            setError(null);
            const { token, region } = await fetchToken();

            const speechConfig = SpeechSDK.SpeechConfig.fromAuthorizationToken(token, region);
            speechConfig.speechRecognitionLanguage = 'en-US';

            const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
            const transcriber = new SpeechSDK.ConversationTranscriber(speechConfig, audioConfig);

            // ─── Interim results (partial) ─── //
            transcriber.transcribing = (s, e) => {
                if (e.result.reason === SpeechSDK.ResultReason.RecognizingSpeech) {
                    onTranscript?.({
                        text: e.result.text,
                        speaker: e.result.speakerId || 'Unknown',
                        isFinal: false,
                        offset: e.result.offset,
                        duration: e.result.duration,
                    });
                }
            };

            // ─── Final results ─── //
            transcriber.transcribed = (s, e) => {
                if (e.result.reason === SpeechSDK.ResultReason.RecognizedSpeech && e.result.text) {
                    onTranscript?.({
                        text: e.result.text,
                        speaker: e.result.speakerId || 'Unknown',
                        isFinal: true,
                        offset: e.result.offset,
                        duration: e.result.duration,
                    });
                }
            };

            transcriber.canceled = (s, e) => {
                if (e.reason === SpeechSDK.CancellationReason.Error) {
                    console.error('Azure Speech error:', e.errorDetails);
                    setError(e.errorDetails);
                }
                setIsListening(false);
            };

            transcriber.sessionStopped = () => {
                setIsListening(false);
            };

            transcriber.startTranscribingAsync(
                () => {
                    setIsListening(true);
                    console.log('🎙️ Azure Speech: transcription started with diarization');
                },
                (err) => {
                    console.error('Failed to start Azure Speech:', err);
                    setError(String(err));
                }
            );

            transcriberRef.current = transcriber;
        } catch (err) {
            console.error('Azure Speech init error:', err);
            setError(err.message);
        }
    }, [onTranscript]);

    const stopListening = useCallback(() => {
        if (transcriberRef.current) {
            transcriberRef.current.stopTranscribingAsync(
                () => {
                    console.log('🎙️ Azure Speech: transcription stopped');
                    transcriberRef.current?.close();
                    transcriberRef.current = null;
                },
                (err) => console.error('Error stopping transcription:', err)
            );
        }
        setIsListening(false);
    }, []);

    const toggleListening = useCallback(() => {
        if (isListening) {
            stopListening();
        } else {
            startListening();
        }
    }, [isListening, startListening, stopListening]);

    return {
        isListening,
        error,
        startListening,
        stopListening,
        toggleListening,
    };
}
