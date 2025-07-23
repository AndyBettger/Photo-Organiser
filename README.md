# Photo Tools Suite

This repository contains a set of Python tools to help organise and label your photo library.

---

## Tools Included

### 📁 1. Photo Organiser
**File:** `photo_organiser_gui_v1.1.py`  
Sorts images and videos by date taken, renames duplicates, and uses EXIF metadata or file modification times.

### 🖼️ 2. Folder Naming Assistant
**File:** `folder_namer_gui_v0.6.py`  
Allows you to review folders of photos and append short descriptions to folder names (e.g. `2024-03-10 Beach Walk`), with thumbnail previews and a full-size click-to-enlarge feature.

### 🚀 3. Photo Tools Launcher
**File:** `photo_tools_launcher_v0.1.py`  
Simple GUI to launch either of the tools above with one click.

---

## Features

- Thumbnail previews and folder-by-folder navigation
- Smart duplicate detection and "unsure" folder for manual review
- Manual renaming tool for quick annotation of date-based folders
- One-click launcher for convenience
- EXIF-based sorting and fallback logic for unsupported formats

---

## Getting Started

### 🔧 Requirements

- Python 3.8 or later
- [Pillow](https://pypi.org/project/Pillow/)  
  Install with:
  ```
  pip install pillow
  ```

---

### 🚀 Launch Instructions

1. Clone or download the repository.
2. Open a terminal in the script folder.
3. Run the launcher:
   ```
   python photo_tools_launcher_v0.1.py
   ```
4. Use the buttons to open:
   - **Photo Organiser**
   - **Folder Naming Assistant**

---

## Optional: Running Each Tool Directly

You can also run the individual tools directly:

- Organiser:
  ```
  python photo_organiser_gui_v1.1.py
  ```

- Folder Namer:
  ```
  python folder_namer_gui_v0.6.py
  ```

# Photo Organiser

A powerful tool to organize iPhone photos and videos into dated folders using EXIF metadata or fallback to file modified dates.

## Features

- Organizes `.JPG`, `.MOV`, `.HEIC`, `.PNG`, and more
- Detects duplicates using SHA-256 or MD5 hashing
- Supports multiple input folders
- Sorts files by date taken (`YYYY/YYYY-MM-DD`)
- GUI frontend using Tkinter
- Automatically skips or deletes `Thumbs.db`
- Creates log and duplicate reports
- Optional fallback to modified date (enabled by default)
- Supports dry-run planning mode

## Usage

Simply run the GUI:
```bash
python photo_organiser_gui_v1.1.py
```

## Requirements

- Python 3.10+
- `ffprobe` (part of [FFmpeg](https://ffmpeg.org))
- Python packages:
  - `Pillow`
  - `tkinter` (comes with Python)
  - `pillow-heif` (for HEIC support)

## Versioning

Version: `v1.1`

## License

MIT License