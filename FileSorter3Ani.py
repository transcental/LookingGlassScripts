import os
import shutil


file_directories = []
for i in range(3):
    file_directories.append(input(f"Starting Directory {i}:  "))
file_directory_end = input("Ending Directory:  ")
total_frames = int(input("Total Frames:  "))


for i in range(3):
    for entry in file_directories[i]:
        filename = os.path.basename(entry)
        current_frame = int(filename[21] + filename[22])
        if(current_frame < total_frames * (i + 1) and current_frame >= total_frames * i):
            shutil.copy(entry, file_directory_end)