from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QGridLayout
from pytube import YouTube, Playlist
import os
import sys
import ssl
 
# in case it didn't work uncomment this , but becareful since it disables certificate verification for HTTPS connections
#ssl._create_default_https_context = ssl._create_unverified_context


class PlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Playlist Downloader")

        # Playlist URL Label and Text Field
        self.playlist_url_label = QLabel("Playlist URL:")
        self.playlist_url_field = QLineEdit()

        # Download Path Label and Button
        self.download_path_label = QLabel("Download Path:")
        self.download_path_button = QPushButton("Choose Folder")
        self.download_path_button.clicked.connect(self.openFolderDialog)

        # Download Button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.downloadPlaylist)

        
        self.status_label = QLabel("")

        grid = QGridLayout()
        grid.addWidget(self.playlist_url_label, 0, 0)
        grid.addWidget(self.playlist_url_field, 0, 1)
        grid.addWidget(self.download_path_label, 1, 0)
        grid.addWidget(self.download_path_button, 1, 1)
        grid.addWidget(self.download_button, 2, 0, 1, 2)
        grid.addWidget(self.status_label, 3, 0, 1, 2)
        self.setLayout(grid)

        self.show()

    def openFolderDialog(self):
        download_path = QFileDialog.getExistingDirectory(self, "Choose Download Folder")
        if download_path:
            self.download_path_button.setText(download_path)

    def downloadPlaylist(self):
        playlist_url = self.playlist_url_field.text()
        download_path = self.download_path_button.text()
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls
        playlist_title = playlist.title
        folder_path = os.path.join(download_path, playlist_title)
        os.makedirs(folder_path, exist_ok=True)

        for url in video_urls:
            try:
                video = YouTube(url)
                video_stream = video.streams.get_highest_resolution()
                video_stream.download(folder_path)
                self.status_label.setText(f"Downloaded video: {video.title}")
            except Exception as e:
                self.status_label.setText(f"Error downloading video: {video.title}. {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlaylistDownloader()
    sys.exit(app.exec_())
