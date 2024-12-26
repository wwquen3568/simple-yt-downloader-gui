# YouTube Downloader GUI 🎥

A PySide6-based GUI application to download YouTube videos, music, and thumbnails. This app uses `yt-dlp` for downloading and `pygame` for audio playback.

## Preview 😊
*The usage example video sound is large. so you need to turn down the volumn...*

[Download Example Video](https://private-user-images.githubusercontent.com/94620584/398778771-ae4c4685-5410-49df-a4b5-d5d31da09a22.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzUyMzU2MjIsIm5iZiI6MTczNTIzNTMyMiwicGF0aCI6Ii85NDYyMDU4NC8zOTg3Nzg3NzEtYWU0YzQ2ODUtNTQxMC00OWRmLWE0YjUtZDVkMzFkYTA5YTIyLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI2VDE3NDg0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc0MTBkMGM4YWEwNTVjYjYyZWZkOGViNmQ2NDIzMmU2OWEzYzI5YmUxNzU5ZGU3YzExNGEwOTA1NWEyMmZiOWUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.dypx6h1Gc6UF-4IvsgDgJitxf3hslQMoym5wVvx8azc)


## Features ✨

- **Validate YouTube Links** ✅: Ensure the link is valid before downloading.
- **Download Options** 📝:
  - Download YouTube thumbnails as `.jpg`. 🖼️
  - Extract and download audio in `.mp3` format. 🎵
  - Download videos in the best available format. 📽️
- **Folder Navigation** 📂:
  - Open folders for thumbnails, music, and videos directly from the app.
- **Audio Playback** 🎧:
  - Play the most recently downloaded audio or video file. ▶️
  - Stop playback anytime. ⏹️
- **User-Friendly Logs** 📜: View real-time logs for download progress and playback.

## Notices 🚨

- **Validation Delay**: Validating a link may take some time depending on the video's metadata size. Please be patient. ⏳
- **Playback Bugs**: The audio playback feature might encounter issues with some files. This is due to `pygame` limitations for certain file formats. ⚠️

## Installation 🛠️

### Prerequisites
1. Python 3.10 or later 🐍
2. Pip installed
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Install Dependencies

Create a `requirements.txt` file with the following content:

```
PySide6
yt-dlp
pygame
requests
```

Then, install them:

```bash
pip install -r requirements.txt
```

## Running the Application 🚀

Run the following command in your terminal:

```bash
python main.py
```

## Project Structure 📁

```plaintext
.
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── logs/                # Output Logs
├── result/              # Output folder for downloads
│   ├── thumbnails/      # Folder for downloaded thumbnails
│   ├── mp3/             # Folder for downloaded audio files
│   └── video/           # Folder for downloaded video files

```

## Usage 🛠️

1. **Enter a YouTube Link**: Paste the YouTube link into the input field. 🔗
2. **Validate the Link**: Click the "Validate Link" button. ✔️
   - **Note**: Validating a link may take some time depending on the video's metadata size. Please be patient.
3. **Download Options**: Choose to download the thumbnail, music, or video. ⬇️
4. **Access Files**: Use the "Open Folder" buttons to quickly access your downloads. 📂
5. **Play Audio**: Use the "Play" button to listen to downloaded audio or video. 🎶
   - **Note**: The audio playback feature might encounter issues with some files. This is due to `pygame` limitations for certain file formats.


## Contributing 🤝

Contributions are welcome! Please fork the repository and create a pull request for any changes.


## Acknowledgments 🙏

- `yt-dlp` for the core downloading functionality. 📅
- `pygame` for audio playback. 🎧
- `PySide6` for the beautiful GUI framework. 💻

---

Happy Downloading! 🎉
