# 🗂️ Automatic File Sorter

A Python tool that watches a folder (like `Downloads`) and automatically sorts new files into category folders — PDFs, images, spreadsheets, archives, and more — the moment they land. No more digging through a messy folder.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## ✨ Features

- 🔁 **Live folder monitoring** — uses [Watchdog](https://pypi.org/project/watchdog/) to detect new files in real time
- 🗃️ **Dictionary-based sorting** — 40+ file extensions mapped to clean category folders out of the box
- 📁 **Automatic folder creation** — destination folders are created if they don't already exist
- 🔀 **Duplicate-safe renaming** — `Resume.pdf` becomes `Resume (1).pdf` instead of overwriting
- ⏳ **Copy-safe** — waits for a file's size to stabilize before moving it, so large files being copied in aren't grabbed half-written
- 🧾 **Timestamped logging** — every action is written to `sorting_log.txt` as well as the console
- 📊 **Run summary** — see exactly how many files went where after every sweep
- ⚙️ **Config-driven** — one file to edit; no digging through logic to change behavior

---

## 📁 Project Structure

```
Automatic-File-Sorter/
│
├── main.py             # Entry point — runs an initial sweep, then watches live
├── sorter.py           # All sorting logic (move, rename, log, folder creation)
├── config.py           # Folder path, file-type map, and other settings
├── requirements.txt    # Dependencies
├── README.md
├── LICENSE
├── .gitignore
└── sorting_log.txt     # Created automatically on first run
```

---

## 🚀 Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/<your-username>/Automatic-File-Sorter.git
cd Automatic-File-Sorter
pip install -r requirements.txt
```

### 2. Configure your folder

Open `config.py` and set `SOURCE_DIR` to the folder you want organized:

```python
SOURCE_DIR = r"C:\Users\YourName\Downloads"
```

You can also edit `FILE_TYPES` here to add extensions or change which folder a type goes to.

### 3. Run it

```bash
python main.py
```

The script will:
1. Sort every file already sitting in `SOURCE_DIR`
2. Print a summary
3. Keep running and sort new files as they arrive, until you press `Ctrl+C`

---

## 🧠 How It Works

| File | Responsibility |
| `config.py` | Defines *what* — the target folder, the extension → folder map, log path |
| `sorter.py` | Defines *how* — moving, renaming duplicates, waiting for copies to finish, logging |
| `main.py` | Defines *when* — runs the startup sweep, then starts a `watchdog` observer that calls `sorter.py` for every new file |

Every file is checked for a stable size before it's moved, so a large video or zip file that's still being copied into the folder won't get moved (and potentially corrupted) mid-transfer.


## 🔮 Possible Future Improvements

- [ ] System tray icon with start/stop controls
- [ ] Support for watching multiple folders at once
- [ ] `.env` or CLI arguments instead of editing `config.py` directly
- [ ] Undo/rollback for the last sort
- [ ] Package as a standalone `.exe` with PyInstaller


