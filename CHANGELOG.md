# Changelog

## v0.6 – 2025-07-23

### Folder Naming Assistant (`folder_namer_gui_v0.6.py`)
- Fixed thumbnail duplication issues
- Added "Change Folder" button
- Automatically skips folders that are already renamed or contain no images
- Supports click-and-hold for full-size image previews
- Removed non-functional thumbnail resize on window resize
- Improved cross-platform folder path formatting (Windows-friendly)

## v0.1 – 2025-07-23

### Photo Tools Launcher (`photo_tools_launcher_v0.1.py`)
- New launcher GUI to open either the Organiser or Folder Namer
- Provides a single interface to access both tools

## [v1.1] - 2025-07-23

### Photo Organiser GUI (`photo_organiser_gui_v1.1.py`)
- Default to "Move" instead of "Copy"
- Fallback to file modified date enabled by default
- Auto-skip of `thumbs.db` files
- SHA-256 and MD5-based duplicate detection
- GUI frontend with progress feedback and dry-run mode
- Output folders organized by `YYYY/YYYY-MM-DD`
- CSV log of duplicates with original file reference and hash