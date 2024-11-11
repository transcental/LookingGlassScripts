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
            frame_number = filename[21] + filename[22]
            angle_number = filename[37] + filename[38]
            if frame_number == angle_number:
                shutil.copy(entry, end)
