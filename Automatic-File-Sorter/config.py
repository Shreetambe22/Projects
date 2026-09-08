"""
Configuration for Automatic File Sorter.

Edit SOURCE_DIR below to the folder you want watched and organized.
Everything else is optional to tweak.
"""

import os

# ----------------------------------------------------------------------
# Folder that will be watched and organized
# ----------------------------------------------------------------------
SOURCE_DIR = r"D:\All info scans\Krushna"

# ----------------------------------------------------------------------
# Where files with an unrecognized extension should go.
# Set to None to leave unknown files where they are instead.
# ----------------------------------------------------------------------
OTHERS_FOLDER = "Others"

# ----------------------------------------------------------------------
# Log file (created automatically next to this script)
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "sorting_log.txt")

# ----------------------------------------------------------------------
# How long to wait for a file to finish copying before moving it.
# This stops the watcher from grabbing a half-written file.
# ----------------------------------------------------------------------
FILE_READY_CHECK_INTERVAL = 0.5   # seconds between size checks
FILE_READY_MAX_CHECKS = 20        # ~10 seconds max wait per file

# ----------------------------------------------------------------------
# Extension -> destination folder name
# ----------------------------------------------------------------------
FILE_TYPES = {
    # Documents
    ".pdf": "PDF Files",
    ".doc": "Word Files",
    ".docx": "Word Files",
    ".txt": "Text Files",
    ".rtf": "Text Files",
    ".md": "Text Files",

    # Spreadsheets
    ".xls": "Excel Files",
    ".xlsx": "Excel Files",
    ".csv": "CSV Files",

    # Presentations
    ".ppt": "PowerPoint Files",
    ".pptx": "PowerPoint Files",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".tiff": "Images",
    ".heic": "Images",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Audio
    ".mp3": "Audio Files",
    ".wav": "Audio Files",
    ".flac": "Audio Files",
    ".m4a": "Audio Files",

    # Video
    ".mp4": "Video Files",
    ".mkv": "Video Files",
    ".avi": "Video Files",
    ".mov": "Video Files",

    # Code
    ".py": "Code Files",
    ".js": "Code Files",
    ".html": "Code Files",
    ".css": "Code Files",
    ".json": "Code Files",
    ".ipynb": "Code Files",

    # Executables / installers
    ".exe": "Programs",
    ".msi": "Programs",
    ".apk": "Programs",
}
