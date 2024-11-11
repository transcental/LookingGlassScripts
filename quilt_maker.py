import os
import tkinter as tk
from tkinter import ttk
import shutil
from PIL import Image

root = tk.Tk()

root.geometry("750x200")
selectedVar = tk.StringVar()

lookingGlassNames = [
    "Go",
    "Portrait",
    "16' Landscape",
    "16' Portrait",
    "32' Landscape",
    "32' Portrait",
    "65'"]

#Lookup table to match quilt ratio to target display
lookingGlassQuiltLayouts = [
    [11,6],
    [8,6],
    [7,7],
    [11,6],
    [7,7],
    [11,6],
    [8,9]]

def GetInputInfo():
    # Get the selected option's index from the dropdown
    selectedOption = selectedVar.get()

    #Pass the target directory and target display index
    MakeQuilt(dirPathVar.get(), lookingGlassNames.index(selectedOption))

label = ttk.Label(root, text = "Please Input target device and the file path of the images to be formatted.")
label.pack(pady = 10)
# Create the dropdown (Combobox) and set the options
dropdown = ttk.Combobox(root, textvariable=selectedVar, values=lookingGlassNames)
dropdown.current(0)  # Set the default selected option to the first item
dropdown.pack(pady=10)

# Create an entry for the directory path
dirPathVar = tk.StringVar()
dirPathEntry = ttk.Entry(root, textvariable=dirPathVar, width=40)
dirPathEntry.pack(pady=10)
dirPathEntry.insert(0, "Enter directory path here")  # Placeholder text

# Create the "Make Quilt" button
makeQuiltButton = tk.Button(root, text="Make Quilt", command=GetInputInfo)
makeQuiltButton.pack(pady=20)

def MakeQuilt(path, targetDisplayIndex):
    #Find quilt ratio of target display
    totalColumns = lookingGlassQuiltLayouts[targetDisplayIndex][0]
    totalRows = lookingGlassQuiltLayouts[targetDisplayIndex][1]

    #Creates the layout for the quilt filling the columns and rows with '-'
    #["-" for columns in range(totalColumns)] make a list of '-' with a length of totalColumns
    #for rows in range(totalRows) do the above totalRows times
    quiltLayout = [["-" for columns in range(totalColumns)] for rows in range(totalRows)]
    currentRow = 0
    currentColumn = 0

    #Get everything in the target directory
    with os.scandir(path) as directory:
        for entry in directory:
            #Replace the '-' with the image
            if '_v' in str(entry):
                quiltLayout[currentRow][currentColumn] = entry
                currentColumn += 1
                if(currentColumn == totalColumns):
                    currentColumn = 0
                    currentRow += 1
                
            else:
                print(entry)

    #Find the size of a single image
    imageWidth, imageHeight = Image.open(quiltLayout[0][0]).size
    #Extrapolate that to the width and height that the quilt will need to be
    quiltWidth = imageWidth * totalColumns
    quiltHeight = imageHeight * totalRows

    #Create an empty image to save the quilt into
    quilt = Image.new("RGBA", (quiltWidth,quiltHeight))
    quiltMap = quilt.load()

    currentWidth = 0
    currentHeight = 0
    for row in range(totalRows):
        currentWidth= 0
        for column in range(totalColumns):

            #Open the next image to be copied onto the quilt
            currentImage = Image.open(quiltLayout[row][column])
            currentImageMap = currentImage.load()

            #Copy each pixel from the image to the quilt
            for x in range(imageWidth):
                for y in range(imageHeight):
                    #currentWidth and currentHeight are the offset added to x and y so they are in the correct column and row on the quilt
                    quiltMap[currentWidth +x, (quiltHeight -1) - (currentHeight +y)] = currentImageMap[x, (imageHeight -1) -y]
            currentWidth = imageWidth * (column + 1)
        currentHeight = imageHeight * (row + 1)

    quilt.show()

    quilt.save("finalQuilt.png")

root.mainloop()
