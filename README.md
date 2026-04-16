# Bulk File Renamer

A Windows GUI tool for bulk file renaming. Combine multiple rules — find/replace, prefix, suffix, sequential numbering, and case conversion — in a single pass. Written in Python with Tkinter.

## Screenshot

<img width="980" height="930" alt="Bulk File Renamer GUI" src="https://github.com/user-attachments/assets/673b42b7-6d82-481d-af25-9336f418affc" />

## Features

- **Find & Replace** — literal or regex
- **Multi Find/Replace** — hundreds of pairs, one per line (e.g. `oldName newName`)
- **Prefix / Suffix** — prepend or append text (suffix goes before the extension)
- **Sequential Numbering** — `photo001`, `photo002`, ... (base name + start + padding)
- **Case Conversion** — lower / UPPER / Title Case
- **Recursive** — optionally walk subfolders
- **Extension Filter** — e.g. `.jpg,.png`
- **Preview** — see new names before applying (conflicts highlighted)
- **Undo** — revert the last operation
- **Safe Renaming** — two-phase rename that handles `a ↔ b` swaps correctly

## Installation

### Option 1: Prebuilt .exe (recommended)

Download the latest `.exe` from the [Releases](../../releases) page and run it. No Python installation required.

### Option 2: Run from source

```bash
git clone https://github.com/ayberkbgln/bulk-file-renamer.git
cd bulk-file-renamer
python toplu_rename.py
```

Requires Python 3.8+. Tkinter ships with the standard library, so no extra dependencies are needed.

### Option 3: Build your own .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "BulkFileRenamer" toplu_rename.py
```

The executable is written to the `dist/` folder.

## Usage

1. Click **Gözat...** (Browse) and pick a folder
2. Optionally: enable recursion, add an extension filter
3. Tick the operations you want and fill in the values
4. Click **Önizleme** (Preview) and review the list (green = OK, red = conflict)
5. Click **Uygula** (Apply) and confirm
6. If anything looks wrong, click **Geri Al** (Undo) to revert

> The UI labels are currently in Turkish; an English localization is planned.

### Multi Find/Replace Format

One rule per line:

```
oldWord newWord
IMG_ Holiday_
DSC_ Photo_
_v1
```

- **Separator:** TAB or whitespace (the first run of whitespace is treated as the separator)
- **Single token on a line** → that text is deleted (the `_v1` example above strips `_v1`)
- **Lines starting with `#`** are treated as comments and skipped

## Contributing

Issues and pull requests are welcome. Feel free to open an issue for feature requests or bug reports.

## License

[MIT](LICENSE)
