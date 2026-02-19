# Library Management System - Deployment Guide

## Step 1: Create a GitHub Repository

1. Go to https://github.com and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `library-management`
5. Select "Public"
6. Click "Create repository"

## Step 2: Upload Files to GitHub

### Option A: Using GitHub Web Interface
1. On your new repository page, click "uploading an existing file"
2. Drag and drop all files from the `library_management` folder
3. Click "Commit changes"

### Option B: Using Git Commands
```
bash
# Open terminal in the library_management folder
cd library_management
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-management.git
git push -u origin main
```

## Step 3: Deploy to Render

1. Go to https://render.com and sign up (use your GitHub account)
2. After signing in, click "New +" and select "Web Service"
3. Click "Connect GitHub" and select your repository
4. Use these settings:
   - **Name:** library-management
   - **Runtime:** Python
   - **Build Command:** (leave empty)
   - **Start Command:** `python app.py`
5. Click "Deploy Web Service"

## Step 4: Access Your Application

After deployment completes (usually 2-5 minutes), you'll get a URL like:
`https://library-management.onrender.com`

## Troubleshooting

### If deployment fails:
1. Check the deployment logs in Render dashboard
2. Make sure all files are uploaded correctly
3. Verify requirements.txt has correct dependencies

### If you see "Application Error":
1. Check the logs for specific error messages
2. Make sure the Procfile is correct
3. Verify Python version in runtime.txt

## Files Already Prepared:
- ✅ Procfile - for Render deployment
- ✅ runtime.txt - Python version specification
- ✅ requirements.txt - Python dependencies
- ✅ app.py - Main Flask application
- ✅ models.py - Database models
- ✅ templates/ - HTML templates
- ✅ static/ - CSS and JavaScript files

## Support
If you need help, please ask!
