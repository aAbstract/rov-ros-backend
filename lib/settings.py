import json


def get_settings() -> dict:
    _settings_obj = None

    with open('./settings.json', 'r') as f:
        set_json_txt = f.read()
        _settings_obj = json.loads(set_json_txt)

    return _settings_obj
