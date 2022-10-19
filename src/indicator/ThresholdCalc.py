import numpy


def get_eye_threshold(left_eye, right_eye):
    left_a = abs(left_eye[38].y - left_eye[42].y)
    left_b = abs(left_eye[39].y - left_eye[41].y)
    left_c = 2 * abs(left_eye[37].x - left_eye[40].x)
    left_eye_threshold = (left_a + left_b) / left_c

    right_a = abs(right_eye[44].y - right_eye[48].y)
    right_b = abs(right_eye[45].y - right_eye[47].y)
    right_c = 2 * abs(right_eye[43].x - right_eye[46].x)
    right_eye_threshold = (right_a + right_b) / right_c

    eye_threshold = round(numpy.average([left_eye_threshold, right_eye_threshold]), 2)
    return eye_threshold


def get_yawn_threshold(yawn):
    yawn_threshold = round(((yawn[51].y - yawn[59].y) + (yawn[53].y - yawn[57].y)) /
                           (2 * (yawn[49].x - yawn[55].x)), 2)

    return yawn_threshold
