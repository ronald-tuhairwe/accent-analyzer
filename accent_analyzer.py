import numpy as np
import speech_recognition as sr
import librosa
import re
from typing import Dict, List, Tuple
import tempfile
import os

class AccentAnalyzer:
    """Analyzes audio features to classify English accents"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Accent classification patterns and features
        self.accent_features = {
            'American': {
                'r_pronunciation': 'rhotic',
                'vowel_patterns': ['æ', 'ɑː', 'oʊ'],
                'tempo_range': (140, 180),
                'pitch_variation': 'moderate',
                'keywords': ['can\'t', 'dance', 'path', 'bath']
            },
            'British': {
                'r_pronunciation': 'non_rhotic',
                'vowel_patterns': ['ɑː', 'ɔː', 'əʊ'],
                'tempo_range': (120, 160),
                'pitch_variation': 'high',
                'keywords': ['can\'t', 'dance', 'path', 'bath']
            },
            'Australian': {
                'r_pronunciation': 'non_rhotic',
                'vowel_patterns': ['aɪ', 'eɪ', 'oʊ'],
                'tempo_range': (130, 170),
                'pitch_variation': 'high',
                'keywords': ['day', 'mate', 'no']
            },
            'Canadian': {
                'r_pronunciation': 'rhotic',
                'vowel_patterns': ['aʊ', 'oʊ', 'æ'],
                'tempo_range': (135, 175),
                'pitch_variation': 'moderate',
                'keywords': ['about', 'house', 'out']
            },
            'Indian': {
                'r_pronunciation': 'rhotic',
                'vowel_patterns': ['e', 'o', 'a'],
                'tempo_range': (150, 200),
                'pitch_variation': 'very_high',
                'keywords': ['very', 'good', 'only']
            }
        }
    
    def analyze_accent(self, audio_path: str, audio_features: Dict) -> Dict:
        """
        Main accent analysis function
        
        Args:
            audio_path (str): Path to audio file
            audio_features (dict): Pre-extracted audio features
            
        Returns:
            dict: Analysis results with accent classification and confidence
        """
        try:
            # Get speech-to-text transcription
            transcription = self._transcribe_audio(audio_path)
            
            # Analyze various accent indicators
            accent_scores = {}
            
            for accent_name in self.accent_features.keys():
                score = self._calculate_accent_score(accent_name, audio_features, transcription)
                accent_scores[accent_name] = score
            
            # Determine primary accent and confidence
            primary_accent = max(accent_scores, key=accent_scores.get)
            confidence = accent_scores[primary_accent]
            
            # Calculate English proficiency score
            english_proficiency = self._calculate_english_proficiency(audio_features, transcription)
            
            # Generate summary
            summary = self._generate_summary(primary_accent, confidence, transcription, audio_features)
            
            # Technical details for report
            technical_details = {
                'all_accent_scores': accent_scores,
                'transcription_length': len(transcription.split()) if transcription else 0,
                'audio_duration': audio_features.get('duration', 0),
                'speech_rate': audio_features.get('speech_rate', 0),
                'pitch_mean': audio_features.get('pitch_mean', 0),
                'tempo': audio_features.get('tempo', 0)
            }
            
            return {
                'accent': primary_accent,
                'confidence': confidence,
                'english_proficiency': english_proficiency,
                'summary': summary,
                'transcription': transcription,
                'technical_details': technical_details
            }
            
        except Exception as e:
            # Return default result with error information
            return {
                'accent': 'Unknown',
                'confidence': 0.0,
                'english_proficiency': 0.0,
                'summary': f'Analysis failed: {str(e)}',
                'transcription': '',
                'technical_details': {'error': str(e)}
            }
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using speech recognition"""
        try:
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record the audio data
                audio_data = self.recognizer.record(source)
                
                # Try to recognize speech using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    # Try with alternative recognition if Google fails
                    try:
                        text = self.recognizer.recognize_sphinx(audio_data)
                        return text
                    except:
                        return ""
                except sr.RequestError:
                    # If online services fail, return empty string
                    return ""
                    
        except Exception:
            return ""
    
    def _calculate_accent_score(self, accent_name: str, audio_features: Dict, transcription: str) -> float:
        """Calculate confidence score for a specific accent"""
        try:
            accent_info = self.accent_features[accent_name]
            score = 0.0
            max_score = 0.0
            
            # 1. Tempo analysis (20% weight)
            tempo = audio_features.get('tempo', 0)
            tempo_range = accent_info['tempo_range']
            if tempo_range[0] <= tempo <= tempo_range[1]:
                score += 20
            elif abs(tempo - np.mean(tempo_range)) < 30:
                score += 10
            max_score += 20
            
            # 2. Pitch variation analysis (25% weight)
            pitch_std = audio_features.get('pitch_std', 0)
            pitch_variation = accent_info['pitch_variation']
            
            if pitch_variation == 'very_high' and pitch_std > 80:
                score += 25
            elif pitch_variation == 'high' and 50 < pitch_std <= 80:
                score += 25
            elif pitch_variation == 'moderate' and 20 < pitch_std <= 50:
                score += 25
            elif pitch_variation == 'low' and pitch_std <= 20:
                score += 25
            max_score += 25
            
            # 3. Spectral features analysis (20% weight)
            mfcc_features = [audio_features.get(f'mfcc_{i}_mean', 0) for i in range(5)]
            
            # Compare MFCC patterns (simplified)
            if accent_name == 'American':
                if mfcc_features[1] > 0 and mfcc_features[2] < 0:
                    score += 15
            elif accent_name == 'British':
                if mfcc_features[1] < 0 and mfcc_features[3] > 0:
                    score += 15
            elif accent_name == 'Australian':
                if mfcc_features[2] > 0 and mfcc_features[4] > 0:
                    score += 15
            elif accent_name == 'Indian':
                if mfcc_features[0] > 10 and mfcc_features[1] > 0:
                    score += 15
            
            max_score += 20
            
            # 4. Speech rate analysis (15% weight)
            speech_rate = audio_features.get('speech_rate', 0)
            expected_rates = {
                'American': (4, 6),
                'British': (3, 5),
                'Australian': (4, 6),
                'Canadian': (4, 6),
                'Indian': (5, 8)
            }
            
            if accent_name in expected_rates:
                rate_range = expected_rates[accent_name]
                if rate_range[0] <= speech_rate <= rate_range[1]:
                    score += 15
                elif abs(speech_rate - np.mean(rate_range)) < 2:
                    score += 10
            max_score += 15
            
            # 5. Transcription analysis (20% weight)
            if transcription:
                text_score = self._analyze_text_patterns(accent_name, transcription)
                score += text_score * 0.2
            max_score += 20
            
            # Calculate percentage score
            final_score = (score / max_score * 100) if max_score > 0 else 0
            
            # Apply audio quality weighting
            quality_factor = min(1.0, audio_features.get('duration', 0) / 30)  # Longer audio = better confidence
            final_score *= quality_factor
            
            return min(100, max(0, final_score))
            
        except Exception:
            return 0.0
    
    def _analyze_text_patterns(self, accent_name: str, transcription: str) -> float:
        """Analyze text patterns specific to accent types"""
        try:
            text_lower = transcription.lower()
            score = 0.0
            
            # Keyword analysis
            accent_keywords = self.accent_features[accent_name]['keywords']
            keyword_matches = sum(1 for keyword in accent_keywords if keyword in text_lower)
            score += keyword_matches * 5
            
            # Specific pattern analysis
            if accent_name == 'American':
                # American patterns
                if re.search(r'\bcan\'t\b', text_lower):
                    if 'can\'t' in text_lower:  # Simplified pronunciation check
                        score += 10
                
            elif accent_name == 'British':
                # British patterns
                british_words = ['whilst', 'amongst', 'colour', 'favour', 'realise']
                british_matches = sum(1 for word in british_words if word in text_lower)
                score += british_matches * 8
                
            elif accent_name == 'Australian':
                # Australian patterns
                aussie_words = ['mate', 'bloke', 'sheila', 'fair dinkum']
                aussie_matches = sum(1 for word in aussie_words if word in text_lower)
                score += aussie_matches * 10
                
            elif accent_name == 'Canadian':
                # Canadian patterns
                canadian_words = ['eh', 'aboot', 'hoose', 'oot']
                canadian_matches = sum(1 for word in canadian_words if word in text_lower)
                score += canadian_matches * 10
                
            elif accent_name == 'Indian':
                # Indian English patterns
                indian_patterns = ['very good', 'only', 'what is your good name', 'please do the needful']
                indian_matches = sum(1 for pattern in indian_patterns if pattern in text_lower)
                score += indian_matches * 8
            
            return min(100, score)
            
        except Exception:
            return 0.0
    
    def _calculate_english_proficiency(self, audio_features: Dict, transcription: str) -> float:
        """Calculate overall English proficiency score"""
        try:
            proficiency = 0.0
            
            # 1. Speech clarity (based on audio features)
            clarity_score = 0
            
            # Clear speech indicators
            if audio_features.get('rms_mean', 0) > 0.01:  # Good volume
                clarity_score += 20
            
            if 0.3 < audio_features.get('zcr_mean', 0) < 0.7:  # Good articulation
                clarity_score += 20
            
            if audio_features.get('spectral_centroid_mean', 0) > 1000:  # Clear consonants
                clarity_score += 15
            
            proficiency += clarity_score * 0.4  # 40% weight
            
            # 2. Speech fluency
            fluency_score = 0
            
            speech_rate = audio_features.get('speech_rate', 0)
            if 3 <= speech_rate <= 7:  # Normal speech rate
                fluency_score += 25
            
            tempo = audio_features.get('tempo', 0)
            if 120 <= tempo <= 200:  # Good tempo
                fluency_score += 15
            
            proficiency += fluency_score * 0.3  # 30% weight
            
            # 3. Vocabulary and grammar (from transcription)
            language_score = 0
            
            if transcription:
                word_count = len(transcription.split())
                if word_count > 10:  # Sufficient content
                    language_score += 20
                
                # Check for complete sentences
                sentence_count = len([s for s in transcription.split('.') if s.strip()])
                if sentence_count > 0:
                    language_score += 10
                
                # Vocabulary diversity
                unique_words = len(set(transcription.lower().split()))
                if unique_words > word_count * 0.7:  # Good vocabulary diversity
                    language_score += 10
            
            proficiency += language_score * 0.3  # 30% weight
            
            return min(100, max(0, proficiency))
            
        except Exception:
            return 50.0  # Default medium proficiency
    
    def _generate_summary(self, accent: str, confidence: float, transcription: str, audio_features: Dict) -> str:
        """Generate a human-readable summary of the analysis"""
        try:
            summary_parts = []
            
            # Accent classification
            if confidence >= 80:
                summary_parts.append(f"Strong indicators of {accent} English accent detected.")
            elif confidence >= 60:
                summary_parts.append(f"Moderate indicators of {accent} English accent detected.")
            elif confidence >= 40:
                summary_parts.append(f"Some characteristics of {accent} English accent present.")
            else:
                summary_parts.append(f"Accent classification uncertain. Possible {accent} influence.")
            
            # Audio quality assessment
            duration = audio_features.get('duration', 0)
            if duration < 10:
                summary_parts.append("Short audio sample may limit accuracy.")
            elif duration > 60:
                summary_parts.append("Long audio sample provides good analysis depth.")
            
            # Speech characteristics
            speech_rate = audio_features.get('speech_rate', 0)
            if speech_rate > 6:
                summary_parts.append("Fast speaking pace observed.")
            elif speech_rate < 3:
                summary_parts.append("Slow speaking pace observed.")
            else:
                summary_parts.append("Normal speaking pace.")
            
            # Clarity assessment
            if audio_features.get('rms_mean', 0) > 0.05:
                summary_parts.append("Clear audio quality.")
            elif audio_features.get('rms_mean', 0) < 0.01:
                summary_parts.append("Audio quality may affect accuracy.")
            
            # Transcription quality
            if transcription and len(transcription.split()) > 20:
                summary_parts.append("Sufficient speech content for reliable analysis.")
            elif transcription:
                summary_parts.append("Limited speech content detected.")
            else:
                summary_parts.append("Speech transcription unavailable - analysis based on audio features only.")
            
            return " ".join(summary_parts)
            
        except Exception:
            return "Analysis completed with limited information available."
