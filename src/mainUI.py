from UI.MainWindows import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap

import cv2
import numpy

from common import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.windows = Ui_Form()
        self.windows.setupUi(self)

        self.windows.pushButton.clicked.connect(self.start)
        self.windows.pushButton_2.clicked.connect(self.stop)


    def start(self):
        print("open")

        self.camera = cv2.VideoCapture(CONFIG["camera_source"])
        if self.camera.isOpened():
            #若为while True，则会存在camera读取不到frame而导致程序崩溃。关闭camera存在时间空隙
            while self.camera.isOpened():
                ret, frame = self.camera.read()
                frame = cv2.resize(frame, (350, 300))

                frame, ear, mar = IndicatorCalc.get_fatigue_index(frame, True)

                self.show_info(ear, mar)
                self.show_frame(frame)

                cv2.waitKey(1)


    def stop(self):
        print("close")
        if self.camera.isOpened():
            self.camera.release()


    def show_info(self, ear, mar):
        if ear != None and mar != None:
            if ear <= CONFIG["personal_characteristics_threshold"]["eye"]:
                self.windows.label_2.setText("{} - {}".format(str(ear), "已闭眼"))
            else:
                self.windows.label_2.setText("{} - {}".format(str(ear), "已睁开眼"))

            if mar >= CONFIG["personal_characteristics_threshold"]["yawn"]:
                self.windows.label_3.setText("{} - {}".format(str(mar), "哈切"))
            else:
                self.windows.label_3.setText("{} - {}".format(str(mar), "闭嘴"))


    def show_frame(self, frame):
        frame_qt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame_qt = QImage(frame_qt.data,
                          frame_qt.shape[1], frame_qt.shape[0],
                          QImage.Format_RGB32).rgbSwapped()
        self.windows.label.setPixmap(QPixmap.fromImage(frame_qt))
        self.windows.label.show()




if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
