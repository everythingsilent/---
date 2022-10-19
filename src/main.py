import cv2
import numpy
from faceArea import FaceDetection
from faceKeyPoints import KeyPointsDetection
from indicator import ThresholdCalc
from common import ConfigGeneration

CONFIG  = ConfigGeneration.get_config()

def get_key_points(all_points):
    try:
        left_eye_point = KeyPointsDetection.get_left_eye_points(all_points)
        right_eye_point = KeyPointsDetection.get_right_eye_points(all_points)
        yawn_point = KeyPointsDetection.get_yawn_points(all_points)
        return left_eye_point, right_eye_point, yawn_point
    except:
        print("所有关键点获取失败")
        return None

def face_detection(frame):

    try:
        face_area_n = FaceDetection.get_face_area_n(frame)
        face_area_dlibs = FaceDetection.face_area_numpy_to_dlib(face_area_n)

        # face_area_n = [numpy.array([322,155,249,249])] #测试
    except:
        print("人脸区域获取失败")

    if face_area_n != tuple():
        for i in range(len(face_area_n)):
            left, right = face_area_n[i][0], face_area_n[i][2]
            up, down = face_area_n[i][1], face_area_n[i][3]+25

            frame = cv2.rectangle(frame, (left, up, right, down), (255, 255, 255), 1)

            try:
                all_points = KeyPointsDetection.get_face_key_points(frame, face_area_dlibs[i])
                left_eye, right_eye, yawn = get_key_points(all_points)

                #draw left_eye
                for i in range(37,68):
                    cv2.circle(frame, (all_points.part(i).x, all_points.part(i).y), 1, (255,255,255), -1)


                eye_threshold = ThresholdCalc.get_eye_threshold(left_eye, right_eye)
                yawn_threshold = ThresholdCalc.get_yawn_threshold(yawn)

                #"personal_characteristics_threshold": {"eye": 0.2, "yawn": 1.12}
                if eye_threshold <= CONFIG["personal_characteristics_threshold"]["eye"]:
                    print("已闭眼")

                if yawn_threshold >= CONFIG["personal_characteristics_threshold"]["yawn"]:
                    print("哈切")

            except:
                print("阈值计算关键点获取失败")

            break

    return frame


def show_windows(capture):
    while True:
        ret, frame = capture.read()
        frame = face_detection(frame)
        cv2.imshow("main window", frame)

        if cv2.waitKey(1) == 27:
            break


def open_capture():
    capture = cv2.VideoCapture(CONFIG["camera_source"])
    if capture.isOpened():
        show_windows(capture)
        capture.release()
    else:
        raise Exception


if __name__ == '__main__':
    try:
        open_capture()
    except:
        print("摄像头打开失败")


