import cv2
import numpy
import time


from common import ConfigGeneration
from indicator import IndicatorCalc


CONFIG = ConfigGeneration.get_config()


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


if __name__ == '__main__':
    fatigue_indicator = IndicatorCalc.Fatigue()

    camer= cv2.VideoCapture(CONFIG["camera_source"])
    prompt_interval_minute = CONFIG["prompt_interval_minute"]
    minimum_prompt_level = CONFIG["minimum_prompt_level"]

    initiate_time = time.time()
    last_recorded_minute = 0
    while camer.isOpened():
        ret, frame = camer.read()
        frame = fatigue_indicator.update(frame)

        # 根据提示间隔提取指标并提示
        current_minute = round((time.time()-initiate_time)/60, 2)
        if current_minute%prompt_interval_minute == 0 and last_recorded_minute!=current_minute:
            last_recorded_minute = current_minute

            # 当前指标对应提示方式
            current_indicator = fatigue_indicator.get_indicator()
            if minimum_prompt_level >= current_indicator:
                prompt_mode(current_indicator)
                fatigue_indicator.show_info()
                print(current_indicator)

        cv2.imshow("windows", frame)
        if cv2.waitKey(1) == 27:
            break
    camer.release()

