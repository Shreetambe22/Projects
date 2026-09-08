"""
Automatic File Sorter - entry point.

Runs one initial sweep of SOURCE_DIR, then watches it continuously
and sorts new files as they arrive. This is the piece the original
notebook was missing: watchdog was imported but never wired up, so
nothing actually ran "automatically."
"""

import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
from sorter import sort_single_file, sort_existing_files, log


class SortHandler(FileSystemEventHandler):
    """Reacts to files appearing directly inside SOURCE_DIR."""

    def on_created(self, event):
        if event.is_directory:
            return
        sort_single_file(event.src_path)

    def on_moved(self, event):
        # Handles files renamed/dropped in by another program
        if event.is_directory:
            return
        sort_single_file(event.dest_path)


def main():
    log.info(f"Watching folder: {config.SOURCE_DIR}")

    # Sort whatever is already sitting in the folder before we start watching
    sort_existing_files()

    event_handler = SortHandler()
    observer = Observer()
    observer.schedule(event_handler, config.SOURCE_DIR, recursive=False)
    observer.start()

    log.info("Live monitoring started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Stopped by user.")

    observer.join()


if __name__ == "__main__":
    main()
