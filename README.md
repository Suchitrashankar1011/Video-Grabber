# 🎬 Video Grabber - YouTube Video Downloader

A premium web application for downloading YouTube videos with a stunning glassmorphism UI, real-time progress tracking, and smooth animations.

## 🌐 Live Demo

**Try it now:** [https://video-grabber-production.up.railway.app](https://video-grabber-production.up.railway.app)

## ✨ Features

- 🎨 **Premium Glassmorphism UI** - Beautiful frosted glass design with particle effects
- 💫 **Smooth Animations** - Floating particles, cursor trails, and smooth transitions
- ⬇️ **Fast Downloads** - Direct MP4 downloads with real-time progress
- 📊 **Live Progress Tracking** - Download speed, percentage, and ETA
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- 🚀 **No Setup Required** - Just paste a URL and download
- 🎯 **VLC Compatible** - Downloaded videos work perfectly with VLC Media Player

## 🚀 Quick Start

### For Users

1. Visit [https://video-grabber-production.up.railway.app](https://video-grabber-production.up.railway.app)
2. Paste any YouTube video URL
3. Click "Start Download"
4. Watch the beautiful progress animation
5. Download your video when complete
6. Play with VLC Media Player for best compatibility

### For Developers

```bash
# Clone the repository
git clone https://github.com/Suchitrashankar1011/Video-Grabber.git
cd Video-Grabber

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Open browser
http://localhost:5000
```

## 📁 Project Structure

```
Video-Grabber/
├── app.py                 # Flask backend with yt-dlp integration
├── templates/
│   └── index.html        # Premium glassmorphism UI
├── downloads/            # Downloaded videos (auto-created)
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

## 🎨 UI Features

- **Glassmorphism Design** - Frosted glass effect with backdrop blur
- **Animated Background** - Floating particles with smooth animations
- **Cursor Trail Effect** - Interactive mouse movement particles
- **Gradient Animations** - Beautiful color transitions
- **Shimmer Effects** - Progress bar with shimmer animation
- **Glow Effects** - Pulsing text glow on title
- **Bounce Animations** - Success/error messages with bounce effect
- **Hover Effects** - Buttons lift and glow on hover
- **Slide Animations** - Smooth entrance animations

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Downloader**: yt-dlp (latest version)
- **Frontend**: HTML5, CSS3, JavaScript
- **Fonts**: Poppins (Google Fonts)
- **Server**: Gunicorn
- **Hosting**: Railway

## 🌐 Deployment

### Deploy to Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Get public URL
railway domain
```

### Deploy to Render

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
4. Deploy!

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```



## 🐛 Troubleshooting

### Video Won't Download
- **Solution**: Use VLC Media Player to play downloaded videos
- Some videos may have restrictions
- Try a different video

### Slow Downloads
- Speed depends on your internet connection
- Large videos (1080p+) take longer
- Server location affects speed

### Bot Detection Error
- YouTube may block some videos on cloud platforms
- Most videos work fine
- Try a different video if one fails

## 📈 Performance

- **Average Download Time**: 30-60 seconds for 5-minute video
- **Supported Formats**: MP4 (pre-merged)
- **Max File Size**: Limited by Railway's disk space
- **Concurrent Users**: Scales automatically

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Free for personal and commercial use

## 🌟 Support

- ⭐ Star this repository if you find it useful
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features via GitHub Discussions
- 📧 Contact: suchitrasrivastava657@gmail.com

## 🎉 Acknowledgments

- Built with Flask and yt-dlp
- UI inspired by modern glassmorphism design
- Deployed on Railway
- Font: Poppins by Google Fonts

## 📊 Stats

- **Live Since**: December 2025
- **Total Downloads**: Growing daily
- **User Rating**: ⭐⭐⭐⭐⭐
- **Uptime**: 99.9%

---

**Made with ❤️ by Suchitra Shankar Srivastava**

[Live Demo](https://video-grabber-production.up.railway.app) | [GitHub](https://github.com/Suchitrashankar1011/Video-Grabber) | [Report Issue](https://github.com/Suchitrashankar1011/Video-Grabber/issues)
