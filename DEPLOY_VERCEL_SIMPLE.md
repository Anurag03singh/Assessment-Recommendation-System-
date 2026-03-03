# Deploy to Vercel - Simple Guide

## Prerequisites
- Vercel account (free): https://vercel.com/signup
- Vercel CLI: `npm install -g vercel`

---

## Deploy Backend (5 minutes)

### Step 1: Login to Vercel
```bash
vercel login
```

### Step 2: Deploy Backend
```bash
cd backend
vercel --prod
```

When prompted:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name?** → `shl-api` (or your choice)
- **Directory?** → `./` (current directory)
- **Override settings?** → No

### Step 3: Copy Your Backend URL
After deployment, you'll see:
```
✅ Production: https://shl-api-xxx.vercel.app
```

**Copy this URL!** You'll need it for the frontend.

---

## Deploy Frontend (3 minutes)

### Step 1: Set API URL
```bash
cd ../frontend
```

Create `.env.production`:
```
VITE_API_URL=https://shl-api-xxx.vercel.app
```
(Replace with your actual backend URL)

### Step 2: Deploy Frontend
```bash
vercel --prod
```

When prompted:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name?** → `shl-frontend` (or your choice)
- **Directory?** → `./` (current directory)
- **Override settings?** → No

### Step 3: Copy Your Frontend URL
After deployment:
```
✅ Production: https://shl-frontend-xxx.vercel.app
```

---

## Test Your Deployment

### Test Backend
```bash
curl https://shl-api-xxx.vercel.app/health
```

Expected: `{"status":"healthy"}`

### Test Frontend
Open in browser:
```
https://shl-frontend-xxx.vercel.app
```

Try a query: "Java developer with collaboration skills"

---

## Update Deployment

### Update Backend
```bash
cd backend
git pull
vercel --prod
```

### Update Frontend
```bash
cd frontend
git pull
vercel --prod
```

---

## Your URLs for Submission

**GitHub**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

**Backend API**: `https://shl-api-xxx.vercel.app`

**Frontend**: `https://shl-frontend-xxx.vercel.app`

---

## Troubleshooting

### Backend: "Module not found"
```bash
cd backend
vercel --prod --force
```

### Frontend: Can't connect to API
1. Check `.env.production` has correct backend URL
2. Redeploy: `vercel --prod --force`

### Both: Need to rebuild
```bash
vercel --prod --force
```

---

## That's It! 🎉

Both frontend and backend are now deployed on Vercel!

**Total time: ~8 minutes**
