from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QWidget, QLineEdit, QGroupBox, QScrollArea
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap
import yt_dlp
import os
import re
import requests
import pygame

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

        # Define project directory and result folder paths
        self.project_dir = os.path.abspath(os.path.dirname(__file__))
        self.result_dir = os.path.join(self.project_dir, "result")
        self.thumbnails_dir = os.path.join(self.result_dir, "thumbnails")
        self.music_dir = os.path.join(self.result_dir, "mp3")
        self.video_dir = os.path.join(self.result_dir, "video")

        # Create result folders if they don't exist
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Set up the UI
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 900, 700)

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

        # Validation result section
        self.validation_group = QGroupBox("Validation Result")
        validation_layout = QVBoxLayout()

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setPixmap(QPixmap())  # Placeholder for thumbnail
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        validation_layout.addWidget(self.thumbnail_label)

        self.title_label = QLabel("No link validated yet.")
        validation_layout.addWidget(self.title_label)

        self.validation_group.setLayout(validation_layout)
        layout.addWidget(self.validation_group)

        # Optional input for custom name
        self.custom_name_input = QLineEdit()
        self.custom_name_input.setPlaceholderText("Custom file name (optional)")
        self.custom_name_input.setEnabled(False)
        layout.addWidget(self.custom_name_input)

        # Action buttons
        self.thumbnail_button = QPushButton("Download Thumbnail")
        self.music_button = QPushButton("Download Music")
        self.video_button = QPushButton("Download Video")
        self.open_thumbnails_folder_button = QPushButton("Open Thumbnails Folder")
        self.open_music_folder_button = QPushButton("Open Music Folder")
        self.open_video_folder_button = QPushButton("Open Videos Folder")

        # Connect buttons to open folder paths
        self.open_thumbnails_folder_button.clicked.connect(lambda: os.startfile(self.thumbnails_dir))
        self.open_music_folder_button.clicked.connect(lambda: os.startfile(self.music_dir))
        self.open_video_folder_button.clicked.connect(lambda: os.startfile(self.video_dir))

        # Connect buttons
        self.thumbnail_button.clicked.connect(self.download_thumbnail)
        self.music_button.clicked.connect(self.download_music)
        self.video_button.clicked.connect(self.download_video)

        # Disable buttons initially
        for btn in [
            self.thumbnail_button, self.music_button, self.video_button
        ]:
            layout.addWidget(btn)
            btn.setEnabled(False)

        layout.addWidget(self.open_thumbnails_folder_button)
        layout.addWidget(self.open_music_folder_button)
        layout.addWidget(self.open_video_folder_button)

        # Logs
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        # Recently downloaded section
        self.recently_downloaded_label = QLabel("Nothing was downloaded just yet...")
        layout.addWidget(self.recently_downloaded_label)

        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        self.play_button.clicked.connect(self.play_recent)
        self.stop_button.clicked.connect(self.stop_playback)

        # Scroll area
        scroll_area = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)

        self.setCentralWidget(scroll_area)

        # Variables
        self.valid_link = False
        self.url = ""
        self.recent_file = None

    def validate_link(self):
        self.url = self.link_input.text().strip()
        if "youtube.com" in self.url or "youtu.be" in self.url:
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    self.title_label.setText(f"Title: {info['title']}")
                    self.valid_link = True
                    self.custom_name_input.setEnabled(True)
                    self.thumbnail_button.setEnabled(True)
                    self.music_button.setEnabled(True)
                    self.video_button.setEnabled(True)
                    self.show_thumbnail(info['thumbnail'])
            except Exception as e:
                self.title_label.setText("Validation failed!")
                self.valid_link = False
        else:
            self.title_label.setText("Validation failed!")
            self.valid_link = False

    def show_thumbnail(self, url):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        # Resize the pixmap to a maximum size while maintaining aspect ratio
        max_width = 300
        max_height = 300
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        self.thumbnail_label.setPixmap(scaled_pixmap)

    def download_thumbnail(self):
        if not self.valid_link:
            return
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            title = info['title']
            filename = self.generate_unique_filename(title, self.thumbnails_dir, "jpg")
            response = requests.get(info['thumbnail'])
            with open(filename, 'wb') as f:
                f.write(response.content)
            self.log_area.append(f"Downloaded thumbnail: {filename}")

    def download_music(self):
        if not self.valid_link:
            return
        custom_name = self.custom_name_input.text().strip()
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.music_dir, f'{custom_name or "%(title)s"}.%(ext)s'),
        }
        self.start_download(options)

    def download_video(self):
        if not self.valid_link:
            return
        custom_name = self.custom_name_input.text().strip()
        options = {
            'format': 'best',
            'outtmpl': os.path.join(self.video_dir, f'{custom_name or "%(title)s"}.%(ext)s'),
        }
        self.start_download(options)

    def start_download(self, options):
        self.download_thread = DownloadThread(self.url, options)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.log_signal.connect(self.update_log)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, progress):
        pass

    def update_log(self, log_message):
        cleaned_message = clean_ansi_escape_codes(log_message)
        self.log_area.append(cleaned_message)

    def download_finished(self):
        # Enable play button for the most recent file
        self.recent_file = self.find_recent_file()
        if self.recent_file:
            self.recently_downloaded_label.setText(f"Recently downloaded: {self.recent_file}")
            self.play_button.setEnabled(True)

    def play_recent(self):
        if self.recent_file:
            try:
                pygame.mixer.music.load(self.recent_file)
                pygame.mixer.music.play()
                self.log_area.append(f"Playing: {self.recent_file}")
                self.stop_button.setEnabled(True)
            except pygame.error as e:
                self.log_area.append(f"Error playing file: {str(e)}")

    def stop_playback(self):
        pygame.mixer.music.stop()
        self.log_area.append("Playback stopped.")
        self.stop_button.setEnabled(False)

    def find_recent_file(self):
        # Check both music and video directories for the most recent file
        recent_files = []
        for folder in [self.music_dir, self.video_dir]:
            for root, _, files in os.walk(folder):
                for file in files:
                    recent_files.append(os.path.join(root, file))
        return max(recent_files, key=os.path.getctime, default=None)

    def generate_unique_filename(self, base, folder, ext):
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"{base}.{ext}")
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(folder, f"{base} ({counter}).{ext}")
            counter += 1
        return filename


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
