# 📸 Photo Tools Suite

A set of Python tools to help organise and label your photo library with intelligent sorting, previewing, and renaming features.

---

## 🧰 Tools Overview

### 1. Photo Organiser
**File:** `photo_organiser_gui_v1.1.py`  
Automatically sorts images and videos into folders by date taken using EXIF metadata or fallback to modification dates. Supports duplicate detection and a manual review folder.

### 2. Folder Naming Assistant
**File:** `folder_namer_gui_v0.6e.py`  
Visually previews images in each dated folder, allows you to enter a short name (e.g. `2023-08-10 Brighton Trip`) to rename the folder. Click to view full-size images. Auto-skips empty folders and those already renamed.

### 3. Photo Tools Launcher
**File:** `photo_tools_launcher_v0.1.py`  
Simple GUI launcher to open either of the above tools with one click.

---

## 🧠 Features

- 📂 Sorts images/videos by date (`YYYY/YYYY-MM-DD`)
- 🧠 Duplicate detection using SHA-256
- 🖼️ Thumbnail previews and full-size image viewer
- ✏️ Rename folders with optional descriptions
- 🔍 "Unsure" folder for files needing manual review
- 💡 Supports multiple input folders
- 🧰 One-click launcher for convenience
- ✅ EXIF metadata + fallback support

---

## ⚙️ Requirements

- **Python 3.10 or later**
- Python packages:
  - `tkinter` (comes with Python)
  - `Pillow`
  - `pillow-heif` (for HEIC support)
- `ffprobe` (from [FFmpeg](https://ffmpeg.org)) for video metadata

Install dependencies (if needed):
```bash
pip install pillow pillow-heif
```

---

## 🚀 Getting Started

1. Download or clone this repository.
2. Open a terminal in the folder.
3. Launch the main tools using:

### 🧭 Option A: Use the Launcher
```bash
python photo_tools_launcher_v0.1.py
```

Choose between:
- **Photo Organiser**
- **Folder Naming Assistant**

### 🛠 Option B: Run Each Tool Directly

**Photo Organiser:**
```bash
python photo_organiser_gui_v1.1.py
```

**Folder Naming Assistant:**
```bash
python folder_namer_gui_v0.6e.py
```

---

## 📁 Tool Details

### 📁 Photo Organiser

Organises photos and videos from iPhones and other sources into date folders.

**Features:**
- Supports `.JPG`, `.JPEG`, `.MOV`, `.PNG`, `.HEIC`, etc.
- EXIF-based date extraction (fallback to modified date)
- Duplicate detection via hash comparison
- "Unsure" folder for manual sorting
- Dry-run preview mode available
- Full GUI with progress bar

**Version:** `v1.1`

---

### 🖼️ Folder Naming Assistant

Add descriptions to already date-organised folders by reviewing images visually.

**Features:**
- Auto-scans subfolders for `.jpg`, `.jpeg`, `.png` images
- Skips empty folders or already renamed ones
- Thumbnail previews (click to view full size)
- Editable folder name box
- Skip or rename via buttons or [Enter] key
- Optional full-screen image viewer with black background

**Version:** `v0.6e`

---

### 🚀 Photo Tools Launcher

A convenient launcher for the tools above.

**File:** `photo_tools_launcher_v0.1.py`

**Version:** `v0.1`

---

## 🗂 Versioning & Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed changes per version.

---

## 📜 License

This project is licensed under the MIT License.
