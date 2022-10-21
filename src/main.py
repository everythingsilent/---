import cv2
import numpy

from common import ConfigGeneration
from indicator import AspectRatioCalc, IndicatorCalc

CONFIG = ConfigGeneration.get_config()

def show_threshold_info(ear,mar):
    if ear != None and mar != None:
        if ear <= CONFIG["personal_characteristics_threshold"]["eye"]:
            print("已闭眼")
        if mar >= CONFIG["personal_characteristics_threshold"]["yawn"]:
            print("哈切")


if __name__ == '__main__':
    total_frame = 0


    camer= cv2.VideoCapture(CONFIG["camera_source"])
    while camer.isOpened():
        ret, frame = camer.read()
        total_frame += 1

        frame, ear, mar = AspectRatioCalc.get_aspect_ratio(frame)
        show_threshold_info(ear, mar)



        cv2.imshow("windows", frame)
        if cv2.waitKey(1) == 27:
            break
    camer.release()

