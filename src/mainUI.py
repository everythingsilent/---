from UI.MainWindows import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import cv2
import numpy

from common import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('提示')
        self.windows_height = 230
        self.windows_widht = 280
        self.resize(self.windows_widht, self.windows_height)
        self.move(QApplication.desktop().width()-self.windows_widht-50, 1080-self.windows_height-100)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.windows = Ui_Form()
        self.windows.setupUi(self)

        self.fatigue_indicator = IndicatorCalc.Fatigue()
        self.camera = cv2.VideoCapture(CONFIG["camera_source"])
        self.camera_switch = False

        self.windows.pushButton.clicked.connect(self.start)
        self.windows.pushButton_2.clicked.connect(self.prompt)


    def start(self):
        if not self.camera_switch:
            self.camera_switch = True
        else:
            self.camera_switch = False

        if self.camera.isOpened():
            # 若为while True，则会存在camera读取不到frame而导致程序崩溃。关闭camera存在时间空隙
            while self.camera.isOpened():
                ret, frame = self.camera.read()
                frame = cv2.resize(frame, (350, 300))

                if self.camera_switch:
                    frame = self.fatigue_indicator.update(frame)

                    self.fatigue_indicator.show_info()

                    fatigue_indicator = self.fatigue_indicator.get_indicator()
                    self.windows.label_2.setText("疲劳指标")
                    self.windows.label_3.setText(fatigue_indicator)

                    self.show_frame(frame)
                    cv2.waitKey(1)
                else:
                    cv2.waitKey(0)

    def show_frame(self, frame):
        frame_qt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame_qt = QImage(frame_qt.data,
                          frame_qt.shape[1], frame_qt.shape[0],
                          QImage.Format_RGB32).rgbSwapped()
        self.windows.label.setPixmap(QPixmap.fromImage(frame_qt))
        self.windows.label.show()


    def prompt(self):
        # 显示窗口
        self.new_windows = NewWindow()
        self.new_windows.show()

        music_path =r"UI\audio\moderate.mp3"
        url = QUrl.fromLocalFile(music_path)
        content = QMediaContent(url)

        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        print(self.player.state())


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
