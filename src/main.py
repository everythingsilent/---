import cv2
import numpy

from common import ConfigGeneration
from indicator import IndicatorCalc

CONFIG = ConfigGeneration.get_config()

if __name__ == '__main__':
    camer= cv2.VideoCapture(CONFIG["camera_source"])
    while camer.isOpened():
        ret, frame = camer.read()



        frame, ear, mar = IndicatorCalc.get_fatigue_index(frame, True)
        if ear!=None and mar!=None:
            if ear <= CONFIG["personal_characteristics_threshold"]["eye"]:
                print("已闭眼")
            if mar >= CONFIG["personal_characteristics_threshold"]["yawn"]:
                print("哈切")

        cv2.imshow("windows", frame)
        if cv2.waitKey(1) == 27:
            break
    camer.release()

