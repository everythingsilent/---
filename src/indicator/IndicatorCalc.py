import cv2

from faceArea import FaceDetection
from faceKeyPoints import KeyPointsDetection
from indicator import ThresholdCalc
from common import ConfigGeneration

CONFIG = ConfigGeneration.get_config()


def draw_face_points(frame, face_key_points):
    for i in range(37,68):
        cv2.circle(frame, (face_key_points.part(i).x, face_key_points.part(i).y), 1, (255, 255, 255), -1)
    return frame


def draw_face_ares(frame, face_areas):
    for area in face_areas:
        left, right = area[0], area[2]
        up, down = area[1], area[3] + 25
        frame = cv2.rectangle(frame, (left, up, right, down), (255, 255, 255), 1)
    return frame


def get_fatigue_index(frame, show):

    face_areas = FaceDetection.get_face_area_n(frame)
    face_areas_dlib = FaceDetection.face_area_numpy_to_dlib(face_areas)

    if show:
        frame = draw_face_ares(frame, face_areas)

    for area_dlib in face_areas_dlib:
        face_key_points = KeyPointsDetection.get_face_key_points(frame, area_dlib)

        if show:
            frame = draw_face_points(frame, face_key_points)

        left_eye = KeyPointsDetection.get_left_eye_points(face_key_points)
        right_eye = KeyPointsDetection.get_right_eye_points(face_key_points)
        yawn = KeyPointsDetection.get_yawn_points(face_key_points)

        ear = ThresholdCalc.get_ear(left_eye, right_eye)
        mar = ThresholdCalc.get_mar(yawn)

        # break
        return frame, ear, mar
    return frame, None, None