# YouTube Video Downloader

A fast and reliable web application for downloading YouTube videos in MP4 format. Features a modern interface with real-time progress tracking.

## ✨ Features

- 🎬 **Clean Web Interface** - Modern, responsive design
- ⬇️ **Fast Downloads** - Direct MP4 downloads with real-time progress
- 📊 **Live Progress** - Download speed, percentage, and ETA
- 📱 **Mobile Friendly** - Works on all devices
- 🚀 **No Setup Required** - Works out of the box

## 🎯 Recommended Player

**Use VLC Media Player** for best compatibility:
- Download VLC (free): https://www.videolan.org/
- VLC plays all downloaded videos perfectly
- Available for Windows, Mac, Linux, iOS, and Android

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

Navigate to `http://localhost:5000`

## 📖 Usage

1. **Paste YouTube URL** - Copy any YouTube video URL
2. **Click "Start Download"** - Begin the download
3. **Watch Progress** - Real-time speed and ETA
4. **Download Complete** - Click the link to save the video
5. **Play with VLC** - Open the video in VLC Media Player

## 📁 File Structure

```
youtube-downloader/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Frontend interface
├── downloads/            # Downloaded videos (auto-created)
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

## 🌐 Deployment

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### Deploy to Railway/Render

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Deploy!

### Environment Variables

- `PORT` - Server port (default: 5000)
- `DEBUG` - Debug mode (set to `False` for production)

## 🔧 Technical Details

### How It Works

1. **Format Selection** - Selects best available MP4 format
2. **Direct Download** - Downloads pre-merged video+audio files
3. **Progress Tracking** - Real-time updates via polling
4. **File Serving** - Secure file delivery through Flask

### Technology Stack

- **Backend**: Flask (Python)
- **Downloader**: yt-dlp
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: Local filesystem

## 📝 Notes

- **Fast Downloads** - No conversion or processing delays
- **VLC Recommended** - Best compatibility with all video formats
- **Secure** - Path validation prevents security issues
- **Production Ready** - Suitable for deployment

## 🐛 Troubleshooting

### Video Won't Play

- **Solution**: Use VLC Media Player (plays everything)
- Download VLC: https://www.videolan.org/

### Download Fails

- Check your internet connection
- Verify the YouTube URL is correct
- Some videos may have restrictions
- Try a different video

### Slow Downloads

- Speed depends on your internet connection
- Large videos (1080p+) take longer
- Server location affects download speed

## 🎥 Alternative Players

If you don't want to use VLC:
- **Windows**: Movies & TV app (built-in)
- **Mac**: QuickTime Player
- **Web Browsers**: Chrome, Firefox, Edge (drag and drop video file)
- **Mobile**: Default video players usually work



## 📄 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Feel free to submit a Pull Request.

## ⭐ Support

If you find this useful, please star the repository!

---

**Made with ❤️ for easy YouTube downloads**
