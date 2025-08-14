# VedhVaani Kundali API - Railway Deploy Pack

## 🚀 Deployment Steps

### 1. Upload to GitHub
- Create a new GitHub repository.
- Upload all files from this folder to that repository.

### 2. Deploy on Railway
- Go to [https://railway.app](https://railway.app) and sign in with GitHub.
- Click "New Project" → "Deploy from GitHub Repo".
- Select your repository.

### 3. Settings
- Railway will auto-detect Python project and install requirements.
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. Test API
- After deploy, open your Railway project's public URL.
- Visit `/docs` endpoint to test API.

Example: `https://your-railway-app.up.railway.app/docs`

### 5. Connect to VedhVaani App
- Replace API URL in your VedhVaani app with Railway's public URL.
