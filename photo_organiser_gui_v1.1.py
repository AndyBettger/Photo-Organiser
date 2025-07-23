#!/usr/bin/env python3
import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import subprocess
import csv
from collections import defaultdict

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mov", ".mp4", ".heic"}

def get_date_taken(file_path):
    file_path = Path(file_path)
    ext = file_path.suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".heic"}:
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id)
                    if tag in ["DateTimeOriginal", "DateTime"]:
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception:
            pass
    try:
        result = subprocess.run([
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format_tags=creation_time",
            "-of", "default=noprint_wrappers=1:nokey=0",
            str(file_path)
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in result.stdout.splitlines():
            if "creation_time=" in line:
                date_str = line.split("=")[1].strip()
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        pass
    return None

def hash_file(path, method="sha256"):
    h = hashlib.sha256() if method == "sha256" else hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def organize_files(input_dirs, output_path, use_copy, fallback_to_modified, plan, log_callback, hash_method, progress_callback, stage_callback):
    seen_hashes = set()
    hash_to_files = defaultdict(list)
    hash_to_output_path = {}
    duplicate_records = []
    organized_count = 0
    fallback_organized_count = 0
    unsupported_count = 0
    unsure_count = 0
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        log_callback(msg)

    log("📁 Scanning files...")

    all_files = []
    for input_dir in input_dirs:
        for file in Path(input_dir).rglob("*.*"):
            if file.name.lower() == "thumbs.db":
                continue
            if file.suffix.lower() in SUPPORTED_EXTENSIONS:
                all_files.append(file)

    total_files = len(all_files)
    log(f"🔍 Found {total_files} supported files.")

    stage_callback("Hashing")
    for i, file in enumerate(all_files):
        date = get_date_taken(file)
        used_fallback = False
        if not date and fallback_to_modified:
            try:
                date = datetime.fromtimestamp(file.stat().st_mtime)
                used_fallback = True
            except Exception:
                pass

        file_hash = hash_file(file, method=hash_method)
        hash_to_files[file_hash].append((file, date, used_fallback))
        progress_callback((i + 1) / total_files * 50)

    stage_callback("Organizing")
    file_index = 0
    for file_hash, entries in hash_to_files.items():
        valid_dates = [d for _, d, _ in entries if d and d.year >= 1978]
        best_date = min(valid_dates) if valid_dates else None

        for idx, (file, _, used_fallback) in enumerate(entries):
            if file.name.lower() == "thumbs.db" or file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                unsupported_count += 1
                continue

            is_duplicate = file_hash in seen_hashes
            if best_date:
                if is_duplicate:
                    base_dir = Path(output_path) / "duplicates" / str(best_date.year) / best_date.strftime("%Y-%m-%d")
                else:
                    base_dir = Path(output_path) / str(best_date.year) / best_date.strftime("%Y-%m-%d")
            else:
                base_dir = Path(output_path) / ("duplicates" if is_duplicate else "unsure") / "unknown_date"
                unsure_count += 1

            base_dir.mkdir(parents=True, exist_ok=True)
            target_path = base_dir / file.name

            if is_duplicate:
                original_path = hash_to_output_path.get(file_hash, "unknown")
                log(f"[DUPLICATE] {file} -> {target_path} (duplicate of {original_path})")
                duplicate_records.append((str(file), str(target_path), str(original_path), file_hash))
                if not plan:
                    if use_copy:
                        shutil.copy2(file, target_path)
                    else:
                        shutil.move(file, target_path)
            else:
                seen_hashes.add(file_hash)
                hash_to_output_path[file_hash] = str(target_path)
                log(f"[MOVE] {file} -> {target_path}")
                if best_date and not used_fallback:
                    organized_count += 1
                elif best_date and used_fallback:
                    fallback_organized_count += 1
                if not plan:
                    if use_copy:
                        shutil.copy2(file, target_path)
                    else:
                        shutil.move(file, target_path)

            file_index += 1
            progress_callback(50 + (file_index / total_files * 50))

    log_path = Path(output_path) / "organiser_log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")

    if duplicate_records:
        csv_path = Path(output_path) / "duplicates_summary.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Duplicate File", "Moved To", "Original Matched File", "File Hash"])
            writer.writerows(duplicate_records)

    return {
        "input_files": total_files,
        "organized": organized_count,
        "fallback": fallback_organized_count,
        "duplicates": len(duplicate_records),
        "unsupported": unsupported_count,
        "unsure": unsure_count
    }

