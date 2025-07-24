
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import glob
from pathlib import Path

def get_folders_with_images(root_folder):
    supported_extensions = ('.jpg', '.jpeg', '.png')
    folders_with_images = set()
    for path in Path(root_folder).rglob("*"):
        if path.is_file() and path.suffix.lower() in supported_extensions:
            folders_with_images.add(str(path.parent.resolve()))
    return sorted(folders_with_images)

def get_preview_images(folder_path, max_images=5):
    if not folder_path:
        return []
    exts = ["*.jpg", "*.jpeg", "*.png"]
    images = []
    for ext in exts:
        images.extend(glob.glob(os.path.join(folder_path, ext)))
    return images[:max_images]

def is_folder_named(folder):
    base = os.path.basename(folder)
    return len(base) > 10 and base[10] == ' '

class FolderNamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Naming Assistant")
        self.current_folder_path = None
        self.folder_list = []

        self.title_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.title_label.pack(pady=5)

        self.thumbnail_frame = tk.Frame(root)
        self.thumbnail_frame.pack()

        self.entry = tk.Entry(root, font=("Arial", 12), width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.rename_folder)
        self.entry.focus_set()

        self.progress_label = tk.Label(root, text="Progress: 0 / 0")
        self.progress_label.pack(pady=5)


        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Rename", command=self.rename_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Skip", command=self.next_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Choose Folder", command=self.select_input_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Open in Explorer", command=self.open_in_explorer).pack(side=tk.LEFT, padx=5)

        self.root.after(100, self.select_input_folder)

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Root Folder")
        if not folder:
            return
        self.folder_list = [f for f in get_folders_with_images(folder) if not is_folder_named(f)]
        self.folder_index = 0
        self.next_folder()

    def next_folder(self):
        if self.folder_index >= len(self.folder_list):
            messagebox.showinfo("Done", "No more folders to process.")
            self.root.quit()
            return
        self.current_folder_path = self.folder_list[self.folder_index]
        self.folder_index += 1
        self.entry.delete(0, tk.END)
        self.title_label.config(text=self.current_folder_path.replace("/", "\\"))
        self.display_thumbnails()
        self.progress_label.config(text=f"Progress: {self.folder_index} / {len(self.folder_list)}")

    def rename_folder(self, event=None):
        new_name = self.entry.get().strip()
        if not new_name:
            return
        parent = os.path.dirname(self.current_folder_path)
        base = os.path.basename(self.current_folder_path)
        if len(base) >= 10:
            prefix = base[:10]
            new_folder = os.path.join(parent, f"{prefix} {new_name}")
            try:
                os.rename(self.current_folder_path, new_folder)
                self.folder_list[self.folder_index - 1] = new_folder
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename folder: {e}")
        self.next_folder()

    def display_thumbnails(self):
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        if not self.current_folder_path:
            return
        images = get_preview_images(self.current_folder_path, max_images=5)
        for img_path in images:
            try:
                img = Image.open(img_path)
                img.thumbnail((350, 350))
                tk_img = ImageTk.PhotoImage(img)
                label = tk.Label(self.thumbnail_frame, image=tk_img, bg="black")
                label.image = tk_img
                label.pack(side=tk.LEFT, padx=5)
                label.bind("<ButtonPress-1>", lambda e, p=img_path: self.show_full_image(p))
                label.bind("<ButtonRelease-1>", self.hide_full_image)
            except:
                continue

    def show_full_image(self, image_path):
        try:
            image = Image.open(image_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            image.thumbnail((screen_width, screen_height))
            self.full_image = ImageTk.PhotoImage(image)
            self.full_image_window = tk.Toplevel(self.root)
            self.full_image_window.configure(bg="black")
            self.full_image_window.attributes("-fullscreen", True)
            label = tk.Label(self.full_image_window, image=self.full_image, bg="black")
            label.pack(expand=True)
        except Exception:
            pass

    def hide_full_image(self, event=None):
        if hasattr(self, 'full_image_window') and self.full_image_window:
            self.full_image_window.destroy()

    def open_in_explorer(self):
        if self.current_folder_path:
            os.startfile(self.current_folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderNamerApp(root)
    root.mainloop()
