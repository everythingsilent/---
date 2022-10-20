import cv2
import os
import dlib

face_detection_model = os.path.join(os.path.dirname(os.getcwd()),
                                    "common", "model", "haarcascade_frontalface_alt.xml")
#模块路径的不统一导致无法读取
if not os.path.isfile(face_detection_model):
    face_detection_model = os.path.join(os.getcwd(),
                                        "common", "model", "haarcascade_frontalface_alt.xml")

detector = cv2.CascadeClassifier(face_detection_model)


def get_face_area_n(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #<class 'numpy.ndarray'> [[322 155 249 249]]
    face_area_n = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    return face_area_n


def face_area_numpy_to_dlib(face_area_n):
    face_area_dlib = []
    if face_area_n != tuple():
        for i in range(len(face_area_n)):
            left, right = face_area_n[i][0], face_area_n[i][0] + face_area_n[i][2]
            up, down = face_area_n[i][1], face_area_n[i][1] + face_area_n[i][3]+25

            try:
                face_area_dlib.append(dlib.rectangle(int(left), int(up), int(right), int(down)))
            except:
                print("numpy转dlib数据失败")
                raise Exception

    #[rectangle(278,274,451,447)]
    return face_area_dlib