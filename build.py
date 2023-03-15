import os
import shutil

from app import app


def copy_static_files():
    static_folder = app.static_folder
    build_folder = "build"

    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)

    shutil.copytree(static_folder, build_folder)
    shutil.copy("templates/index.html", build_folder)


if __name__ == "__main__":
    copy_static_files()
