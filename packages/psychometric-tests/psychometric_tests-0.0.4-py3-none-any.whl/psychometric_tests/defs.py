import json
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).parent


def resource_dir() -> Path:
    return project_root() / 'resource'


def remote_associates_dir() -> Path:
    question_dir = settings()['rat']['question_dir']
    if question_dir:
        return Path(question_dir).resolve()
    else:
        return project_root() / 'rat' / 'remote_associates'


def nback_stimulus_dir() -> Path:
    stimulus_dir = settings()['nback']['stimulus_dir']
    if stimulus_dir:
        return Path(stimulus_dir).resolve()
    else:
        return project_root() / 'nback' / 'stimulus'


def settings() -> dict:
    settings_file = project_root() / 'settings.json'
    with open(settings_file) as f:
        s = json.load(f)

    for t, w in [('ant', 'font_weight'),
                 ('rat', 'title_font_weight'),
                 ('rat', 'ques_font_weight'),
                 ('rat', 'answer_font_weight'),
                 ('rat', 'sol_font_weight'),
                 ('nback', 'stimulus_font_weight'),
                 ('nback', 'answer_font_weight')]:
        if type(s[t][w]) is str:
            s[t][w] = fontweight_enum[s[t][w]]

    return s


def update_settings(test, setting, val):
    settings_file = project_root() / 'settings.json'
    with open(settings_file) as f:
        s = json.load(f)

    s[test][setting] = val

    with open(settings_file, 'w') as f:
        json.dump(s, f, sort_keys=False, indent=2)


fontweight_enum = {'Thin': 0,
                   'ExtraLight': 12,
                   'Light': 25,
                   'Normal': 50,
                   'Medium': 57,
                   'DemiBold': 63,
                   'Bold': 75,
                   'ExtraBold': 81,
                   'Black': 87,
                   }
