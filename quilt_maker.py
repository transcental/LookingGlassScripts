from PIL import Image
from tkinter import ttk

import os
import tkinter as tk

root = tk.Tk()

root.geometry("750x200")
selected_var = tk.StringVar()

LOOKING_GLASS_NAMES = [
    "Go",
    "Portrait",
    '16" Landscape',
    '16" Portrait',
    '32" Landscape',
    '32" Portrait',
    '65"',
]

# Lookup table to match quilt ratio to target display
LOOKING_GLASS_QUILT_LAYOUTS = [
    [11, 6],
    [8, 6],
    [7, 7],
    [11, 6],
    [7, 7],
    [11, 6],
    [8, 9],
]


def get_input_info():
    # Get the selected option's index from the dropdown
    selected_option = selected_var.get()

    # Pass the target directory and target display index
    make_quilt(dir_path.get(), LOOKING_GLASS_NAMES.index(selected_option))


label = ttk.Label(
    root,
    text="Please Input target device and the file path of the images to be formatted.",
)
label.pack(pady=10)
# Create the dropdown (Combobox) and set the options
dropdown = ttk.Combobox(root, textvariable=selected_var, values=LOOKING_GLASS_NAMES)
dropdown.current(0)  # Set the default selected option to the first item
dropdown.pack(pady=10)

# Create an entry for the directory path
dir_path = tk.StringVar()
dir_path_entry = ttk.Entry(root, textvariable=dir_path, width=40)
dir_path_entry.pack(pady=10)
dir_path_entry.insert(0, "Enter directory path here")  # Placeholder text

# Create the "Make Quilt" button
make_quilt_button = tk.Button(root, text="Make Quilt", command=get_input_info)
make_quilt_button.pack(pady=20)


def make_quilt(path, targetDisplayIndex):

    # Find quilt ratio of target display
    total_columns = LOOKING_GLASS_QUILT_LAYOUTS[targetDisplayIndex][0]
    total_rows = LOOKING_GLASS_QUILT_LAYOUTS[targetDisplayIndex][1]
    size_of_quilts = LOOKING_GLASS_QUILT_LAYOUTS[targetDisplayIndex][0] * LOOKING_GLASS_QUILT_LAYOUTS[targetDisplayIndex][1]

    # Creates the layout for the quilt filling the columns and rows with '-'
    # ["-" for columns in range(total_columns)] make a list of '-' with a length of total_columns
    # for rows in range(total_rows) do the above total_rows times
    quilt_layout = [
        ["-" for columns in range(total_columns)] for rows in range(total_rows)
    ]
    current_row = 0
    current_column = 0

    #with os.scandir(path) as directory:
    # print(f'{directory=}')
    # for item in directory:
    #     print(f'{item=}')

    # Get everything in the target directory
    ############ no protection from blender quilts
    dir = sorted(os.listdir(path))
    number_of_quilts = len(dir) / size_of_quilts
    for quilt_itorator in range(int(number_of_quilts)):
        for i in range(size_of_quilts):
            # Replace the '-' with the image
            if "_v" in str(dir[i+size_of_quilts*quilt_itorator]): ########protection from blender quilts but too late
                # print(f'angle {i}')
                quilt_layout[current_row][current_column] = path + '\\'*(path[-1]!='\\') + dir[i+size_of_quilts*quilt_itorator]
                current_column += 1
                if current_column == total_columns:
                    current_column = 0
                    current_row += 1
            else:
                print(dir[i+size_of_quilts*quilt_itorator])
        current_row = 0
        # Find the size of a single image
       # print(quilt_layout)

        image_width, image_height = Image.open(quilt_layout[0][0]).size
        # Extrapolate that to the width and height that the quilt will need to be
        quilt_width = image_width * total_columns
        quilt_height = image_height * total_rows

        # Create an empty image to save the quilt into
        quilt = Image.new("RGBA", (quilt_width, quilt_height))
        quiltMap = quilt.load()

        current_width = 0
        current_height = 0
        for row in range(total_rows):
            current_width = 0
            for column in range(total_columns):

                # Open the next image to be copied onto the quilt
                current_image = Image.open(quilt_layout[row][column])
                current_image_map = current_image.load()

                # Copy each pixel from the image to the quilt
                for x in range(image_width):
                    for y in range(image_height):
                        # current_width and current_height are the offset added to x and y so they are in the correct column and row on the quilt
                        quiltMap[
                            current_width + x, (quilt_height - 1) - (current_height + y)
                        ] = current_image_map[x, (image_height - 1) - y]
                current_width = image_width * (column + 1)
            current_height = image_height * (row + 1)

        # quilt.show()

        print(f"Quilt {quilt_itorator} has been saved")
        quilt.save(f"quilt/{quilt_itorator}.png")


root.mainloop()