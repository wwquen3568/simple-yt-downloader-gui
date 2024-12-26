from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QWidget, QLineEdit, QHBoxLayout
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QKeyEvent
import yt_dlp
import os
import re
import webbrowser


def clean_ansi_escape_codes(text: str) -> str:
    """
    Remove ANSI escape codes from the given text.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class DownloadThread(QThread):
    progress_signal = Signal(int)  # Signal for progress percentage
    log_signal = Signal(str)      # Signal for log messages

    def __init__(self, url, options):
        super().__init__()
        self.url = url
        self.options = options

    def run(self):
        # Define the progress hook
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '').strip('%')
                if percent.isdigit():
                    self.progress_signal.emit(int(percent))
                self.log_signal.emit(d.get('_default_template', ''))

        # Configure yt-dlp options
        ydl_opts = self.options
        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Link input
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Enter YouTube link here...")
        self.link_input.returnPressed.connect(self.validate_link)
        layout.addWidget(self.link_input)

        # Validation button
        self.validate_button = QPushButton("Validate Link")
        self.validate_button.clicked.connect(self.validate_link)
        layout.addWidget(self.validate_button)

        # Action buttons
        self.thumbnail_button = QPushButton("Download Thumbnail")
        self.music_button = QPushButton("Download Music")
        self.video_button = QPushButton("Download Video")
        self.open_link_button = QPushButton("Open Link in Browser")
        self.open_results_button = QPushButton("Open Results Folder")

        self.thumbnail_button.clicked.connect(self.download_thumbnail)
        self.music_button.clicked.connect(self.download_music)
        self.video_button.clicked.connect(self.download_video)
        self.open_link_button.clicked.connect(self.open_link)
        self.open_results_button.clicked.connect(lambda: os.startfile("result"))

        # Disable buttons initially
        self.thumbnail_button.setEnabled(False)
        self.music_button.setEnabled(False)
        self.video_button.setEnabled(False)
        self.open_link_button.setEnabled(False)

        for btn in [self.thumbnail_button, self.music_button, self.video_button, self.open_link_button]:
            layout.addWidget(btn)

        # Logs
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.progress_label = QLabel("Progress: 0%")
        layout.addWidget(self.progress_label)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variables
        self.valid_link = False
        self.url = ""

    def validate_link(self):
        self.url = self.link_input.text().strip()
        if "youtube.com" in self.url or "youtu.be" in self.url:
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    self.log_area.append(f"Link Validated: {info['title']}")
                    self.valid_link = True
                    self.thumbnail_button.setEnabled(True)
                    self.music_button.setEnabled(True)
                    self.video_button.setEnabled(True)
                    self.open_link_button.setEnabled(True)
            except Exception as e:
                self.log_area.append(f"Error: {str(e)}")
                self.valid_link = False
        else:
            self.log_area.append("Invalid YouTube Link")
            self.valid_link = False

    def download_thumbnail(self):
        if not self.valid_link:
            return
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            thumbnail_url = info['thumbnail']
            self.download_file(thumbnail_url, "result/thumbnails", f"{info['id']}.jpg")
            self.log_area.append(f"Thumbnail downloaded: {thumbnail_url}")

    def download_music(self):
        if not self.valid_link:
            return
        self.start_download({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'result/mp3/%(title)s.%(ext)s',
        })

    def download_video(self):
        if not self.valid_link:
            return
        self.start_download({
            'format': 'best',
            'outtmpl': 'result/video/%(title)s.%(ext)s',
        })

    def open_link(self):
        if self.valid_link:
            webbrowser.open(self.url)

    def start_download(self, options):
        self.download_thread = DownloadThread(self.url, options)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.log_signal.connect(self.update_log)
        self.download_thread.start()

    def update_progress(self, progress):
        self.progress_label.setText(f"Progress: {progress}%")

    def update_log(self, log_message):
        # Clean the log message of ANSI escape codes before displaying
        cleaned_message = clean_ansi_escape_codes(log_message)
        self.log_area.append(cleaned_message)

    def download_file(self, url, path, filename):
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            base, ext = os.path.splitext(full_path)
            counter = 1
            while os.path.exists(full_path):
                full_path = f"{base}({counter}){ext}"
                counter += 1
        with open(full_path, 'wb') as file:
            file.write(requests.get(url).content)


if __name__ == "__main__":
    import sys
    import requests
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
