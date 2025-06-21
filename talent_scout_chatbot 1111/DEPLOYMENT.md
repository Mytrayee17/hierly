# 🚀 Deployment Guide for Hirely AI

This guide covers multiple deployment options for your Hirely AI Streamlit application.

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Git repository (GitHub recommended)

## 🎯 **Option 1: Streamlit Cloud (Recommended)**

**Best for:** Streamlit applications, easiest setup, free tier available

### Steps:
1. **Push your code to GitHub** ✅ (Already done!)
2. **Visit [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Configure:**
   - **Repository**: `Mytrayee17/hierly`
   - **Branch**: `main`
   - **Main file path**: `talent_scout_chatbot 1111/app.py`
6. **Add your API key in the secrets section:**
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
7. **Click "Deploy"**

### Advantages:
- ✅ Native Streamlit support
- ✅ Automatic HTTPS
- ✅ Free tier available
- ✅ Easy environment variable management
- ✅ Automatic deployments on git push

---

## 🌐 **Option 2: Vercel Deployment**

**Best for:** Custom domains, advanced routing, serverless functions

### Setup Files Created:
- ✅ `vercel.json` - Vercel configuration
- ✅ Updated `requirements.txt` - Clean dependencies

### Steps:
1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory:**
   ```bash
   cd "talent_scout_chatbot 1111"
   vercel
   ```

4. **Set environment variables:**
   ```bash
   vercel env add GEMINI_API_KEY
   ```

5. **Follow the prompts and deploy**

### Custom Domain (Optional):
```bash
vercel domains add yourdomain.com
```

---

## 🐳 **Option 3: Docker Deployment**

**Best for:** Self-hosted solutions, full control

### Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy:
```bash
docker build -t hirely-ai .
docker run -p 8501:8501 -e GEMINI_API_KEY=your-key hirely-ai
```

---

## ☁️ **Option 4: Heroku**

**Best for:** Traditional cloud hosting

### Create Procfile:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Deploy:
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your-api-key
git push heroku main
```

---

## 🔧 **Environment Variables Setup**

For all deployments, you'll need to set your Google Gemini API key:

### Streamlit Cloud:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### Vercel:
```bash
vercel env add GEMINI_API_KEY
```

### Docker:
```bash
docker run -e GEMINI_API_KEY=your-key ...
```

### Heroku:
```bash
heroku config:set GEMINI_API_KEY=your-api-key
```

---

## 📊 **Performance Considerations**

### For Vercel:
- ⚠️ **Cold starts**: First request may be slower
- ⚠️ **Function timeout**: 10 seconds for hobby plan
- ⚠️ **Memory limits**: 1024MB for hobby plan

### For Streamlit Cloud:
- ✅ **No cold starts**
- ✅ **Longer timeouts**
- ✅ **Better for interactive apps**

---

## 🔒 **Security Best Practices**

1. **Never commit API keys to Git**
2. **Use environment variables**
3. **Enable HTTPS (automatic on most platforms)**
4. **Set up proper CORS if needed**

---

## 🚨 **Troubleshooting**

### Common Issues:

1. **ModuleNotFoundError:**
   - Check `requirements.txt` includes all dependencies
   - Ensure Python version compatibility

2. **API Key Issues:**
   - Verify environment variable is set correctly
   - Check API key permissions

3. **Port Issues:**
   - Ensure app listens on `0.0.0.0` for container deployments
   - Use `$PORT` environment variable when available

4. **Memory Issues:**
   - Optimize imports
   - Use `@st.cache_data` for expensive operations

---

## 📈 **Monitoring & Analytics**

### Streamlit Cloud:
- Built-in analytics dashboard
- Usage statistics
- Error logs

### Vercel:
- Function execution logs
- Performance metrics
- Error tracking

---

## 🎉 **Recommended Approach**

**For your Hirely AI application, I recommend:**

1. **Start with Streamlit Cloud** - Easiest setup, perfect for Streamlit apps
2. **Consider Vercel** if you need custom domains or advanced features
3. **Use Docker** for self-hosted or enterprise deployments

---

**Ready to deploy? Choose your platform and follow the steps above!** 🚀 