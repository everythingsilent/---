import os
import json

config_root = os.getcwd()
config_url = os.path.join(config_root,
                              "common", "config.json")


def set_config(camera_source=0,
                 prompt_mode={"voice_broadcast":1, "windows_warning":1, "info_prompt":0},
                 minimum_prompt_level=1,
                 personal_characteristics_threshold={"eye":0.20, "yawn":1.12},
                 prompt_interval_minute=10,
                 frame_display={"show_face_area":1, "show_face_points":1}):

    try:
        config_data = {"camera_source":camera_source,
                       "prompt_mode":prompt_mode,
                       "minimum_prompt_level":minimum_prompt_level,
                       "personal_characteristics_threshold":personal_characteristics_threshold,
                       "prompt_interval_minute":prompt_interval_minute,
                       "frame_display":frame_display}
        config_json = json.dumps(config_data, sort_keys=True, indent=4, separators=(',', ':'))

        config_file = open(config_url, 'w')
        config_file.write(config_json)
        config_file.close()
        return True
    except:
        return False


def get_config():
    try:
        config_file = open(config_url, 'r')
        config_json = config_file.read()
        config_data = json.loads(config_json)
        return config_data
    except:
        return None


# set_config()