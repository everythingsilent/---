import dlib
import os

key_points_detection_model = os.path.join(os.path.dirname(os.getcwd()),
                                          "common", "model", "shape_predictor_68_face_landmarks.dat")
# 模块路径的不统一导致无法读取
if not os.path.isfile(key_points_detection_model):
    key_points_detection_model = os.path.join(os.getcwd(),
                                              "common", "model", "shape_predictor_68_face_landmarks.dat")

predictor = dlib.shape_predictor(key_points_detection_model)


def get_face_key_points(frame, area):
    face_key_points = predictor(frame, area)
    return face_key_points


def get_left_eye_points(all_points):
    left_eye_points = {i + 1: all_points.part(i) for i in range(36, 42)}
    return left_eye_points


def get_right_eye_points(all_points):
    right_eye_points = {i + 1: all_points.part(i) for i in range(42, 48)}
    return right_eye_points


def get_yawn_points(all_points):
    yawn_points = {i + 1: all_points.part(i) for i in range(48, 68)}
    return yawn_points
