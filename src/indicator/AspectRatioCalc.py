import numpy
import cv2

from faceKeyPoints import KeyPointsDetection
from faceArea import FaceDetection
import ConfigGeneration

CONFIG = ConfigGeneration.get_config()


def get_ear(left_eye, right_eye):
    left_a = abs(left_eye[38].y - left_eye[42].y)
    left_b = abs(left_eye[39].y - left_eye[41].y)
    left_c = 2 * abs(left_eye[37].x - left_eye[40].x)
    left_ear = (left_a + left_b) / left_c

    right_a = abs(right_eye[44].y - right_eye[48].y)
    right_b = abs(right_eye[45].y - right_eye[47].y)
    right_c = 2 * abs(right_eye[43].x - right_eye[46].x)
    right_ear = (right_a + right_b) / right_c

    ear = round(numpy.average([left_ear, right_ear]), 2)
    return ear


def get_mar(yawn):
    mar = round(((yawn[51].y - yawn[59].y) + (yawn[53].y - yawn[57].y)) /
                (2 * (yawn[49].x - yawn[55].x)), 2)
    return mar


def draw_face_points(frame, face_key_points):
    for i in range(36, 68):
        cv2.circle(frame, (face_key_points.part(i).x, face_key_points.part(i).y),
                   1, (255, 255, 255), -1)
    return frame


def draw_face_ares(frame, face_areas):
    for area in face_areas:
        left, right = area[0], area[2]
        up, down = area[1], area[3] + 25
        frame = cv2.rectangle(frame, (left, up, right, down), (255, 255, 255), 1)
    return frame


def calc_aspect_ratio(face_key_points):
    left_eye = KeyPointsDetection.get_left_eye_points(face_key_points)
    right_eye = KeyPointsDetection.get_right_eye_points(face_key_points)
    yawn = KeyPointsDetection.get_yawn_points(face_key_points)

    ear = get_ear(left_eye, right_eye)
    mar = get_mar(yawn)
    return ear, mar


def get_aspect_ratio(frame, show_face_area=True, show_face_points=True):
    face_areas = FaceDetection.get_face_area_n(frame)
    face_areas_dlib = FaceDetection.face_area_numpy_to_dlib(face_areas)

    if show_face_area:
        frame = draw_face_ares(frame, face_areas)

    for area_dlib in face_areas_dlib:
        face_key_points = KeyPointsDetection.get_face_key_points(frame, area_dlib)

        if show_face_points:
            frame = draw_face_points(frame, face_key_points)

        ear, mar = calc_aspect_ratio(face_key_points)

        # break 只返回一个人的眼睑，嘴部纵横比
        return frame, ear, mar

    return frame, None, None
