import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def launch_script(script_name):
    try:
        subprocess.Popen(['python', script_name])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch {script_name}:\n{e}")

def launch_organiser():
    launch_script("photo_organiser_gui_v1.1.py")

def launch_folder_namer():
    launch_script("folder_namer_gui_v0.6.py")

root = tk.Tk()
root.title("Photo Tools Launcher")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title = tk.Label(frame, text="Photo Tools Launcher", font=('Arial', 16, 'bold'))
title.pack(pady=(0, 10))

organiser_btn = tk.Button(frame, text="Launch Organiser", command=launch_organiser, width=30)
organiser_btn.pack(pady=5)

namer_btn = tk.Button(frame, text="Launch Folder Naming Assistant", command=launch_folder_namer, width=30)
namer_btn.pack(pady=5)

exit_btn = tk.Button(frame, text="Exit", command=root.quit, width=30)
exit_btn.pack(pady=(10, 0))

root.mainloop()