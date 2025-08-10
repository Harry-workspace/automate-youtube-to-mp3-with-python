# Railway Deployment Guide

This guide will help you deploy the YouTube to MP3 Converter API to Railway.

## Prerequisites

1. A GitHub account
2. A Railway account (sign up at [railway.app](https://railway.app))
3. FFmpeg installed on Railway (handled automatically)

## Step 1: Prepare Your Repository

Make sure your repository contains all the necessary files:

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Railway deployment configuration
- `runtime.txt` - Python version specification
- `.gitignore` - Git ignore rules

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub

1. **Push to GitHub**: Ensure your code is pushed to a GitHub repository

2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Automatic Deployment**:
   - Railway will automatically detect the Python app
   - It will install dependencies from `requirements.txt`
   - The app will be deployed using the `Procfile`

### Option B: Deploy from Local Directory

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and Deploy**:
   ```bash
   railway init
   railway up
   ```

## Step 3: Configure Environment Variables

Railway will automatically set the `PORT` environment variable. No additional configuration is needed.

## Step 4: Access Your API

Once deployed, Railway will provide you with a URL like:
```
https://your-app-name.railway.app
```

### Test Your API

1. **Health Check**:
   ```bash
   curl https://your-app-name.railway.app/api/health
   ```

2. **API Documentation**:
   ```bash
   curl https://your-app-name.railway.app/
   ```

3. **Convert a Video**:
   ```bash
   curl -X POST https://your-app-name.railway.app/api/convert \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
   ```

## API Usage Examples

### JavaScript/Fetch

```javascript
// Convert a video
const response = await fetch('https://your-app-name.railway.app/api/convert', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID'
  })
});

const data = await response.json();
const taskId = data.task_id;

// Check status
const statusResponse = await fetch(`https://your-app-name.railway.app/api/status/${taskId}`);
const statusData = await statusResponse.json();

if (statusData.status === 'completed') {
  // Download the file
  window.open(`https://your-app-name.railway.app${statusData.download_url}`);
}
```

### Python/Requests

```python
import requests
import time

# Convert a video
response = requests.post('https://your-app-name.railway.app/api/convert', 
                        json={'url': 'https://www.youtube.com/watch?v=VIDEO_ID'})
data = response.json()
task_id = data['task_id']

# Poll for status
while True:
    status_response = requests.get(f'https://your-app-name.railway.app/api/status/{task_id}')
    status_data = status_response.json()
    
    if status_data['status'] == 'completed':
        download_url = f"https://your-app-name.railway.app{status_data['download_url']}"
        print(f"Download URL: {download_url}")
        break
    elif status_data['status'] == 'error':
        print(f"Error: {status_data['message']}")
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again
```

## Monitoring and Logs

- **View Logs**: In Railway dashboard, go to your project and click on "Deployments" to view logs
- **Health Monitoring**: Use the `/api/health` endpoint to monitor your API
- **File Cleanup**: Files are automatically deleted after 24 hours to save storage

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that `requirements.txt` is properly formatted
   - Ensure all dependencies are compatible

2. **Runtime Errors**:
   - Check Railway logs for error messages
   - Verify FFmpeg is available (should be automatic)

3. **CORS Issues**:
   - The API includes CORS headers for web applications
   - If you need specific origins, modify the CORS configuration in `app.py`

### Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- GitHub Issues: Create an issue in your repository

## Cost Considerations

- Railway offers a free tier with limited usage
- Monitor your usage in the Railway dashboard
- Consider upgrading for production use

## Security Notes

- The API is designed for educational purposes
- Files are automatically cleaned up after 24 hours
- Consider adding rate limiting for production use
- Always respect copyright laws when downloading content
