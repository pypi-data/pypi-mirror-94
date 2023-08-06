import csv
import os
import subprocess
import time
from pathlib import Path
from platform import system


def _get_desktop_win():
    try:
        from win32com.shell import shell, shellcon

        desktop_folder = Path(
            shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0))
    except ModuleNotFoundError:
        desktop_folder = Path.home() / 'Desktop'

    return desktop_folder


def _get_desktop_nix():
    desktop_folder = Path.home() / 'Desktop'
    return desktop_folder


def _open_file_win(file_path):
    os.startfile(file_path)


def _open_file_nix(file_path):
    opener = "open" if system() == "darwin" else "xdg-open"
    subprocess.call([opener, str(file_path)])


def read_csv(file_path, encoding='utf-8', add_index=True):
    temp = []
    with open(file_path, encoding=encoding) as f:
        reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(reader):
            if add_index:
                row.insert(0, i)
            temp.append(row)
    return temp


def save_csv(file_path, data, header=None, encoding='utf-8'):
    with open(file_path, mode='w', encoding=encoding, newline='') as f:
        writer = csv.writer(f, delimiter=',')
        if header:
            writer.writerow(header)
        for row in data:
            writer.writerow(row)


def change_encoding(file_path, source_encoding='shift-jis',
                    target_encoding='utf-8'):
    temp_file = file_path.parent / '~temp'
    with open(file_path, 'r', encoding=source_encoding) as f, \
            open(temp_file, 'w', encoding=target_encoding) as e:
        text = f.read()
        e.write(text)
    file_path.unlink()
    temp_file.rename(file_path)


def convert_time(seconds):
    return time.strftime("%M:%S", time.gmtime(seconds))


if system() == 'Windows':
    get_desktop = _get_desktop_win
    open_file = _open_file_win
else:
    get_desktop = _get_desktop_nix
    open_file = _open_file_nix
