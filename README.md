# YouTube Downloader GUI 🎥

A PySide6-based GUI application to download YouTube videos, music, and thumbnails. This app uses `yt-dlp` for downloading and `pygame` for audio playback.

## Preview 😊
[Download Example Video](examples/example.mp4)


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

## Screenshots 📸

### Main Interface
![Main Interface](https://via.placeholder.com/800x600.png?text=Main+Interface)

### Logs
![Logs](https://via.placeholder.com/800x600.png?text=Logs)

## Contributing 🤝

Contributions are welcome! Please fork the repository and create a pull request for any changes.


## Acknowledgments 🙏

- `yt-dlp` for the core downloading functionality. 📅
- `pygame` for audio playback. 🎧
- `PySide6` for the beautiful GUI framework. 💻

---

Happy Downloading! 🎉
