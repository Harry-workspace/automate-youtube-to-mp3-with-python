# YouTube to MP3 Converter

A simple Python application to download YouTube videos and convert them to MP3 format. Available as both a command-line tool and a REST API with RapidAPI compatibility.

## Features

- Download YouTube videos and convert to MP3
- Modern implementation using `yt-dlp` (actively maintained)
- Automatic directory creation
- Default save location: `D:\Downloads`
- Cross-platform compatibility
- **NEW**: REST API with web download URLs
- **NEW**: Railway deployment ready
- **NEW**: RapidAPI compatibility with authentication
- **NEW**: Enhanced video metadata extraction
- **NEW**: Configurable audio quality settings

## Prerequisites

1. **FFmpeg**: Ensure that [`ffmpeg`](https://ffmpeg.org/download.html#releases) is installed on your machine. See guide [here](https://video.stackexchange.com/questions/20495/how-do-i-set-up-and-use-ffmpeg-in-windows).
2. **Python**: Python 3.7 or higher

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/imdadahad/automate-youtube-to-mp3-with-python.git
   cd automate-youtube-to-mp3-with-python
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

1. Run the application:
   ```bash
   python run.py
   ```

2. Enter the YouTube video URL when prompted

3. Enter the directory where you want to save the MP3 file, or leave empty to save in `D:\Downloads`

### REST API

The API provides endpoints for converting YouTube videos to MP3 and returning download URLs.

#### Start the API Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

##### 1. Convert YouTube Video to MP3
```http
POST /api/convert
Content-Type: application/json
X-RapidAPI-Key: YOUR_API_KEY
X-RapidAPI-Host: your-api-host.rapidapi.com

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "quality": "192",
  "format": "mp3"
}
```

**Response:**
```json
{
  "success": true,
  "task_id": "unique-task-id",
  "status": "started",
  "message": "Conversion started successfully",
  "api_info": {
    "provider": "RapidAPI",
    "endpoint": "/api/convert",
    "usage": "Use the task_id to check status at /api/status/{task_id}"
  }
}
```

##### 2. Check Conversion Status
```http
GET /api/status/{task_id}
X-RapidAPI-Key: YOUR_API_KEY
X-RapidAPI-Host: your-api-host.rapidapi.com
```

**Response:**
```json
{
  "success": true,
  "task_id": "unique-task-id",
  "data": {
    "status": "completed",
    "progress": 100,
    "filename": "video_title_task_id.mp3",
    "title": "Video Title",
    "download_url": "/api/download/video_title_task_id.mp3",
    "file_size_mb": 3.45,
    "duration": 212,
    "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg",
    "uploader": "Channel Name",
    "view_count": 1000000
  }
}
```

##### 3. Download Converted File
```http
GET /api/download/{filename}
X-RapidAPI-Key: YOUR_API_KEY
X-RapidAPI-Host: your-api-host.rapidapi.com
```

Returns the MP3 file as a downloadable attachment.

##### 4. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "YouTube to MP3 Converter API",
  "version": "1.0.0",
  "rapidapi_compatible": true
}
```

##### 5. API Information
```http
GET /api/info
```

Returns complete API documentation and usage examples.

##### 6. Web Interface
```http
GET /web
```

Interactive web interface for converting videos.

#### Example Usage with curl

```bash
# Convert a video
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'

# Check status
curl http://localhost:5000/api/status/{task_id} \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com"

# Download the file
curl -O http://localhost:5000/api/download/{filename} \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com"
```

## Deployment Options

### Railway Deployment

This project is ready for deployment on Railway. The API will automatically handle:

- Background video processing
- File cleanup (files deleted after 24 hours)
- CORS support for web applications
- Health checks for monitoring

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Railway deployment instructions.**

### RapidAPI Deployment

Deploy your API on RapidAPI platform to monetize it and reach a global audience.

**See [RAPIDAPI_DEPLOYMENT.md](RAPIDAPI_DEPLOYMENT.md) for detailed RapidAPI deployment instructions.**

#### RapidAPI Features

- **Authentication**: Built-in API key validation
- **Rate Limiting**: Configurable usage limits
- **Monetization**: Set up pricing plans
- **Analytics**: Track usage and revenue
- **Documentation**: Automatic API documentation

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## What's Changed

This project has been modernized from the original:
- **Updated from `youtube_dl` to `yt-dlp`**: More reliable and actively maintained
- **Default save location**: Now defaults to `D:\Downloads` instead of current directory
- **Automatic directory creation**: Creates the target directory if it doesn't exist
- **Better error handling**: More robust video processing
- **NEW**: REST API with async processing
- **NEW**: Railway deployment configuration
- **NEW**: File cleanup and management
- **NEW**: CORS support for web applications
- **NEW**: RapidAPI compatibility with authentication
- **NEW**: Enhanced video metadata extraction
- **NEW**: Configurable audio quality settings
- **NEW**: Comprehensive API documentation
- **NEW**: OpenAPI specification for RapidAPI

## API Parameters

### Convert Endpoint Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes | - | YouTube video URL |
| `quality` | string | No | "192" | Audio quality (128, 192, 320 kbps) |
| `format` | string | No | "mp3" | Output format (mp3) |

### Response Data

When conversion is completed, the status endpoint returns:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Conversion status (downloading, converting, completed, error) |
| `progress` | integer | Progress percentage (0-100) |
| `title` | string | Video title |
| `filename` | string | Generated filename |
| `download_url` | string | Download endpoint URL |
| `file_size_mb` | number | File size in MB |
| `duration` | integer | Video duration in seconds |
| `thumbnail` | string | Video thumbnail URL |
| `uploader` | string | Channel name |
| `view_count` | integer | View count |

## ⚠ Disclaimer

This app is intended for educational purposes only. Please respect copyright laws and only download content you have permission to use.

## Original Project

This is based on the original project by [Imdad Ahad](https://github.com/imdadahad/automate-youtube-to-mp3-with-python) for educational purposes.
