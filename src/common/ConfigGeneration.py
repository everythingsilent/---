import os
import json

config_root = os.getcwd()
config_url = os.path.join(config_root, "config.json")

if not os.path.isfile(config_url):
    config_url = os.path.join(config_root,
                              "common", "config.json")

def set_config(camera_source=0,
                 prompt_mode={"voice_broadcast":1, "windows_warning":1, "info tips":1},
                 minimum_prompt_level=1,
                 personal_characteristics_threshold={"eye":0.20, "yawn":1.12}):

    try:
        config_data = {"camera_source":camera_source, "prompt_mode":prompt_mode,
                       "minimum_prompt_level":minimum_prompt_level,
                       "personal_characteristics_threshold":personal_characteristics_threshold}
        config_json = json.dumps(config_data)

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
