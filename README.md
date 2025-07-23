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