# Bulk File Renamer

A Windows GUI tool for bulk file renaming. Combine multiple rules — find/replace, multi-pair find/replace, prefix, suffix, sequential numbering, and case conversion — in a single pass. Bilingual UI (Turkish / English), dark mode, rule profiles, drag-and-drop, and more.

## Screenshot

<img width="980" height="930" alt="Bulk File Renamer GUI" src="https://github.com/user-attachments/assets/673b42b7-6d82-481d-af25-9336f418affc" />

## Features

### Renaming rules (combine freely)
- **Find & Replace** — literal or regex
- **Multi Find/Replace** — hundreds of pairs, one per line (`oldName newName`)
- **Prefix / Suffix** — prepend / append text (suffix goes before the extension)
- **Sequential Numbering** — `photo001`, `photo002`, ... (base name + start + padding)
- **Case Conversion** — lower / UPPER / Title Case

### Workflow
- **Preview** with color-coded status (green = OK, red = conflict, orange = excluded)
- **Exclude rows** from the preview (double-click, Space, or Delete key)
- **Safe two-phase rename** — `a ↔ b` swaps work correctly
- **Undo** — revert the last operation
- **Recursive** subfolder traversal
- **Extension filter** (e.g. `.jpg,.png`)
- **Sorting** — by name, modified date, or size (asc/desc)

### Quality of life
- **Light / Dark theme** — switchable at runtime
- **Bilingual UI** — Turkish and English
- **Drag & drop** — drop a folder onto the window
- **Recent folders** — last 10 folders in a dropdown
- **Rule profiles** — save / load your settings to a `.json` file
- **Keyboard shortcuts** — Ctrl+O, Ctrl+P, Ctrl+Enter, Ctrl+Z, Ctrl+S, Ctrl+L, Del, F1
- **Tooltips** on every button
- **About / Contact** dialog with clickable links

## Installation

### Option 1: Prebuilt .exe (recommended)

Download the latest `BulkFileRenamer.exe` from the [Releases](../../releases) page and run it. No Python installation required.

### Option 2: Run from source

```bash
git clone https://github.com/ayberkbgln/bulk-file-renamer.git
cd bulk-file-renamer
pip install tkinterdnd2   # optional, for drag & drop
python toplu_rename.py
```

Requires Python 3.8+. Tkinter ships with the standard library. `tkinterdnd2` is optional — the app works without it, just without drag-and-drop.

### Option 3: Build your own .exe

```bash
pip install pyinstaller pillow tkinterdnd2
python make_icon.py
pyinstaller --onefile --windowed --icon=app.ico \
            --add-data "app.ico;." --add-data "icon_256.png;." \
            --collect-all tkinterdnd2 \
            --name "BulkFileRenamer" toplu_rename.py
```

## Keyboard shortcuts

| Shortcut       | Action             |
| -------------- | ------------------ |
| `Ctrl+O`       | Browse folder      |
| `Ctrl+P`       | Preview            |
| `Ctrl+Enter`   | Apply              |
| `Ctrl+Z`       | Undo               |
| `Ctrl+S`       | Save profile       |
| `Ctrl+L`       | Load profile       |
| `Del` / `Space`| Exclude selected   |
| `F1`           | About              |

## Multi Find/Replace format

One rule per line:

```
oldWord newWord
IMG_ Holiday_
DSC_ Photo_
_v1
```

- **Separator:** TAB or whitespace (the first run of whitespace is the separator)
- **Single token on a line** → that text is deleted (the `_v1` line strips `_v1` from names)
- **Lines starting with `#`** are treated as comments and skipped

## About / Contact

Developed by **Ayberk Bağlan**.

- GitHub: [github.com/ayberkbgln](https://github.com/ayberkbgln)
- LinkedIn: [linkedin.com/in/ayberkbaglan](https://www.linkedin.com/in/ayberkbaglan/)
- X / Twitter: [@yulewiz](https://x.com/yulewiz)
- Email: ayberkbaglan@gmail.com

## Contributing

Issues and pull requests are welcome. Feel free to open an issue for feature requests or bug reports.

## License

[MIT](LICENSE)
