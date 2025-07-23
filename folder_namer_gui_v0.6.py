
import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def get_preview_images(folder_path, max_images=5):
    if not folder_path:
        return []
    image_extensions = ['.jpg', '.jpeg', '.png']
    images = []
    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(folder_path, f"*{ext}")))
    return images[:max_images]

class FolderNamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Naming Assistant")

        self.folder_list = []
        self.folder_index = 0
        self.current_folder_path = None
        self.thumbnails = []
        self.thumbnail_labels = []

        self.title_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

        self.canvas = tk.Canvas(root, bg="lightgrey", height=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.resize_thumbnails)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)

        self.entry = tk.Entry(self.controls_frame, width=40)
        self.entry.grid(row=0, column=0, padx=5)

        self.rename_button = tk.Button(self.controls_frame, text="Rename Folder", command=self.rename_folder)
        self.rename_button.grid(row=0, column=1, padx=5)

        self.skip_button = tk.Button(self.controls_frame, text="Skip", command=self.skip_folder)
        self.skip_button.grid(row=0, column=2, padx=5)

        self.explorer_button = tk.Button(self.controls_frame, text="Open in Explorer", command=self.open_in_explorer)
        self.explorer_button.grid(row=0, column=3, padx=5)

        self.change_button = tk.Button(self.controls_frame, text="Change Folder", command=self.choose_root_folder)
        self.change_button.grid(row=0, column=4, padx=5)

        self.progress_label = tk.Label(root, text="Progress: 0 / 0")
        self.progress_label.pack(pady=5)

        self.choose_root_folder()

    def choose_root_folder(self):
        selected_folder = filedialog.askdirectory(title="Select Root Folder")
        if selected_folder:
            self.folder_list = self.get_target_folders(selected_folder)
            self.folder_index = 0
            self.load_current_folder()

    def get_target_folders(self, root_folder):
        folders = []
        for dirpath, dirnames, filenames in os.walk(root_folder):
            if any(fname.lower().endswith(('.jpg', '.jpeg', '.png')) for fname in filenames):
                if not os.path.basename(dirpath).strip().count(" "):  # skip already renamed
                    folders.append(dirpath)
        return sorted(folders)

    def load_current_folder(self):
        if self.folder_index >= len(self.folder_list):
            messagebox.showinfo("Done", "All folders have been processed.")
            self.root.quit()
            return

        self.current_folder_path = self.folder_list[self.folder_index]
        self.title_label.config(text=self.current_folder_path.replace("/", "\\"))
        self.entry.delete(0, tk.END)
        self.display_thumbnails()
        self.progress_label.config(text=f"Progress: {self.folder_index + 1} / {len(self.folder_list)}")

    def display_thumbnails(self):
        for label in self.thumbnail_labels:
            label.destroy()
        self.thumbnail_labels.clear()

        images = get_preview_images(self.current_folder_path, max_images=5)
        self.thumbnails.clear()

        for idx, img_path in enumerate(images):
            try:
                image = Image.open(img_path)
                thumb = image.copy()
                thumb.thumbnail((350, 350))
                thumb_tk = ImageTk.PhotoImage(thumb)
                label = tk.Label(self.canvas, image=thumb_tk)
                label.image = thumb_tk
                label.bind("<ButtonPress-1>", lambda e, p=img_path: self.show_full_image(p))
                label.bind("<ButtonRelease-1>", self.hide_full_image)
                label.pack(side=tk.LEFT, padx=5)
                self.thumbnail_labels.append(label)
                self.thumbnails.append(thumb_tk)
            except Exception:
                continue

    def resize_thumbnails(self, event):
        if self.current_folder_path:
            self.display_thumbnails()

    def show_full_image(self, image_path):
        try:
            image = Image.open(image_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            image.thumbnail((screen_width, screen_height))
            self.full_image = ImageTk.PhotoImage(image)
            self.full_image_window = tk.Toplevel(self.root)
            self.full_image_window.attributes("-fullscreen", True)
            label = tk.Label(self.full_image_window, image=self.full_image)
            label.pack(expand=True)
        except Exception:
            pass

    def hide_full_image(self, event=None):
        if hasattr(self, 'full_image_window') and self.full_image_window:
            self.full_image_window.destroy()

    def rename_folder(self):
        new_name = self.entry.get().strip()
        if not new_name:
            return
        new_folder_name = f"{os.path.basename(self.current_folder_path)} {new_name}"
        new_path = os.path.join(os.path.dirname(self.current_folder_path), new_folder_name)
        if os.path.exists(new_path):
            messagebox.showerror("Exists", f"Folder already exists: {new_folder_name}")
            return
        try:
            os.rename(self.current_folder_path, new_path)
            self.folder_list[self.folder_index] = new_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename: {e}")
            return
        self.folder_index += 1
        self.load_current_folder()

    def skip_folder(self):
        self.folder_index += 1
        self.load_current_folder()

    def open_in_explorer(self):
        if self.current_folder_path:
            os.startfile(self.current_folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderNamerApp(root)
    root.mainloop()
