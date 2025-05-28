import streamlit as st
import os
import tempfile
import time
from video_downloader import VideoDownloader
from audio_processor import AudioProcessor
from accent_analyzer import AccentAnalyzer

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Accent Analysis Tool</h1>
        <h3>AI-Powered English Accent Classification for Hiring Evaluation</h3>
        <p>Upload video content and get detailed accent analysis with confidence scoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # Enhanced sidebar with better styling
    with st.sidebar:
        st.markdown("""
        <div class="feature-card">
            <h2>🌟 Supported Features</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📹 Video Sources</h4>
            <ul>
                <li>YouTube URLs</li>
                <li>Loom recordings</li>
                <li>Direct MP4/video links</li>
                <li>Public video URLs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>🗣️ Accent Classifications</h4>
            <ul>
                <li>🇺🇸 American English</li>
                <li>🇬🇧 British English</li>
                <li>🇦🇺 Australian English</li>
                <li>🇨🇦 Canadian English</li>
                <li>🇮🇳 Indian English</li>
                <li>🌍 Other English variants</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📊 Analysis Output</h4>
            <ul>
                <li>Accent classification</li>
                <li>Confidence score (0-100%)</li>
                <li>English proficiency rating</li>
                <li>Detailed analysis summary</li>
                <li>Downloadable report</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main interface with enhanced styling
    st.markdown("""
    <div class="feature-card">
        <h2>🔗 Video URL Input</h2>
        <p>Enter a public video URL containing English speech for analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    video_url = st.text_input(
        "Enter video URL:",
        placeholder="https://www.youtube.com/watch?v=... or https://www.loom.com/share/...",
        help="Paste a public video URL that contains English speech"
    )
    
    # Processing options in styled containers
    st.markdown("""
    <div class="feature-card">
        <h3>⚙️ Processing Options</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        max_duration = st.number_input(
            "⏱️ Max duration (minutes):",
            min_value=1,
            max_value=10,
            value=5,
            help="Limit processing time for long videos"
        )
    
    with col2:
        sample_rate = st.selectbox(
            "🎵 Audio quality:",
            options=[16000, 22050, 44100],
            index=1,
            help="Higher rates provide better quality but slower processing",
            format_func=lambda x: f"{x} Hz {'(Standard)' if x == 22050 else '(High Quality)' if x == 44100 else '(Fast)'}"
        )
    
    # Enhanced analysis button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button(
        "🚀 Start Accent Analysis",
        disabled=not video_url or st.session_state.processing,
        type="primary",
        use_container_width=True
    )
    
    # Process video when button is clicked
    if analyze_button and video_url:
        st.session_state.processing = True
        st.session_state.analysis_result = None
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize processors
            downloader = VideoDownloader()
            audio_processor = AudioProcessor(sample_rate=sample_rate)
            analyzer = AccentAnalyzer()
            
            # Step 1: Download video
            status_text.text("📥 Downloading video...")
            progress_bar.progress(20)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                video_path = downloader.download_video(video_url, temp_dir)
                
                if not video_path:
                    st.error("❌ Failed to download video. Please check the URL and try again.")
                    st.session_state.processing = False
                    return
                
                # Step 2: Extract audio
                status_text.text("🎵 Extracting audio...")
                progress_bar.progress(40)
                
                audio_path = audio_processor.extract_audio(video_path, max_duration * 60)
                
                if not audio_path:
                    st.error("❌ Failed to extract audio from video.")
                    st.session_state.processing = False
                    return
                
                # Step 3: Process audio features
                status_text.text("🔊 Processing audio features...")
                progress_bar.progress(60)
                
                audio_features = audio_processor.extract_features(audio_path)
                
                # Step 4: Analyze accent
                status_text.text("🎯 Analyzing accent...")
                progress_bar.progress(80)
                
                analysis_result = analyzer.analyze_accent(audio_path, audio_features)
                
                # Complete
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Show success message
                st.markdown("""
                <div class="success-message">
                    <h3>🎉 Analysis Complete!</h3>
                    <p>Your accent analysis has been successfully processed. Check the results below.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.analysis_result = analysis_result
                
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.error("Please check your internet connection and try again with a different video.")
        
        finally:
            st.session_state.processing = False
            time.sleep(1)
            st.rerun()
    
    # Display results
    if st.session_state.analysis_result:
        display_results(st.session_state.analysis_result)

def display_results(result):
    """Display analysis results in a formatted way"""
    st.markdown("""
    <div class="feature-card">
        <h1>📊 Analysis Results</h1>
        <p>Detailed breakdown of your accent classification analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metrics with custom styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        accent = result['accent']
        flag_map = {
            'American': '🇺🇸',
            'British': '🇬🇧', 
            'Australian': '🇦🇺',
            'Canadian': '🇨🇦',
            'Indian': '🇮🇳'
        }
        flag = flag_map.get(accent, '🌍')
        
        st.markdown(f"""
        <div class="metric-container">
            <h2>{flag}</h2>
            <h3>Detected Accent</h3>
            <h2>{accent} English</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence = result['confidence']
        confidence_color = "#56ab2f" if confidence >= 80 else "#ff7675" if confidence < 60 else "#fdcb6e"
        
        st.markdown(f"""
        <div class="metric-container" style="background: linear-gradient(135deg, {confidence_color} 0%, {confidence_color}aa 100%);">
            <h2>📈</h2>
            <h3>Confidence Score</h3>
            <h2>{confidence:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        english_score = result.get('english_proficiency', 0)
        proficiency_color = "#00b894" if english_score >= 80 else "#e17055" if english_score < 60 else "#fdcb6e"
        
        st.markdown(f"""
        <div class="metric-container" style="background: linear-gradient(135deg, {proficiency_color} 0%, {proficiency_color}aa 100%);">
            <h2>🎯</h2>
            <h3>English Proficiency</h3>
            <h2>{english_score:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed analysis with enhanced styling
    st.markdown("""
    <div class="feature-card">
        <h2>🔍 Detailed Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Confidence level interpretation with enhanced styling
    if confidence >= 80:
        confidence_level = "High"
        confidence_bg = "#00b894"
        confidence_icon = "🟢"
    elif confidence >= 60:
        confidence_level = "Medium"
        confidence_bg = "#fdcb6e"
        confidence_icon = "🟡"
    else:
        confidence_level = "Low"
        confidence_bg = "#e17055"
        confidence_icon = "🔴"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {confidence_bg} 0%, {confidence_bg}aa 100%); 
                padding: 1rem; border-radius: 8px; color: white; margin: 1rem 0;">
        <h3>{confidence_icon} Confidence Level: {confidence_level}</h3>
        <p>Classification reliability based on audio analysis and speech patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary with enhanced styling
    if 'summary' in result:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Analysis Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;'>{result['summary']}</div>", unsafe_allow_html=True)
    
    # Technical details with enhanced styling
    with st.expander("🔧 Technical Details & Metrics"):
        technical_details = result.get('technical_details', {})
        
        # Create a formatted display of technical details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Audio Analysis:**")
            st.write(f"• Duration: {technical_details.get('audio_duration', 0):.1f} seconds")
            st.write(f"• Speech Rate: {technical_details.get('speech_rate', 0):.1f} segments/sec")
            st.write(f"• Average Pitch: {technical_details.get('pitch_mean', 0):.1f} Hz")
            
        with col2:
            st.markdown("**Classification Scores:**")
            all_scores = technical_details.get('all_accent_scores', {})
            for accent, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                st.write(f"• {accent}: {score:.1f}%")
    
    # Download report with enhanced styling
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Download Report</h3>
        <p>Get a detailed PDF report of the accent analysis for your records</p>
    </div>
    """, unsafe_allow_html=True)
    
    report_data = generate_report(result)
    
    st.download_button(
        label="📥 Download Detailed Analysis Report",
        data=report_data,
        file_name=f"accent_analysis_{int(time.time())}.txt",
        mime="text/plain",
        use_container_width=True
    )

def generate_report(result):
    """Generate a downloadable text report"""
    report = f"""
ACCENT ANALYSIS REPORT
=====================

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

RESULTS SUMMARY
--------------
Detected Accent: {result['accent']}
Confidence Score: {result['confidence']:.1f}%
English Proficiency: {result.get('english_proficiency', 0):.1f}%

ANALYSIS DETAILS
---------------
{result.get('summary', 'No additional details available.')}

TECHNICAL INFORMATION
--------------------
"""
    
    for key, value in result.get('technical_details', {}).items():
        report += f"{key}: {value}\n"
    
    report += """
HIRING EVALUATION NOTES
----------------------
- High confidence scores (80%+) indicate reliable accent classification
- Medium confidence scores (60-79%) suggest accent may have mixed characteristics
- Low confidence scores (<60%) may indicate unclear audio or mixed accents
- Consider audio quality and speaking pace when interpreting results

This analysis is intended as a supplementary tool for hiring evaluation.
Final decisions should incorporate multiple assessment methods.
"""
    
    return report

if __name__ == "__main__":
    main()
