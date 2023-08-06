from pathlib import Path


def project_root() -> Path:
    return Path(__file__).parent


def resource_dir() -> Path:
    return project_root() / 'resource'


def remote_associates_dir() -> Path:
    return project_root() / 'rat' / 'remote_associates'


def nback_stimulus_dir() -> Path:
    return project_root() / 'nback' / 'stimulus'


font = 'Arial'
