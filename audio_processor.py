import os
import tempfile
import numpy as np
from pydub import AudioSegment
import librosa
import librosa.display

class AudioProcessor:
    """Handles audio extraction and feature processing"""
    
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.supported_formats = ['.mp4', '.avi', '.mkv', '.webm', '.mov', '.mp3', '.wav', '.m4a']
    
    def extract_audio(self, video_path, max_duration_seconds=300):
        """
        Extract audio from video file
        
        Args:
            video_path (str): Path to video file
            max_duration_seconds (int): Maximum duration to process
            
        Returns:
            str: Path to extracted audio file
        """
        try:
            # Load video and extract audio
            audio = AudioSegment.from_file(video_path)
            
            # Limit duration if specified
            if max_duration_seconds and len(audio) > max_duration_seconds * 1000:
                audio = audio[:max_duration_seconds * 1000]
            
            # Convert to mono and set sample rate
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(self.sample_rate)
            
            # Create temporary file for audio
            temp_dir = os.path.dirname(video_path)
            audio_path = os.path.join(temp_dir, "extracted_audio.wav")
            
            # Export as WAV
            audio.export(audio_path, format="wav")
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Audio extraction failed: {str(e)}")
    
    def extract_features(self, audio_path):
        """
        Extract audio features for accent analysis
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Dictionary containing audio features
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Basic audio properties
            duration = len(y) / sr
            
            # Extract various features
            features = {}
            
            # 1. Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features['spectral_centroid_mean'] = np.mean(spectral_centroids)
            features['spectral_centroid_std'] = np.std(spectral_centroids)
            
            # 2. MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            for i in range(13):
                features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
                features[f'mfcc_{i}_std'] = np.std(mfccs[i])
            
            # 3. Chroma features
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            features['chroma_mean'] = np.mean(chroma)
            features['chroma_std'] = np.std(chroma)
            
            # 4. Spectral rolloff
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            features['rolloff_mean'] = np.mean(rolloff)
            features['rolloff_std'] = np.std(rolloff)
            
            # 5. Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            features['zcr_mean'] = np.mean(zcr)
            features['zcr_std'] = np.std(zcr)
            
            # 6. Tempo and rhythm
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = tempo
            
            # 7. Pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                features['pitch_mean'] = np.mean(pitch_values)
                features['pitch_std'] = np.std(pitch_values)
                features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
            else:
                features['pitch_mean'] = 0
                features['pitch_std'] = 0
                features['pitch_range'] = 0
            
            # 8. Energy and dynamics
            rms = librosa.feature.rms(y=y)[0]
            features['rms_mean'] = np.mean(rms)
            features['rms_std'] = np.std(rms)
            
            # 9. Spectral bandwidth
            bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            features['bandwidth_mean'] = np.mean(bandwidth)
            features['bandwidth_std'] = np.std(bandwidth)
            
            # 10. Audio quality metrics
            features['duration'] = duration
            features['sample_rate'] = sr
            features['audio_length'] = len(y)
            
            # 11. Speech rate estimation (approximate)
            # Count zero-crossing rate peaks as proxy for speech segments
            speech_segments = self._estimate_speech_segments(y, sr)
            features['speech_rate'] = len(speech_segments) / duration if duration > 0 else 0
            
            return features
            
        except Exception as e:
            raise Exception(f"Feature extraction failed: {str(e)}")
    
    def _estimate_speech_segments(self, y, sr, frame_length=2048, hop_length=512):
        """Estimate speech segments using energy-based segmentation"""
        try:
            # Calculate frame-wise energy
            frame_energy = []
            for i in range(0, len(y) - frame_length, hop_length):
                frame = y[i:i + frame_length]
                energy = np.sum(frame ** 2)
                frame_energy.append(energy)
            
            frame_energy = np.array(frame_energy)
            
            # Threshold for speech detection (adaptive)
            threshold = np.mean(frame_energy) * 0.3
            
            # Find speech segments
            speech_frames = frame_energy > threshold
            segments = []
            
            in_speech = False
            start_frame = 0
            
            for i, is_speech in enumerate(speech_frames):
                if is_speech and not in_speech:
                    start_frame = i
                    in_speech = True
                elif not is_speech and in_speech:
                    segments.append((start_frame, i))
                    in_speech = False
            
            # Close last segment if needed
            if in_speech:
                segments.append((start_frame, len(speech_frames)))
            
            return segments
            
        except Exception:
            return []
    
    def get_audio_quality_score(self, audio_path):
        """Calculate audio quality score for confidence weighting"""
        try:
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Signal-to-noise ratio estimation
            signal_power = np.mean(y ** 2)
            noise_power = np.var(y - np.mean(y))
            snr = signal_power / noise_power if noise_power > 0 else float('inf')
            
            # Dynamic range
            dynamic_range = np.max(np.abs(y)) - np.min(np.abs(y))
            
            # Clipping detection
            clipping_ratio = np.sum(np.abs(y) > 0.95) / len(y)
            
            # Overall quality score (0-100)
            quality_score = min(100, max(0, 
                (np.log10(snr) * 20) * 0.4 +  # SNR component
                (dynamic_range * 100) * 0.4 +  # Dynamic range component
                (1 - clipping_ratio) * 100 * 0.2  # Anti-clipping component
            ))
            
            return quality_score
            
        except Exception:
            return 50.0  # Default medium quality
