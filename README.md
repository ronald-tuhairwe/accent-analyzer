# Accent Analysis Tool

A professional AI-powered web application for analyzing English accents from video content, designed for hiring evaluation and language assessment.

## Features

- **Video Source Support**: YouTube, Loom, direct MP4 links, and other public video URLs
- **Accent Classification**: American, British, Australian, Canadian, and Indian English variants
- **Confidence Scoring**: 0-100% reliability rating for each classification
- **English Proficiency**: Overall speaking proficiency assessment
- **Professional Interface**: Modern, responsive design with gradient backgrounds and intuitive navigation
- **Detailed Reports**: Downloadable analysis reports for record-keeping

## Quick Deployment

### Option 1: Streamlit Cloud (I used this since it free)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd accent-analysis-tool

# Install dependencies
pip install -r deployment_requirements.txt

# Run the application
streamlit run app.py
```

The app is be available at `http://localhost:8501](https://accent-analyzer-by-ronald-tuhairwe.streamlit.app/`

## File Structure

```
accent-analysis-tool/
├── app.py                      # Main Streamlit application
├── video_downloader.py         # Video downloading functionality
├── audio_processor.py          # Audio feature extraction
├── accent_analyzer.py          # Accent classification logic
├── deployment_requirements.txt # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── README.md                  # This file
```

## Configuration

### Environment Variables (Optional)
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

### Streamlit Configuration
The app includes optimized settings in `.streamlit/config.toml` for:
- Professional color scheme
- Optimal server configuration
- Enhanced user experience

## Usage

1. **Enter Video URL**: Paste a public video URL containing English speech
2. **Set Processing Options**: 
   - Max duration (1-10 minutes)
   - Audio quality (16kHz, 22kHz, or 44kHz)
3. **Analyze**: Click "Start Accent Analysis" to begin processing
4. **Review Results**: View accent classification, confidence score, and proficiency rating
5. **Download Report**: Get a detailed analysis report for your records

## Technical Details

### Audio Processing
- Extracts audio using pydub and yt-dlp
- Analyzes MFCC features, spectral characteristics, and speech patterns
- Processes pitch, tempo, and rhythm patterns

### Accent Classification
- Rule-based classification system
- Analyzes multiple acoustic features
- Confidence scoring based on pattern matching

### Supported Platforms
- YouTube
- Loom
- Vimeo
- Direct video links (MP4, AVI, MOV, etc.)


## Security & Privacy

- Videos are processed temporarily and not stored
- Audio files are deleted after analysis
- No personal data is retained
- HTTPS encryption for all communications


  ## Now its remaining with training data for and then it cam perfect its categorize as more audios are tested 


## License

This project is ready for commercial use in hiring evaluation and language assessment applications.
