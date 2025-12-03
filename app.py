from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import yt_dlp
import os
import threading
import uuid
import json
import tempfile
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store download progress in memory (simpler and more reliable)
download_progress = {}

# Create a temp directory for progress files as backup
PROGRESS_DIR = os.path.join(tempfile.gettempdir(), 'youtube_downloader_progress')
os.makedirs(PROGRESS_DIR, exist_ok=True)

def save_progress(download_id, progress):
    """Save progress both in memory and to file"""
    download_progress[download_id] = progress
    try:
        progress_file = os.path.join(PROGRESS_DIR, f"{download_id}.json")
        with open(progress_file, 'w') as f:
            json.dump(progress, f)
    except Exception as e:
        print(f"Error saving progress to file: {e}")

def get_progress_from_file(download_id):
    """Get progress from memory first, then file"""
    # Try memory first
    if download_id in download_progress:
        return download_progress[download_id]
    
    # Fallback to file
    progress_file = os.path.join(PROGRESS_DIR, f"{download_id}.json")
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)
                download_progress[download_id] = progress  # Cache in memory
                return progress
        except Exception as e:
            print(f"Error reading progress: {e}")
            return {'status': 'error', 'message': f'Failed to read progress: {str(e)}'}
    
    return {'status': 'not_found'}

def download_video(url, download_id):
    try:
        # Update status to processing
        save_progress(download_id, {'status': 'processing', 'message': 'Extracting video info...'})
        
        # Set download location - use app's downloads directory for deployment
        download_path = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(download_path, exist_ok=True)
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Clean up the progress strings
                percent = str(d.get('_percent_str', '0%')).strip()
                speed = str(d.get('_speed_str', '0KB/s')).strip()
                eta = str(d.get('_eta_str', 'Unknown')).strip()
                
                # Remove any ANSI color codes
                import re
                percent = re.sub(r'\x1b\[[0-9;]*m', '', percent)
                speed = re.sub(r'\x1b\[[0-9;]*m', '', speed)
                eta = re.sub(r'\x1b\[[0-9;]*m', '', eta)
                
                progress = {
                    'status': 'downloading',
                    'percent': percent,
                    'speed': speed,
                    'eta': eta
                }
                save_progress(download_id, progress)
            elif d['status'] == 'finished':
                # Get just the filename without full path for security
                filename = os.path.basename(d['filename'])
                progress = {
                    'status': 'finished',
                    'filename': filename,
                    'download_url': f'/download_file/{download_id}/{filename}'
                }
                save_progress(download_id, progress)

        # SAFE options that never require FFmpeg - exactly like your working code
        ydl_opts = {
            # This format string ONLY selects pre-merged MP4 files
            'format': 'b[ext=mp4]',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
            # Absolutely prevent any merging
            'nopostoverwrites': True,
            'prefer_free_formats': False,
            # Aggressive anti-bot bypass for production
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            # Use Android client to bypass bot detection
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator'],
                    'player_skip': ['webpage', 'configs'],
                    'skip': ['hls', 'dash', 'translated_subs']
                }
            },
            # Additional bypass options
            'nocheckcertificate': True,
            'age_limit': None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First check available formats
            save_progress(download_id, {'status': 'processing', 'message': 'Analyzing video formats...'})
            info = ydl.extract_info(url, download=False)
            
            # Find all pre-merged MP4 formats - exactly like your working code
            mp4_formats = [f for f in info.get('formats', [])
                          if f.get('ext') == 'mp4'
                          and f.get('vcodec') != 'none'
                          and f.get('acodec') != 'none']
            
            if not mp4_formats:
                raise Exception("No pre-merged MP4 format available for this video. Try a different video.")
            
            # Prioritize progressive (non-fragmented) formats for better compatibility
            # These formats work in all media players without conversion
            progressive_formats = []
            for f in mp4_formats:
                # Check if it's a progressive download (not DASH/fragmented)
                protocol = f.get('protocol', '')
                format_note = str(f.get('format_note', '')).lower()
                
                # Progressive formats have 'https' or 'http' protocol and are not DASH
                if (protocol in ['https', 'http'] and 
                    'dash' not in protocol and 
                    'hls' not in protocol and
                    f.get('acodec') != 'none' and
                    f.get('vcodec') != 'none'):
                    progressive_formats.append(f)
            
            # If we found progressive formats, use them (they work in all players)
            if progressive_formats:
                best_format = max(progressive_formats, key=lambda x: x.get('height', 0))
                print(f"Selected progressive format (compatible with all players)")
            else:
                # Fall back to any pre-merged format
                best_format = max(mp4_formats, key=lambda x: x.get('height', 0))
                print(f"No progressive format found, using fragmented format (may need VLC)")
            
            # Store video info with correct resolution
            save_progress(download_id, {
                'status': 'starting',
                'title': info['title'],
                'duration': f"{info['duration'] // 60} minutes" if info.get('duration') else "Unknown",
                'resolution': f"{best_format.get('height', 'unknown')}p MP4 (pre-merged)",
                'message': 'Starting download...'
            })
            
            # Debug: Print format details
            print(f"Available MP4 formats: {len(mp4_formats)}")
            print(f"Selected format: {best_format['format_id']} - {best_format.get('height')}p - vcodec: {best_format.get('vcodec')} - acodec: {best_format.get('acodec')}")
            
            # Force download this specific format
            ydl.params['format'] = str(best_format['format_id'])
            ydl.download([url])
            
            # Find the actual downloaded file
            import glob
            mp4_files = glob.glob(os.path.join(download_path, "*.mp4"))
            if not mp4_files:
                print("No MP4 file found after download")
                return True
            
            # Get the most recently modified file
            downloaded_file = max(mp4_files, key=os.path.getmtime)
            print(f"Downloaded file: {downloaded_file}")
            
            # Video downloaded successfully
            print(f"✅ Download complete: {downloaded_file}")
            print("Note: If video doesn't play in Windows Media Player, use VLC Player or convert with convert_video.py")
            
        return True
        
    except Exception as e:
        progress = {
            'status': 'error',
            'message': str(e)
        }
        save_progress(download_id, progress)
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def start_download():
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Generate unique download ID
    download_id = str(uuid.uuid4())
    
    # Initialize progress immediately
    initial_progress = {
        'status': 'initializing',
        'message': 'Starting download...'
    }
    save_progress(download_id, initial_progress)
    
    # Start download in background thread
    thread = threading.Thread(target=download_video, args=(url, download_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id})

@app.route('/progress/<download_id>')
def get_progress(download_id):
    progress = get_progress_from_file(download_id)
    return jsonify(progress)

@app.route('/download_file/<download_id>/<filename>')
def download_file(download_id, filename):
    """Serve downloaded files"""
    try:
        download_path = os.path.join(os.getcwd(), 'downloads')
        file_path = os.path.join(download_path, filename)
        
        # Security check - ensure file exists and is in downloads directory
        if os.path.exists(file_path) and os.path.commonpath([download_path, file_path]) == download_path:
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use environment variables for deployment flexibility
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)