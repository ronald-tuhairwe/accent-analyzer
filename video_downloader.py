import os
import tempfile
import yt_dlp
from pathlib import Path

class VideoDownloader:
    """Handles downloading videos from various sources"""
    
    def __init__(self):
        self.supported_sites = [
            'youtube.com', 'youtu.be', 'loom.com', 'vimeo.com',
            'dailymotion.com', 'streamable.com'
        ]
    
    def download_video(self, url, output_dir):
        """
        Download video from URL and return the local file path
        
        Args:
            url (str): Video URL
            output_dir (str): Directory to save the video
            
        Returns:
            str: Path to downloaded video file or None if failed
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best[height<=720]/best',  # Limit to 720p for faster processing
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': False,
                'no_warnings': False,
                'extractaudio': False,
                'audioformat': 'wav',
                'quiet': True,
                'no_color': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    raise Exception("Could not extract video information")
                
                # Check duration (limit to reasonable length)
                duration = info.get('duration', 0)
                if duration > 1800:  # 30 minutes max
                    raise Exception("Video is too long (max 30 minutes allowed)")
                
                # Download the video
                ydl.download([url])
                
                # Find the downloaded file
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                
                # Clean filename for filesystem
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                expected_path = os.path.join(output_dir, f"{safe_title}.{ext}")
                
                # Look for any video file in the directory if exact match not found
                if not os.path.exists(expected_path):
                    video_files = []
                    for file in os.listdir(output_dir):
                        if file.lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov')):
                            video_files.append(os.path.join(output_dir, file))
                    
                    if video_files:
                        expected_path = video_files[0]
                    else:
                        raise Exception("Downloaded video file not found")
                
                return expected_path
                
        except yt_dlp.DownloadError as e:
            raise Exception(f"Download failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Video download error: {str(e)}")
    
    def is_supported_url(self, url):
        """Check if URL is from a supported video platform"""
        url_lower = url.lower()
        return any(site in url_lower for site in self.supported_sites)
    
    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'no_color': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown')
                }
                
        except Exception as e:
            raise Exception(f"Could not get video info: {str(e)}")
