# 🚀 How to Deploy Smart Grocery Budget Planner on Render

This guide explains how to deploy the **Smart Grocery Budget Planner** web application to [Render](https://render.com) for free in less than 3 minutes.

---

## 📋 Pre-Configured Render Files

Your repository is already pre-configured with all necessary files for Render:

| File | Purpose |
| :--- | :--- |
| `render.yaml` | Render Blueprint configuration (automates service type, build/start commands, environment variables, and health checks). |
| `Procfile` | Specifies the web process command: `web: python server.py`. |
| `runtime.txt` | Sets the Python version: `python-3.11.9`. |
| `requirements.txt` | Standard dependencies installer for Render's build step. |
| `.gitignore` | Excludes bytecode, temporary test files, and local OS artifacts. |
| `server.py` | Cloud-ready server binding to `0.0.0.0` and reading Render's dynamic `$PORT`. Includes `/healthz` endpoint. |

---

## ⚡ Step-by-Step Deployment Instructions

### Option A: Upload via GitHub Web Interface (No Git installation needed!)
1. Go to [GitHub.com](https://github.com/) and sign in.
2. Click **“New”** to create a new repository (name it e.g. `smart-grocery-budget-planner`), set it to **Public**, and click **“Create repository”**.
3. On the new repository page, click the link: **“uploading an existing file”**.
4. Drag and drop all the files from this folder (`c:\Users\SHREYAS\OneDrive\Desktop\groceries budget planner`) into the GitHub upload area.
5. Click **“Commit changes”**.

### Option B: Push via Git Terminal (if Git is installed)
```bash
git init
git add .
git commit -m "Initial commit: Smart Grocery Budget Planner"
git remote add origin https://github.com/<YOUR_USERNAME>/smart-grocery-budget-planner.git
git branch -M main
git push -u origin main
```

---

## ☁️ Connect & Deploy on Render (Free)
1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click the **“New +”** button at the top right and select **“Web Service”**.
3. Choose **“Build and deploy from a Git repository”** and click **Next**.
4. Connect your GitHub account and select your repository: `smart-grocery-budget-planner`.

---

### Step 3: Configure Settings on Render
Render will automatically detect the settings from `render.yaml`, or you can verify:

- **Name**: `smart-grocery-budget-planner` (or your choice)
- **Region**: Choose the closest region (e.g., *Singapore*, *Oregon*, or *Frankfurt*)
- **Branch**: `main`
- **Root Directory**: Leave blank (default root)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Instance Type**: `Free`

*(Optional) Advanced Settings:*
- **Health Check Path**: `/healthz`

---

### Step 4: Click “Deploy Web Service”
- Render will start building the project and deploying the application.
- Once finished, you will receive your live URL:
  `https://smart-grocery-budget-planner.onrender.com`
- Open the URL in any browser or share it on mobile!

---

## ⚡ Method 2: Deploy using Render Blueprints

Render supports 1-click infrastructure deployment using the included `render.yaml`:
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **“New +”** → **“Blueprint”**.
3. Select your repository.
4. Render will automatically parse `render.yaml` and configure everything.
5. Click **“Apply”**.

---

## 🔍 Verifying the Deployment
Once deployed, check:
1. **Health Check**: `https://<YOUR-RENDER-URL>.onrender.com/healthz` (returns `{"status": "healthy"}`)
2. **REST API**: `https://<YOUR-RENDER-URL>.onrender.com/api/data` (returns JSON state)
3. **Web Dashboard**: `https://<YOUR-RENDER-URL>.onrender.com` (loads responsive dashboard)
