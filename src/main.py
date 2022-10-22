import cv2
import numpy

from common import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()

if __name__ == '__main__':
    fatigue_indicator = IndicatorCalc.Fatigue()

    camer= cv2.VideoCapture(CONFIG["camera_source"])
    while camer.isOpened():
        ret, frame = camer.read()

        frame = fatigue_indicator.update(frame)

        # 每分钟进行重置并显示疲劳指标
        if fatigue_indicator.total_time >= 60:
            print(fatigue_indicator.get_indicator())
            fatigue_indicator.show_info()
            fatigue_indicator.__init__()

        cv2.imshow("windows", frame)
        if cv2.waitKey(1) == 27:
            break
    camer.release()

