import time

from  indicator import AspectRatioCalc, IndicatorFusion
import ConfigGeneration

CONFIG = ConfigGeneration.get_config()

class Fatigue:
    def __init__(self):
        self.total_frame = 0
        self.total_time = 0
        self.total_close_eye_frame = 0
        self.total_close_eye_time = 0
        self.total_close_eye_count = 0
        self.total_yawn_count = 0

        # 记录触发阈值连续帧，判断该连续的帧，属于同一眨眼，打哈切次数
        self.consecutive_frames_eye = 0
        self.consecutive_frames_yawn = 0


    def get_indicator(self):
        preclos = self.get_perclos()
        avg_close_eye_time = self.get_avg_close_time()
        avg_yawn_count = self.get_avg_yawn_count()

        f_preclos = IndicatorFusion.perclos_level(preclos)
        f_avg_close_eye_time = IndicatorFusion.avg_close_eye_level(avg_close_eye_time)
        f_avg_yawn_count = IndicatorFusion.yawn_level(avg_yawn_count)

        fatigue_indicator = IndicatorFusion.fusion_algorithm(f_preclos,
                                                             f_avg_close_eye_time,
                                                             f_avg_yawn_count)
        return fatigue_indicator


    def get_avg_yawn_count(self):
        minute = int(self.total_time/60) if int(self.total_time/60) > 0 else 1
        avg_yawn_count = round(self.total_yawn_count/minute, 3)
        return avg_yawn_count


    def get_perclos(self):
        total_frame = self.total_frame if self.total_frame != 0 else 1
        preclos = round(self.total_close_eye_frame/total_frame, 3)
        return preclos


    def get_avg_close_time(self):
        close_eye_count = self.total_close_eye_count if self.total_close_eye_count >0 else 1
        avg_close_time = round(self.total_close_eye_time/close_eye_count, 3)
        return avg_close_time


    def get_fps(self):
        total_time = self.total_time if self.total_time > 0 else 1
        fps = int(self.total_frame/total_time)
        return fps


    def show_info(self):
        print(self.get_perclos(), self.get_avg_close_time(), self.get_avg_yawn_count(), self.get_fps())


    def update_close_eye(self, ear, process_time):
        if ear <= CONFIG["personal_characteristics_threshold"]["eye"]:
            self.total_close_eye_frame+=1
            self.consecutive_frames_eye+=1
            self.total_close_eye_time+=process_time
            if self.consecutive_frames_eye == 1:
                self.total_close_eye_count+=1
        else:
            self.consecutive_frames_eye = 0


    def update_yawn(self, mar):
        if mar >= CONFIG["personal_characteristics_threshold"]["yawn"]:
            self.consecutive_frames_yawn+=1
            if self.consecutive_frames_yawn == 5:
                self.total_yawn_count += 1
        else:
            self.consecutive_frames_yawn = 0


    def update(self, frame):
        # 计算获取ear与mar的过程时间，即当前帧的时间
        start_time = time.time()
        frame, ear, mar = AspectRatioCalc.get_aspect_ratio(frame,
                                                           show_face_area=bool(CONFIG["frame_display"]["show_face_area"]),
                                                           show_face_points=bool(CONFIG["frame_display"]["show_face_points"]))
        end_time = time.time()
        process_time = end_time - start_time

        if (ear != None) and (mar != None):
            self.total_frame+=1
            self.total_time+=process_time

            self.update_close_eye(ear, process_time)
            self.update_yawn(mar)
        return frame