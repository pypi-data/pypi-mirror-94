import requests
import zipfile
import io
import os
import pathlib


FOLDER = "/Users/phillipdupuis/repos/dtale-desktop/.crap"


def main():
    url = "https://github.com/phillipdupuis/dtale-desktop/archive/master.zip"
    response = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall(FOLDER)
    p = pathlib.Path(FOLDER)


def get_remote_loaders(path: str) -> None:
    url, folder = path.split("::")
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(FOLDER)
    p = pathlib.Path(FOLDER)
    sub_folders = list(p.iterdir())
    assert len(sub_folders) == 1
    f = p.joinpath(sub_folders[0], *folder.split("/"))
    print(f)


if __name__ == "__main__":
    target = "https://github.com/phillipdupuis/dtale-desktop/archive/master.zip::dtale_desktop/default_sources"
    get_remote_loaders(target)
