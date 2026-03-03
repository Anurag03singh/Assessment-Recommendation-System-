# Final Deployment Steps for Render

Your pre-built embeddings are now in the repo. Follow these steps to complete deployment:

## Step 1: Configure Environment Variables on Render

Go to your Render dashboard and add these environment variables:

```
USE_LITE_MODE=true
SKIP_RERANKING=true
```

**How to add:**
1. Go to https://dashboard.render.com
2. Select your service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add both variables above
6. Click "Save Changes"

## Step 2: Trigger Redeploy

The code is already pushed to GitHub. Render should auto-deploy, or you can:
1. Go to "Manual Deploy" section
2. Click "Deploy latest commit"

## Step 3: Monitor Deployment

Watch the logs for:
- ✓ "Recommendation engine loaded successfully" (means it loaded pre-built embeddings)
- No "Building embeddings" message (good - means it's using pre-built)
- Memory usage should stay under 400MB

## Step 4: Test Your API

Once deployed, test with:

```bash
# Replace YOUR_APP_URL with your Render URL
export API_URL="https://your-app.onrender.com"

# Health check
curl $API_URL/health

# Test recommendation
curl -X POST $API_URL/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Looking for Python developer with SQL skills",
    "top_k": 5
  }'
```

## Your API Endpoint

Once deployed, your API will be available at:
```
https://your-app-name.onrender.com/recommend
```

**Request format:**
```json
{
  "query": "Your job description or search text",
  "top_k": 10
}
```

**Response format:**
```json
{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "adaptive_support": "Yes",
      "description": "Assessment description",
      "duration": 60,
      "remote_support": "Yes",
      "test_type": ["Technical", "Cognitive"]
    }
  ]
}
```

## Troubleshooting

If deployment still fails:

1. **Check logs** for specific errors
2. **Verify environment variables** are set correctly
3. **Try Vercel instead** (see VERCEL_DEPLOYMENT.md) - better for serverless
4. **Upgrade to Starter plan** ($7/month) for 2GB RAM if needed

## Alternative: Deploy to Vercel (Recommended)

Vercel has better free tier limits for serverless functions:

```bash
npm install -g vercel
cd backend
vercel
```

Follow prompts and your API will be live in minutes!
