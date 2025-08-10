
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import yt_dlp
import os
import uuid
import threading
import time
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
import functools

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'mp3'}
MAX_FILE_AGE_HOURS = 24  # Files will be deleted after 24 hours

# Development mode - set to True for local testing
DEVELOPMENT_MODE = True

# RapidAPI Configuration
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', 'your-rapidapi-key')
RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST', 'youtube-to-mp3-converter.p.rapidapi.com')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store download status
download_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Remove files older than MAX_FILE_AGE_HOURS"""
    current_time = datetime.now()
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            if current_time - file_time > timedelta(hours=MAX_FILE_AGE_HOURS):
                try:
                    os.remove(filepath)
                    print(f"Cleaned up old file: {filename}")
                except Exception as e:
                    print(f"Error cleaning up {filename}: {e}")

def validate_rapidapi_request(f):
    """Decorator to validate RapidAPI requests"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for RapidAPI headers
        rapidapi_key = request.headers.get('X-RapidAPI-Key')
        rapidapi_host = request.headers.get('X-RapidAPI-Host')
        
        # For development mode, allow requests without RapidAPI headers
        if DEVELOPMENT_MODE or os.environ.get('FLASK_ENV') == 'development':
            return f(*args, **kwargs)
        
        # For production, validate RapidAPI headers
        if not rapidapi_key or not rapidapi_host:
            return jsonify({
                'error': 'Missing RapidAPI headers',
                'message': 'X-RapidAPI-Key and X-RapidAPI-Host headers are required'
            }), 401
        
        # Optional: Validate the API key (you can add your own validation logic)
        if rapidapi_key != RAPIDAPI_KEY:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided RapidAPI key is not valid'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def download_and_convert(video_url, task_id):
    """Download and convert YouTube video to MP3"""
    try:
        download_status[task_id] = {'status': 'downloading', 'progress': 0}
        
        # Extract video info
        with yt_dlp.YoutubeDL() as ydl:
            video_info = ydl.extract_info(url=video_url, download=False)
        
        video_title = video_info['title']
        # Clean filename for filesystem
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}_{task_id}.mp3"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        download_status[task_id] = {'status': 'converting', 'progress': 50}
        
        # Download and convert options - use a temporary filename to avoid double extensions
        temp_filename = f"{safe_title}_{task_id}"
        temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        
        options = {
            'quiet': True,
            'noplaylist': True,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': temp_filepath,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        
        # Download and convert
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        
        # Check if file was created successfully and rename to correct filename
        actual_filepath = None
        
        # Look for the converted file (it might have .mp3 extension added by yt-dlp)
        possible_paths = [
            temp_filepath + '.mp3',  # yt-dlp adds .mp3 extension
            temp_filepath,           # original path
            filepath                 # target path
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                actual_filepath = path
                break
        
        # If no file found, check for any file with the task_id in the name
        if not actual_filepath:
            for filename_in_dir in os.listdir(UPLOAD_FOLDER):
                if task_id in filename_in_dir and filename_in_dir.endswith('.mp3'):
                    actual_filepath = os.path.join(UPLOAD_FOLDER, filename_in_dir)
                    break
        
        if actual_filepath and actual_filepath != filepath:
            # Rename to the correct filename
            try:
                os.rename(actual_filepath, filepath)
            except Exception as e:
                # If rename fails, copy the file
                import shutil
                shutil.copy2(actual_filepath, filepath)
                os.remove(actual_filepath)
        
        if os.path.exists(filepath):
            # Get file size
            file_size = os.path.getsize(filepath)
            
            download_status[task_id] = {
                'status': 'completed',
                'progress': 100,
                'filename': filename,
                'title': video_title,
                'download_url': f'/api/download/{filename}',
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'duration': video_info.get('duration', 0),
                'thumbnail': video_info.get('thumbnail', ''),
                'uploader': video_info.get('uploader', ''),
                'upload_date': video_info.get('upload_date', ''),
                'view_count': video_info.get('view_count', 0)
            }
        else:
            # List files in directory for debugging
            files_in_dir = os.listdir(UPLOAD_FOLDER)
            download_status[task_id] = {
                'status': 'error', 
                'message': f'File conversion failed - file not found. Files in directory: {files_in_dir}'
            }
            
    except Exception as e:
        download_status[task_id] = {'status': 'error', 'message': str(e)}

@app.route('/api/convert', methods=['POST'])
@validate_rapidapi_request
def convert_video():
    """Convert YouTube video to MP3 - RapidAPI compatible"""
    try:
        # Support both JSON and form data
        if request.is_json:
            data = request.get_json()
            video_url = data.get('url')
            quality = data.get('quality', '192')
            format_type = data.get('format', 'mp3')
        else:
            video_url = request.form.get('url')
            quality = request.form.get('quality', '192')
            format_type = request.form.get('format', 'mp3')
        
        if not video_url:
            return jsonify({
                'error': 'Missing required parameter',
                'message': 'URL parameter is required',
                'parameters': {
                    'url': 'YouTube video URL (required)',
                    'quality': 'Audio quality in kbps (optional, default: 192)',
                    'format': 'Output format (optional, default: mp3)'
                }
            }), 400
        
        # Validate URL format
        if not video_url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            return jsonify({
                'error': 'Invalid URL format',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Start download in background thread
        thread = threading.Thread(target=download_and_convert, args=(video_url, task_id))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'started',
            'message': 'Conversion started successfully',
            'api_info': {
                'provider': 'RapidAPI' if not DEVELOPMENT_MODE else 'Development',
                'endpoint': '/api/convert',
                'usage': 'Use the task_id to check status at /api/status/{task_id}'
            }
        }), 202
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/status/<task_id>', methods=['GET'])
@validate_rapidapi_request
def get_status(task_id):
    """Get download status - RapidAPI compatible"""
    if task_id not in download_status:
        return jsonify({
            'error': 'Task not found',
            'message': f'No task found with ID: {task_id}',
            'task_id': task_id
        }), 404
    
    status_data = download_status[task_id].copy()
    
    # Add RapidAPI specific response format
    response = {
        'success': status_data.get('status') != 'error',
        'task_id': task_id,
        'data': status_data
    }
    
    return jsonify(response)

@app.route('/api/download/<filename>', methods=['GET'])
@validate_rapidapi_request
def download_file(filename):
    """Download the converted MP3 file - RapidAPI compatible"""
    if not allowed_file(filename):
        return jsonify({
            'error': 'Invalid file type',
            'message': 'Only MP3 files are allowed for download'
        }), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({
            'error': 'File not found',
            'message': f'File {filename} not found or has expired'
        }), 404
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'YouTube to MP3 Converter API',
        'version': '1.0.0',
        'rapidapi_compatible': True,
        'development_mode': DEVELOPMENT_MODE
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information and documentation"""
    return jsonify({
        'success': True,
        'api_info': {
            'name': 'YouTube to MP3 Converter API',
            'version': '1.0.0',
            'provider': 'RapidAPI',
            'description': 'Convert YouTube videos to MP3 format with high quality audio extraction',
            'development_mode': DEVELOPMENT_MODE
        },
        'endpoints': {
            'POST /api/convert': {
                'description': 'Convert YouTube video to MP3',
                'parameters': {
                    'url': {
                        'type': 'string',
                        'required': True,
                        'description': 'YouTube video URL'
                    },
                    'quality': {
                        'type': 'string',
                        'required': False,
                        'default': '192',
                        'description': 'Audio quality in kbps (128, 192, 320)'
                    },
                    'format': {
                        'type': 'string',
                        'required': False,
                        'default': 'mp3',
                        'description': 'Output format (mp3)'
                    }
                },
                'headers': {
                    'X-RapidAPI-Key': 'Your RapidAPI key (not required in development mode)',
                    'X-RapidAPI-Host': 'youtube-to-mp3-converter.p.rapidapi.com (not required in development mode)',
                    'Content-Type': 'application/json'
                }
            },
            'GET /api/status/{task_id}': {
                'description': 'Check conversion status',
                'parameters': {
                    'task_id': {
                        'type': 'string',
                        'required': True,
                        'description': 'Task ID returned from convert endpoint'
                    }
                }
            },
            'GET /api/download/{filename}': {
                'description': 'Download converted file',
                'parameters': {
                    'filename': {
                        'type': 'string',
                        'required': True,
                        'description': 'Filename returned from status endpoint'
                    }
                }
            }
        },
        'usage_examples': {
            'convert_video': {
                'curl': 'curl -X POST "https://your-api-url.com/api/convert" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}\'',
                'javascript': 'const response = await fetch("https://your-api-url.com/api/convert", {\n  method: "POST",\n  headers: {\n    "Content-Type": "application/json"\n  },\n  body: JSON.stringify({\n    url: "https://www.youtube.com/watch?v=VIDEO_ID"\n  })\n});'
            }
        }
    })

@app.route('/web', methods=['GET'])
def web_interface():
    """Serve the web interface"""
    try:
        with open('static/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return jsonify({'error': 'Web interface not found'}), 404

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'YouTube to MP3 Converter API',
        'version': '1.0.0',
        'rapidapi_compatible': True,
        'development_mode': DEVELOPMENT_MODE,
        'endpoints': {
            'POST /api/convert': 'Convert YouTube video to MP3',
            'GET /api/status/<task_id>': 'Get conversion status',
            'GET /api/download/<filename>': 'Download converted file',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information and documentation',
            'GET /web': 'Web interface'
        },
        'rapidapi_headers': {
            'X-RapidAPI-Key': 'Your RapidAPI key (not required in development mode)',
            'X-RapidAPI-Host': 'youtube-to-mp3-converter.p.rapidapi.com (not required in development mode)'
        }
    })

if __name__ == '__main__':
    # Clean up old files on startup
    cleanup_old_files()
    
    # Get port from environment variable (for Railway deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
