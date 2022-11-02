from UI.UIMainWindows import Ui_Form
from UI.promptWindow import PromptWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import cv2
from threading import Thread
import time
from decimal import Decimal

from common import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windows = Ui_Form()
        self.windows.setupUi(self)

        self.fatigue_detector = IndicatorCalc.Fatigue()

        # 初始化摄像头
        self.camera = Thread(target=self.open_camera).start()
        self.camera_switch = False

        self.windows.pushButton.clicked.connect(self.start_detection)
        self.windows.pushButton_2.clicked.connect(self.stop_camera)


    def open_camera(self):
        self.camera = cv2.VideoCapture(CONFIG["camera_source"])
        self.windows.pushButton.setDisabled(False)

        self.windows.label_2.setText("摄像头加载成功")
        self.camera_switch = True


    def stop_camera(self):
        self.camera.release()
        self.camera_switch = False


    def start_detection(self):
        self.windows.pushButton.setDisabled(True)
        self.windows.pushButton_2.setDisabled(False)

        def show_frame(current_frame):
            frame_qt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame_qt = QImage(frame_qt.data,
                              frame_qt.shape[1], frame_qt.shape[0],
                              QImage.Format_RGB32).rgbSwapped()
            self.windows.label.setPixmap(QPixmap.fromImage(frame_qt))
            self.windows.label.show()


        def show_fatigue_info(fatigue_detector):
            fatigue_indicator_class = ["清醒", "轻度疲劳", "中度疲劳", "重度疲劳"]
            current_fatigue_indicator = fatigue_indicator_class[fatigue_detector.get_indicator()]
            self.windows.label_2.setText(f"当前疲劳指标为:{current_fatigue_indicator}\n"
                                         f"FPS:{fatigue_detector.get_fps()}\n"
                                         f"平均打哈切次数:{fatigue_detector.get_avg_yawn_count()}\n"
                                         f"平均闭眼时长:{fatigue_detector.get_avg_close_time()}\n"
                                         f"PERCLOS:{fatigue_detector.get_perclos()}\n"
                                         f"总检测时长:{round(fatigue_detector.total_time, 2)}")


        def prompt_voice_broadcast(current_indicator):
            print("语音播报")


        def prompt_windows_warning(current_indicator):
            print("弹窗警告")


        def prompt_info_prompt(current_indicator):
            print("信息提示")


        def prompt_mode(current_indicator):
            if CONFIG["prompt_mode"]["voice_broadcast"] == 1:
                prompt_voice_broadcast(current_indicator)
            if CONFIG["prompt_mode"]["windows_warning"] == 1:
                prompt_windows_warning(current_indicator)
            if CONFIG["prompt_mode"]["info_prompt"] == 1:
                prompt_info_prompt(current_indicator)


        prompt_interval_minute = CONFIG["prompt_interval_minute"]
        minimum_prompt_level = CONFIG["minimum_prompt_level"]

        initiate_time = time.time()
        last_recorded_minute = 0
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            frame = self.fatigue_detector.update(frame)
            fatigue_indicator = self.fatigue_detector.get_indicator()

            show_frame(frame)
            show_fatigue_info(self.fatigue_detector)

            # 根据提示间隔提示 Decimal解决浮点计算不精确问题
            current_time = time.time() - initiate_time
            current_minute = round(current_time/60, 2)
            trigger_time = Decimal(str(current_minute)) % Decimal(str(prompt_interval_minute))

            self.fatigue_detector.total_time = current_time
            self.windows.pushButton.setText(f"{current_minute} {trigger_time}")

            if trigger_time == 0 and last_recorded_minute != current_minute:
                last_recorded_minute = current_minute

                # 当前指标对应提示方式
                if minimum_prompt_level >= fatigue_indicator:
                    prompt_mode(fatigue_indicator)

            cv2.waitKey(1)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
