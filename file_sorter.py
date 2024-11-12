import os
import shutil


def copy_needed_images(src, end):
    if os.listdir(end) != 0:
        with os.scandir(end) as it:
            for entry in it:
                os.remove(entry)

    with os.scandir(src) as it:
        for entry in it:
            filename = os.path.basename(entry)
            frame_number = filename[filename.index('_f')+2:filename.index('_qs')]
            view_number = filename[filename.index('_v')+2:filename.index('.png')]
            if frame_number == view_number:
                shutil.copy(entry, end)
