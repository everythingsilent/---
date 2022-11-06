from UI.UIMainWindows import Ui_Form
from UI.promptWindow import PromptWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import cv2
from threading import Thread
import time
import sys
from decimal import Decimal

import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windows = Ui_Form()
        self.windows.setupUi(self)

        self.fatigue_detector = IndicatorCalc.Fatigue()

        self.camera_switch = False
        self.camera = None

        self.windows.pushButton.clicked.connect(self.start_detection)
        self.windows.pushButton_2.clicked.connect(self.stop_detection)


    def stop_detection(self):
        self.camera.release()
        self.camera_switch = False
        self.windows.pushButton.setDisabled(False)
        self.windows.pushButton_2.setDisabled(True)


    def start_detection(self):
        self.fatigue_detector.__init__()
        self.camera = cv2.VideoCapture(CONFIG["camera_source"], cv2.CAP_DSHOW)
        self.camera_switch = True
        self.windows.pushButton.setDisabled(True)
        self.windows.pushButton_2.setDisabled(False)


        def show_frame(current_frame):
            frame_qt = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGBA)
            frame_qt = QImage(frame_qt.data,
                              frame_qt.shape[1], frame_qt.shape[0],
                              QImage.Format_RGB32).rgbSwapped()
            self.windows.label.setPixmap(QPixmap.fromImage(frame_qt))
            self.windows.label.show()

        def show_fatigue_info(fatigue_detector, detection_minute, t_time, pi_minute):
            fatigue_indicator_class = ["清醒", "轻度疲劳", "中度疲劳", "重度疲劳"]
            current_fatigue_indicator = fatigue_indicator_class[fatigue_detector.get_indicator()]
            self.windows.label_2.setText(f"当前疲劳指标为:{current_fatigue_indicator}\n"
                                         f"FPS:{fatigue_detector.get_fps()}\n"
                                         f"平均打哈切次数:{fatigue_detector.get_avg_yawn_count()}\n"
                                         f"平均闭眼时长:{fatigue_detector.get_avg_close_time()}\n"
                                         f"PERCLOS:{fatigue_detector.get_perclos()}\n"
                                         f"检测到人脸时长:{round(fatigue_detector.total_time, 2)}秒\n"
                                         f"系统检测时长:{detection_minute}分钟\n"
                                         f"距系统触发提示时间:{t_time}/{pi_minute}")



        def prompt_voice_broadcast(current_indicator):
            def get_audio_path():
                if current_indicator == 1:
                    ret_audio_path = r"common/audio/mild.mp3"
                elif current_indicator == 2:
                    ret_audio_path = r"common/audio/moderate.mp3"
                elif current_indicator == 3:
                    ret_audio_path = r"common/audio/severe.mp3"
                else:
                    ret_audio_path = r"common/audio/fine.mp3"
                return ret_audio_path

            audio_path = get_audio_path()
            url = QUrl.fromLocalFile(audio_path)
            content = QMediaContent(url)

            self.player = QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()


        def prompt_windows_warning(current_indicator):
            self.window_warning = PromptWindow(current_indicator)
            self.window_warning.show()


        def prompt_info_prompt(current_indicator):
            print("信息提示")
            print("当前状态为：", current_indicator)


        def prompt_mode(current_indicator):
            if CONFIG["prompt_mode"]["voice_broadcast"] == 1:
                prompt_voice_broadcast(current_indicator)
            if CONFIG["prompt_mode"]["windows_warning"] == 1:
                prompt_windows_warning(current_indicator)
            if CONFIG["prompt_mode"]["info_prompt"] == 1:
                Thread(target=prompt_info_prompt, args=(current_indicator,)).start()


        prompt_interval_minute = CONFIG["prompt_interval_minute"]
        minimum_prompt_level = CONFIG["minimum_prompt_level"]

        initiate_time = time.time()
        trigger_initiate_time = initiate_time
        last_recorded_minute = 0
        continuous_listening = False
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            frame = self.fatigue_detector.update(frame)

            # 记录检测时间
            current_time = time.time() - initiate_time
            current_minute = round(current_time / 60, 2)

            # 根据提示间隔提示 Decimal解决浮点计算不精确问题
            trigger_current_time = time.time() - trigger_initiate_time
            trigger_current_minute = round(trigger_current_time / 60, 2)
            trigger_time = Decimal(str(trigger_current_minute)) % Decimal(str(prompt_interval_minute))
            if continuous_listening:
                trigger_initiate_time = time.time()

            if (trigger_time == 0 and last_recorded_minute != current_minute) or continuous_listening:
                last_recorded_minute = current_minute

                fatigue_indicator = self.fatigue_detector.get_indicator()
                if minimum_prompt_level <= fatigue_indicator:
                    prompt_mode(fatigue_indicator)
                    continuous_listening = False
                else:
                    continuous_listening = True

            # 显示信息
            show_frame(frame)
            show_fatigue_info(self.fatigue_detector,
                              current_minute, trigger_time, prompt_interval_minute)

            cv2.waitKey(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
