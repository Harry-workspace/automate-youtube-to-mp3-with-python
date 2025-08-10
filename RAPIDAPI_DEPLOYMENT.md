# RapidAPI Deployment Guide

This guide will help you deploy your YouTube to MP3 Converter API on RapidAPI platform.

## Prerequisites

1. **RapidAPI Account**: Sign up at [rapidapi.com](https://rapidapi.com)
2. **GitHub Repository**: Your API code should be in a GitHub repository
3. **Domain/Server**: You need a server to host your API (Railway, Heroku, AWS, etc.)

## Step 1: Deploy Your API

First, deploy your API to a hosting platform. We recommend Railway for simplicity:

### Deploy to Railway

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add RapidAPI compatibility"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub
   - Select your repository
   - Railway will automatically deploy

3. **Get Your API URL**:
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - This will be your API base URL

## Step 2: Create RapidAPI Account

1. **Sign Up**: Go to [rapidapi.com](https://rapidapi.com) and create an account
2. **Verify Email**: Complete email verification
3. **Add Payment Method**: Required for publishing APIs

## Step 3: Create New API on RapidAPI

1. **Go to RapidAPI Hub**:
   - Click "Add New API" or "Create API"
   - Choose "Create New API"

2. **Fill Basic Information**:
   ```
   API Name: YouTube to MP3 Converter
   Description: Convert YouTube videos to MP3 format with high quality audio extraction
   Category: Media & Entertainment
   Base URL: https://your-app-name.railway.app
   ```

3. **Upload OpenAPI Specification**:
   - Use the `rapidapi_config.json` file from this project
   - Or manually define your endpoints

## Step 4: Configure API Endpoints

### Endpoint 1: Convert Video
- **Path**: `/api/convert`
- **Method**: POST
- **Description**: Convert YouTube video to MP3
- **Parameters**:
  - `url` (required): YouTube video URL
  - `quality` (optional): Audio quality (128, 192, 320 kbps)
  - `format` (optional): Output format (mp3)

### Endpoint 2: Check Status
- **Path**: `/api/status/{task_id}`
- **Method**: GET
- **Description**: Check conversion status
- **Parameters**:
  - `task_id` (path): Task ID from convert endpoint

### Endpoint 3: Download File
- **Path**: `/api/download/{filename}`
- **Method**: GET
- **Description**: Download converted MP3 file
- **Parameters**:
  - `filename` (path): Filename from status endpoint

### Endpoint 4: Health Check
- **Path**: `/api/health`
- **Method**: GET
- **Description**: Check API health

## Step 5: Set Up Authentication

1. **API Key Authentication**:
   - RapidAPI automatically handles API key authentication
   - Users will need to include headers:
     ```
     X-RapidAPI-Key: their-api-key
     X-RapidAPI-Host: your-api-host.rapidapi.com
     ```

2. **Configure Environment Variables**:
   ```bash
   RAPIDAPI_KEY=your-secret-key
   RAPIDAPI_HOST=your-api-host.rapidapi.com
   ```

## Step 6: Test Your API

### Test with curl

```bash
# Convert a video
curl -X POST "https://your-app-name.railway.app/api/convert" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Check status
curl "https://your-app-name.railway.app/api/status/TASK_ID" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com"

# Download file
curl -O "https://your-app-name.railway.app/api/download/FILENAME" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: your-api-host.rapidapi.com"
```

### Test with JavaScript

```javascript
const options = {
  method: 'POST',
  headers: {
    'X-RapidAPI-Key': 'YOUR_API_KEY',
    'X-RapidAPI-Host': 'your-api-host.rapidapi.com',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
  })
};

fetch('https://your-app-name.railway.app/api/convert', options)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

## Step 7: Configure Pricing

1. **Set Up Plans**:
   - **Free Tier**: 10 requests/month
   - **Basic**: 100 requests/month ($5)
   - **Pro**: 1000 requests/month ($20)
   - **Enterprise**: Custom pricing

2. **Configure Rate Limits**:
   - Set appropriate rate limits for each plan
   - Consider conversion time and server resources

## Step 8: Publish Your API

1. **Review and Submit**:
   - Review all endpoint configurations
   - Test all endpoints thoroughly
   - Submit for review

2. **RapidAPI Review Process**:
   - RapidAPI team will review your API
   - This can take 1-3 business days
   - They may request changes or improvements

3. **Go Live**:
   - Once approved, your API will be live
   - Users can subscribe and start using it

## Step 9: Monitor and Maintain

### Monitoring

1. **RapidAPI Analytics**:
   - Track API usage
   - Monitor revenue
   - View user feedback

2. **Server Monitoring**:
   - Monitor your Railway deployment
   - Set up alerts for downtime
   - Track performance metrics

### Maintenance

1. **Regular Updates**:
   - Keep yt-dlp updated
   - Monitor for YouTube changes
   - Update dependencies

2. **File Cleanup**:
   - Files are automatically deleted after 24 hours
   - Monitor disk usage
   - Adjust cleanup intervals if needed

## API Usage Examples

### Complete Workflow

```javascript
// 1. Convert video
const convertResponse = await fetch('https://your-app-name.railway.app/api/convert', {
  method: 'POST',
  headers: {
    'X-RapidAPI-Key': 'YOUR_API_KEY',
    'X-RapidAPI-Host': 'your-api-host.rapidapi.com',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID'
  })
});

const convertData = await convertResponse.json();
const taskId = convertData.task_id;

// 2. Poll for status
let statusData;
do {
  await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
  
  const statusResponse = await fetch(`https://your-app-name.railway.app/api/status/${taskId}`, {
    headers: {
      'X-RapidAPI-Key': 'YOUR_API_KEY',
      'X-RapidAPI-Host': 'your-api-host.rapidapi.com'
    }
  });
  
  statusData = await statusResponse.json();
} while (statusData.data.status !== 'completed' && statusData.data.status !== 'error');

// 3. Download file
if (statusData.data.status === 'completed') {
  const downloadUrl = `https://your-app-name.railway.app${statusData.data.download_url}`;
  window.open(downloadUrl);
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure CORS is properly configured in your Flask app
   - Check that RapidAPI headers are being sent

2. **Authentication Errors**:
   - Verify API key is correct
   - Check that RapidAPI host matches your configuration

3. **Conversion Failures**:
   - Check YouTube URL format
   - Verify FFmpeg is installed on your server
   - Monitor server logs for errors

4. **File Download Issues**:
   - Ensure files exist on server
   - Check file permissions
   - Verify download URLs are correct

### Support

- **RapidAPI Support**: [support.rapidapi.com](https://support.rapidapi.com)
- **Railway Support**: [docs.railway.app](https://docs.railway.app)
- **GitHub Issues**: Create issues in your repository

## Revenue Optimization

1. **Pricing Strategy**:
   - Start with competitive pricing
   - Monitor usage patterns
   - Adjust pricing based on demand

2. **Feature Differentiation**:
   - Offer different quality options
   - Add batch processing for higher tiers
   - Provide priority support for enterprise users

3. **Marketing**:
   - Create compelling API documentation
   - Provide usage examples
   - Respond to user feedback quickly

## Legal Considerations

1. **Terms of Service**:
   - Include appropriate disclaimers
   - State that users must respect copyright laws
   - Limit liability for misuse

2. **Copyright Compliance**:
   - Make it clear that users are responsible for compliance
   - Include warnings about copyright infringement
   - Provide guidance on fair use

3. **Data Privacy**:
   - Implement appropriate data retention policies
   - Ensure GDPR compliance if applicable
   - Protect user data and privacy

## Success Metrics

Track these metrics to measure your API's success:

1. **Usage Metrics**:
   - Number of API calls
   - Conversion success rate
   - Average response time

2. **Revenue Metrics**:
   - Monthly recurring revenue
   - Customer acquisition cost
   - Customer lifetime value

3. **User Satisfaction**:
   - User ratings and reviews
   - Support ticket volume
   - Feature requests

Your YouTube to MP3 Converter API is now ready for RapidAPI deployment! 🚀
