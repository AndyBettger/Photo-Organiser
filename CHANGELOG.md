# Changelog

## [v0.2] - 2025-07-24

### Photo Tools Launcher (`photo_tools_launcher_v0.2.py`)
#### Changed
- Changed buttons to launch new versions.

---

## [v0.6e] - 2025-07-24

### Folder Naming Assistant (`folder_namer_gui_v0.6e.py`)
#### Fixed
- Folder name entry field now accepts text input even when auto folder selection is used.
- Restored correct thumbnail generation logic and avoided duplication.

#### Added
- Automatically opens folder selector on start.
- Progress label (e.g., "Progress: 3 / 10") now appears correctly again.

#### Changed
- Improved thumbnail layout with consistent spacing.
- Full-size image preview now opens on black background and scales to fit screen without cropping.

#### Removed
- Broken thumbnail resizing on window resize, which previously caused errors.

---

## [v0.6] - 2025-07-23

### Folder Naming Assistant (`folder_namer_gui_v0.6.py`)
#### Added
- Thumbnails are now centred with consistent layout.
- Full-size image preview with black background.
- Folder name entry box now supports typing.
- Automatically opens folder selector on launch.
- Skips folders without supported image types.
- Improved folder skipping logic to avoid already named folders.

#### Fixed
- Removed broken image resizing behaviour.
- Resolved several slash escaping and f-string syntax errors.

### Photo Tools Launcher (`photo_tools_launcher_v0.1.py`)
#### Added
- New launcher GUI to open either the Organiser or Folder Namer
- Provides a single interface to access both tools

---

## [v1.1] - 2025-07-23

### Photo Organiser GUI (`photo_organiser_gui_v1.1.py`)
#### Added
- Auto-skip of `thumbs.db` files
- SHA-256 and MD5-based duplicate detection
- GUI frontend with progress feedback and dry-run mode
- Output folders organized by `YYYY/YYYY-MM-DD`
- CSV log of duplicates with original file reference and hash

#### Changed
- Default to "Move" instead of "Copy"
- Fallback to file modified date enabled by default

