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

### Option 1: Streamlit Cloud (Recommended)
1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy directly from your repository
5. Your app will be live at `https://your-app-name.streamlit.app`

### Option 2: Heroku
1. Install Heroku CLI
2. Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
3. Deploy with: `git push heroku main`

### Option 3: Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Streamlit app
3. Deploy with one click

### Option 4: DigitalOcean App Platform
1. Connect your GitHub repository
2. Set build command: `pip install -r deployment_requirements.txt`
3. Set run command: `streamlit run app.py --server.port=8080 --server.address=0.0.0.0`

## Local Development

### Prerequisites
- Python 3.8+
- pip or conda

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

The app will be available at `http://localhost:8501`

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

## Cost Considerations

### Free Deployment Options
- **Streamlit Cloud**: Free tier available
- **Railway**: $5/month after free tier
- **Heroku**: Limited free tier

### Resource Requirements
- Memory: 512MB minimum, 1GB recommended
- CPU: Single core sufficient
- Storage: 1GB for dependencies

## Security & Privacy

- Videos are processed temporarily and not stored
- Audio files are deleted after analysis
- No personal data is retained
- HTTPS encryption for all communications

## Support

For deployment assistance or customization:
- Check the deployment platform's documentation
- Ensure all dependencies are correctly installed
- Verify that the port configuration matches your platform's requirements

## License

This project is ready for commercial use in hiring evaluation and language assessment applications.