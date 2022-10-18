import cv2

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)


    while capture.isOpened():
        ret, frame = capture.read()
        cv2.imshow("main window", frame)

        if cv2.waitKey(1) == 27:
            break

    capture.release()
