import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil

# Define CreateWidgets() function to create the Tkinter GUI components
def CreateWidgets():
    link_Label = Label(root, text="Select the image to detect:", bg="#E8D579")
    link_Label.grid(row=1, column=0, pady=5, padx=5)

    root.sourceText = Entry(root, width=50, textvariable=sourcePath)
    root.sourceText.grid(row=2, column=0, pady=5, padx=5, sticky=W+E)

    source_browseButton = Button(root, text="Select Image", command=SourceBrowse)
    source_browseButton.grid(row=2, column=1, pady=5, padx=5)

    weight_Label = Label(root, text="Select the weights:", bg="#E8D579")
    weight_Label.grid(row=3, column=0, pady=5, padx=5)

    root.weightText = Entry(root, width=50, textvariable=weightPath)
    root.weightText.grid(row=4, column=0, pady=5, padx=5, sticky=W+E)

    weight_browseButton = Button(root, text="Select Weights", command=WeightBrowse)
    weight_browseButton.grid(row=4, column=1, pady=5, padx=5)

    detectButton = Button(root, text="Start Detection", command=Detect)
    detectButton.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

    downloadButton = Button(root, text="Download Detected Image", command=DownloadImage, state=DISABLED)
    downloadButton.grid(row=7, column=0, columnspan=2, pady=5, padx=5)
    root.downloadButton = downloadButton  # store it in root to access later


def WeightBrowse():
    file = filedialog.askopenfilename(initialdir=".")
    weightPath.set(file)


def SourceBrowse():
    file = filedialog.askopenfilename(initialdir=".")
    sourcePath.set(file)

def Detect():
    imagePath = sourcePath.get().strip()  # Get and remove any leading/trailing whitespace
    weights_path = weightPath.get().strip()

    # Validate the image file path
    if not imagePath or not os.path.isfile(imagePath):
        messagebox.showerror("Error", "Invalid image file path!")
        return

    # Validate the weights file path
    if not weights_path or not os.path.isfile(weights_path):
        messagebox.showerror("Error", "Invalid weights file path!")
        return

    # Use quotes to ensure any special characters or spaces in the path are handled correctly
    cmd = f'python detect.py --source "{imagePath}" --weights "{weights_path}"'
    
    exit_code = os.system(cmd)

    # Check the command's exit code
    if exit_code != 0:
        messagebox.showerror("Error", "Failed to execute the detection command!")
        return

    # Determine the latest detection results directory
    detected_directory = find_latest_directory(os.path.join("runs", "detect"))
    
    # Get the path of the detected image
    detected_image_path = os.path.join(detected_directory, os.path.basename(imagePath))
    
    if not os.path.isfile(detected_image_path):
        messagebox.showerror("Error", "Failed to find the detected image!")
        return

    # Display the detected image
    LoadAndShowImage(detected_image_path)

    # Notify the user that the detection was successful
    messagebox.showinfo("Success", "Target detection complete!")

    # Enable the download button after detection
    root.downloadButton['state'] = NORMAL  
    root.detected_image_path = detected_image_path


def DownloadImage():
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    if not save_path:  # User canceled the dialog
        return
    shutil.copy(root.detected_image_path, save_path)
    messagebox.showinfo("Success", "Image saved successfully!")

def LoadAndShowImage(image_path):
    image = Image.open(image_path)
    image = image.resize((1000, 500))  # Adjust size as needed
    photo = ImageTk.PhotoImage(image)
    
    label_image = Label(root, image=photo)
    label_image.image = photo
    label_image.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


def find_latest_directory(base_path):
    # List all sub-directories
    all_subdirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    # Return the most recently modified directory
    return max(all_subdirs, key=os.path.getmtime)

# Create Tkinter window
root = tk.Tk()
root.title("YoloV5 GUI")
root.geometry("800x300")
sourcePath = StringVar()
weightPath = StringVar()
# Create Tkinter variable
sourcePath = StringVar()

# Call the function to create GUI components
CreateWidgets()

root.mainloop()