def run_organiser_async(params):
    input_dirs, output_folder, use_copy, fallback, plan, hash_method, text_widget, progress, stage_label = params

    def log(msg):
        text_widget.insert(tk.END, msg + "\n")
        text_widget.see(tk.END)

    def update_progress(val):
        progress["value"] = val
        progress.update()

    def update_stage(text):
        stage_label.config(text=f"Stage: {text}")
        stage_label.update()

    text_widget.delete("1.0", tk.END)
    progress["value"] = 0
    stage_label.config(text="Stage: Starting")
    text_widget.update()

    result = organize_files(
        input_dirs, output_folder, use_copy, fallback, plan, log, hash_method, update_progress, update_stage)
    summary = (
        f"✔ Done organizing {result['input_files']} files.\n"
        f"  - {result['organized']} files copied using EXIF/metadata\n"
        f"  - {result['fallback']} files copied using modified date\n"
        f"  - {result['duplicates']} duplicates sent to /duplicates\n"
        f"  - {result['unsupported']} unsupported files ignored\n"
        f"  - {result['unsure']} files went to /unsure\n\n"
        f"Total output: {result['organized'] + result['fallback'] + result['duplicates']} organized files\n\n"
        f"See organiser_log.txt for full details."
    )
    progress["value"] = 100
    stage_label.config(text="Stage: Complete")
    messagebox.showinfo("Completed", summary)

def browse_folder(entry):
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def create_gui():
    root = tk.Tk()
    root.title("Photo Organiser")

    tk.Label(root, text="Input Folder 1:").grid(row=0, column=0, sticky="e")
    input1 = tk.Entry(root, width=60)
    input1.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_folder(input1)).grid(row=0, column=2)

    tk.Label(root, text="Input Folder 2:").grid(row=1, column=0, sticky="e")
    input2 = tk.Entry(root, width=60)
    input2.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_folder(input2)).grid(row=1, column=2)

    tk.Label(root, text="Output Folder:").grid(row=2, column=0, sticky="e")
    output = tk.Entry(root, width=60)
    output.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_folder(output)).grid(row=2, column=2)

    use_copy = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Copy (uncheck to Move)", variable=use_copy).grid(row=3, column=1, sticky="w")

    fallback = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Fallback to Modified Date", variable=fallback).grid(row=4, column=1, sticky="w")

    plan = tk.BooleanVar()
    tk.Checkbutton(root, text="Plan Only (Preview)", variable=plan).grid(row=5, column=1, sticky="w")

    hash_method = tk.StringVar(value="sha256")
    tk.Label(root, text="Hash Method:").grid(row=6, column=0, sticky="e")
    tk.OptionMenu(root, hash_method, "sha256", "md5").grid(row=6, column=1, sticky="w")

    progress = ttk.Progressbar(root, length=400, mode="determinate")
    progress.grid(row=7, column=0, columnspan=3, pady=5)

    stage_label = tk.Label(root, text="Stage: Not Started")
    stage_label.grid(row=8, column=0, columnspan=3)

    log_text = tk.Text(root, height=20, width=90)
    log_text.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

    def start():
        input_dirs = [d for d in [input1.get(), input2.get()] if d]
        out = output.get()
        if not input_dirs or not out:
            messagebox.showerror("Error", "Please select at least one input and an output folder.")
            return
        args = (input_dirs, out, use_copy.get(), fallback.get(), plan.get(), hash_method.get(), log_text, progress, stage_label)
        threading.Thread(target=run_organiser_async, args=(args,), daemon=True).start()

    tk.Button(root, text="Start", command=start).grid(row=10, column=1)
    root.mainloop()

if __name__ == "__main__":
    create_gui()