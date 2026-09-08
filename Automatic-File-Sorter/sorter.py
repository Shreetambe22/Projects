"""
Core sorting logic for Automatic File Sorter.

Everything here is reusable by both a one-time sweep (main.py on
startup) and the live watcher (main.py's SortHandler), so there is a
single source of truth for "what happens to a file."
"""

import os
import shutil
import logging
import time

import config


def setup_logging():
    """Configure logging to both the console and sorting_log.txt."""
    logger = logging.getLogger("file_sorter")
    logger.setLevel(logging.INFO)

    if logger.handlers:  # avoid duplicate handlers if re-imported
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


log = setup_logging()


def ensure_folders_exist():
    """Create every destination folder up front so a move never fails
    just because the target directory doesn't exist yet."""
    folder_names = set(config.FILE_TYPES.values())

    if config.OTHERS_FOLDER:
        folder_names.add(config.OTHERS_FOLDER)

    for folder in folder_names:
        os.makedirs(os.path.join(config.SOURCE_DIR, folder), exist_ok=True)


def get_unique_filename(destination_folder, filename):
    """Return a filename that won't collide with anything already in
    destination_folder, appending ' (1)', ' (2)', etc. as needed."""
    name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name} ({counter}){extension}"
        counter += 1

    return new_filename


def is_file_ready(filepath):
    """Poll a file's size for a short while to make sure it has
    finished being written/copied before we move it. Without this,
    the live watcher can grab a file mid-copy and move a corrupted,
    partial version of it.

    Returns True once the size is stable across two checks (or after
    giving up), False if the file disappeared while we were waiting.
    """
    try:
        previous_size = -1
        for _ in range(config.FILE_READY_MAX_CHECKS):
            if not os.path.exists(filepath):
                return False
            current_size = os.path.getsize(filepath)
            if current_size == previous_size:
                return True
            previous_size = current_size
            time.sleep(config.FILE_READY_CHECK_INTERVAL)
        return True  # stopped changing enough times, or gave up waiting
    except OSError:
        return False


def get_destination_folder(filename):
    """Work out which folder a file belongs in, or None if it should
    be left alone (only possible when OTHERS_FOLDER is None)."""
    ext = os.path.splitext(filename)[1].lower()
    return config.FILE_TYPES.get(ext, config.OTHERS_FOLDER)


def sort_single_file(filepath):
    """Move a single file into its matching folder.

    Returns the destination folder name on success, or None if the
    file was skipped (missing, still being written, unrecognized
    with no Others folder configured, or a move error occurred).
    """
    filename = os.path.basename(filepath)

    if not os.path.isfile(filepath):
        return None

    # Never touch the log file itself, or hidden/system files
    if os.path.abspath(filepath) == os.path.abspath(config.LOG_FILE):
        return None
    if filename.startswith("."):
        return None

    folder_name = get_destination_folder(filename)
    if folder_name is None:
        log.info(f"Skipped (unrecognized type): {filename}")
        return None

    if not is_file_ready(filepath):
        log.warning(f"Skipped (still being written): {filename}")
        return None

    destination_folder = os.path.join(config.SOURCE_DIR, folder_name)
    os.makedirs(destination_folder, exist_ok=True)

    new_filename = get_unique_filename(destination_folder, filename)
    destination = os.path.join(destination_folder, new_filename)

    try:
        shutil.move(filepath, destination)
    except (PermissionError, OSError) as e:
        log.error(f"Failed to move {filename}: {e}")
        return None

    if new_filename == filename:
        log.info(f"Moved: {filename} -> {folder_name}/")
    else:
        log.info(f"Renamed & Moved: {filename} -> {folder_name}/{new_filename}")

    return folder_name


def sort_existing_files():
    """Scan SOURCE_DIR once and sort everything currently sitting in
    it. Called on startup, and safe to call any time for a manual
    sweep."""
    ensure_folders_exist()

    total_files = 0
    skipped_files = 0
    moved_count = {}

    for file in os.listdir(config.SOURCE_DIR):
        source = os.path.join(config.SOURCE_DIR, file)

        if os.path.isdir(source):
            continue

        total_files += 1
        folder_name = sort_single_file(source)

        if folder_name:
            moved_count[folder_name] = moved_count.get(folder_name, 0) + 1
        else:
            skipped_files += 1

    print_summary(total_files, skipped_files, moved_count)


def print_summary(total_files, skipped_files, moved_count):
    log.info("=" * 40)
    log.info("          FILE SORTING SUMMARY")
    log.info("=" * 40)
    log.info(f"Total files scanned : {total_files}")

    for folder, count in sorted(moved_count.items()):
        log.info(f"{folder:<20}: {count}")

    log.info(f"Skipped files        : {skipped_files}")
    log.info("=" * 40)
