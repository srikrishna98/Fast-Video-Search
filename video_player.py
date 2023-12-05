from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QTimer
import sys

class VideoPlayer(QWidget):
    def __init__(self, startTime=0, displayText="CSCI 576: Final Project"):
        super().__init__()
        self.setWindowTitle("CSCI576: Final Project")
        self.startTime = startTime
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
        videoWidget.setMinimumSize(960, 720)
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play_video)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.reset_video)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.sliderMoved.connect(self.set_position)

        self.timeLabel = QLabel("00:00 / 00:00")
        self.customTextLabel = QLabel(displayText)
        self.customTextLabel.setAlignment(Qt.AlignCenter) 

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        
         # Layout for the slider and time label
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.positionSlider)
        slider_layout.addWidget(self.timeLabel)
        slider_layout.setSpacing(0)  # Remove spacing

        # Layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.playButton)
        button_layout.addWidget(self.resetButton)
        button_layout.setSpacing(0)  # Remove spacing

        # Layout for the custom text label
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.customTextLabel)
        info_layout.setSpacing(0)  # Remove spacing

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(slider_layout)
        layout.addLayout(button_layout)
        layout.addLayout(info_layout)
        layout.setSpacing(0)  # Remove spacing between layouts
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.error.connect(self.handle_error)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.reset_video()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText("Play")
            self.timer.stop()
        else:
            self.mediaPlayer.play()
            self.playButton.setText("Pause")
            self.timer.start()

    def reset_video(self):
        self.mediaPlayer.setPosition(self.startTime)
        self.mediaPlayer.pause()
        self.playButton.setText("Play")
        self.positionSlider.setValue(self.startTime)
        self.update_time()
        self.timer.stop()


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_media(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))

    def handle_error(self):
        print("Error: " + self.mediaPlayer.errorString())

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def position_changed(self, position):
        self.positionSlider.setValue(position)

    def update_time(self):
        current_time_ms = self.mediaPlayer.position()
        total_time_ms = self.mediaPlayer.duration()
        frame_rate = 30
        current_frame = int(current_time_ms / (1000 / frame_rate))
        total_frames = int(total_time_ms / (1000 / frame_rate))
        time_and_frame_info = f"{self.format_time(current_time_ms)} / {self.format_time(total_time_ms)}, Frame: {current_frame} / {total_frames}"
        self.timeLabel.setText(time_and_frame_info)

    def format_time(self, ms):
        seconds = int(ms / 1000)
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def set_custom_text(self, text):
    	self.customTextLabel.setText(text)

class VideoApp:
    def __init__(self, path, startTime=0, displayText="CSCI 576: Final Project"):
        self.app = QApplication(sys.argv)
        self.player = VideoPlayer(startTime=startTime, displayText=displayText)
        self.player.set_media(path)
        self.player.reset_video()
        self.player.resize(640*2, 480*2)
        self.player.show()

    def run(self):
        sys.exit(self.app.exec_())