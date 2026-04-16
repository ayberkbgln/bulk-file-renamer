"""
Bulk File Renamer / Toplu Dosya Yeniden Adlandirici
GUI ile coklu islem destegi: bul/degistir, coklu kural listesi, onek/sonek,
numaralandirma, harf donusumu. Dil secici (TR/EN), Dark Mode, Profiller,
Drag-drop, siralama, satir hariç tutma, son klasorler, tooltips, kisayollar.

Author: Ayberk Baglan
GitHub: https://github.com/ayberkbgln
"""

import os
import re
import sys
import json
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


APP_NAME = "Bulk File Renamer"
APP_VERSION = "1.2.0"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".bulk_file_renamer.json")
MAX_RECENT = 10


# ---------- Themes ----------
LIGHT_THEME = {
    "bg": "#f5f6fa",
    "fg": "#1f2937",
    "frame_bg": "#ffffff",
    "frame_border": "#e5e7eb",
    "entry_bg": "#ffffff",
    "entry_fg": "#1f2937",
    "btn_bg": "#ffffff",
    "btn_fg": "#1f2937",
    "btn_hover": "#eef2ff",
    "btn_border": "#d1d5db",
    "accent": "#4f7cff",
    "accent_hover": "#3d65e0",
    "accent_fg": "#ffffff",
    "tree_bg": "#ffffff",
    "tree_fg": "#1f2937",
    "tree_heading_bg": "#f3f4f6",
    "tree_heading_fg": "#1f2937",
    "tree_sel": "#dbeafe",
    "tag_ok_bg": "#dcfce7",
    "tag_ok_fg": "#166534",
    "tag_same_bg": "#f3f4f6",
    "tag_same_fg": "#6b7280",
    "tag_conflict_bg": "#fee2e2",
    "tag_conflict_fg": "#991b1b",
    "tag_excluded_bg": "#fff7ed",
    "tag_excluded_fg": "#9a3412",
    "status_bg": "#eef2ff",
    "status_fg": "#1f2937",
    "muted": "#6b7280",
    "link": "#2563eb",
    "tooltip_bg": "#111827",
    "tooltip_fg": "#f9fafb",
    "title_fg": "#111827",
}

DARK_THEME = {
    "bg": "#0f172a",
    "fg": "#e2e8f0",
    "frame_bg": "#1e293b",
    "frame_border": "#334155",
    "entry_bg": "#0f172a",
    "entry_fg": "#e2e8f0",
    "btn_bg": "#334155",
    "btn_fg": "#e2e8f0",
    "btn_hover": "#475569",
    "btn_border": "#475569",
    "accent": "#6366f1",
    "accent_hover": "#818cf8",
    "accent_fg": "#ffffff",
    "tree_bg": "#1e293b",
    "tree_fg": "#e2e8f0",
    "tree_heading_bg": "#334155",
    "tree_heading_fg": "#e2e8f0",
    "tree_sel": "#3730a3",
    "tag_ok_bg": "#14532d",
    "tag_ok_fg": "#bbf7d0",
    "tag_same_bg": "#1e293b",
    "tag_same_fg": "#94a3b8",
    "tag_conflict_bg": "#7f1d1d",
    "tag_conflict_fg": "#fecaca",
    "tag_excluded_bg": "#78350f",
    "tag_excluded_fg": "#fed7aa",
    "status_bg": "#1e293b",
    "status_fg": "#e2e8f0",
    "muted": "#94a3b8",
    "link": "#818cf8",
    "tooltip_bg": "#f9fafb",
    "tooltip_fg": "#111827",
    "title_fg": "#f1f5f9",
}


# ---------- Localization ----------
STRINGS = {
    "tr": {
        "title": "Toplu Dosya Yeniden Adlandirici",
        "folder_section": "Klasor Secimi",
        "folder_label": "Klasor:",
        "browse": "Gozat...",
        "recent": "Son",
        "recursive": "Alt klasorleri de dahil et",
        "ext_filter": "Uzanti filtresi:",
        "ext_hint": "(orn: .jpg,.png - bos birakilirsa tum dosyalar)",
        "sort_label": "Siralama:",
        "sort_name_asc": "Ad (A-Z)",
        "sort_name_desc": "Ad (Z-A)",
        "sort_date_asc": "Degistirilme (eski->yeni)",
        "sort_date_desc": "Degistirilme (yeni->eski)",
        "sort_size_asc": "Boyut (kucuk->buyuk)",
        "sort_size_desc": "Boyut (buyuk->kucuk)",
        "dnd_hint": "(klasor surukleyip birakabilirsiniz)",
        "ops_section": "Islemler (istediginiz kadarini ayni anda kullanabilirsiniz)",
        "find_replace": "Bul ve Degistir",
        "find": "Bul:",
        "replace": "Degistir:",
        "regex": "Regex",
        "multi_fr": "Coklu Bul/Degistir",
        "multi_fr_hint": (
            "Her satira bir cift:  BUL  DEGISTIR  (TAB veya bosluk ile ayirin). "
            "Tek kelime yazarsaniz o metin silinir. '#' ile baslayan satirlar atlanir."
        ),
        "multi_example": "# Ornek:\n# eskiKelime yeniKelime\n# IMG_ foto_\n",
        "prefix_add": "Onek Ekle",
        "suffix_add": "Sonek Ekle",
        "suffix_hint": "(uzantidan once eklenir)",
        "text": "Metin:",
        "numbering": "Numaralandir",
        "base_name": "Taban ad:",
        "start": "Baslangic:",
        "pad": "Basamak:",
        "case_conv": "Harf Donusumu",
        "case_lower": "kucuk",
        "case_upper": "BUYUK",
        "case_title": "Ilk Harfler",
        "preview": "Onizleme",
        "apply": "Uygula",
        "undo": "Geri Al",
        "clear": "Temizle",
        "about": "Hakkinda",
        "profile": "Profil",
        "save_profile": "Profili Kaydet...",
        "load_profile": "Profili Yukle...",
        "preview_section": "Onizleme",
        "exclude_selected": "Secileni Hariç Tut (Del)",
        "include_selected": "Secileni Dahil Et",
        "include_all": "Tumunu Dahil Et",
        "col_old": "Eski Ad",
        "col_new": "Yeni Ad",
        "col_status": "Durum",
        "ready": "Hazir. Klasor secip 'Onizleme'ye basin. | Kisayollar: Ctrl+O / Ctrl+P / Ctrl+Enter / Ctrl+Z",
        "status_ok": "OK",
        "status_same": "Degismez",
        "status_conflict": "Cakisma!",
        "status_exists": "Mevcut!",
        "status_excluded": "Hariç",
        "err_title": "Hata",
        "warn_title": "Uyari",
        "info_title": "Bilgi",
        "err_invalid_folder": "Lutfen gecerli bir klasor secin.",
        "warn_need_op": "En az bir islem secmelisiniz.",
        "no_files": "Dosya bulunamadi.",
        "need_preview": "Once 'Onizleme' yapin.",
        "nothing_to_rename": "Yeniden adlandirilacak dosya yok.",
        "conflict_warn": "{n} dosyada cakisma/mevcut var. Bunlar atlanacak. Devam?",
        "confirm_apply": "{n} dosya yeniden adlandirilacak. Onayliyor musunuz?",
        "done": "Tamamlandi",
        "done_msg": "Basarili: {s}\nBasarisiz: {f}",
        "done_status": "Tamamlandi. Basarili: {s}, Basarisiz: {f}. 'Geri Al' ile eski haline donebilirsiniz.",
        "undo_none": "Geri alinacak islem yok.",
        "undo_confirm": "{n} dosya eski adina dondurulecek. Emin misiniz?",
        "undone": "Geri Alindi",
        "undo_status": "Geri alindi. {n} dosya.",
        "cleared": "Temizlendi.",
        "summary": "Toplam: {t} dosya   |   Degisecek: {ok}   |   Hariç: {ex}   |   Sorunlu: {c}",
        "regex_err": "Regex hatasi: {e}",
        "language": "Dil:",
        "theme": "Tema:",
        "light": "Acik",
        "dark": "Koyu",
        # Profile
        "profile_saved": "Profil kaydedildi.",
        "profile_loaded": "Profil yuklendi.",
        "profile_load_err": "Profil yuklenemedi: {e}",
        "profile_save_title": "Profili Kaydet",
        "profile_load_title": "Profili Yukle",
        "json_files": "JSON dosyalari",
        # Tooltips
        "tt_browse": "Klasor secin (Ctrl+O)",
        "tt_recent": "Son kullanilan klasorler",
        "tt_theme": "Acik/koyu tema arasinda gecis yapin",
        "tt_preview": "Yeni adlari goster, uygulamadan once kontrol edin (Ctrl+P)",
        "tt_apply": "Yeniden adlandirmayi uygula (Ctrl+Enter)",
        "tt_undo": "Son islemi geri al (Ctrl+Z)",
        "tt_clear": "Tum alanlari temizle",
        "tt_save_profile": "Mevcut ayarlari .json dosyasina kaydedin (Ctrl+S)",
        "tt_load_profile": "Kaydedilmis .json profilini yukleyin (Ctrl+L)",
        "tt_regex": "Bul metnini Python regex olarak yorumla",
        "tt_exclude": "Secili satirlari yeniden adlandirmadan hariç tut (Del)",
        "tt_include": "Secili satirlari yeniden dahil et",
        # About
        "about_title": "Hakkinda",
        "about_app_name": APP_NAME,
        "about_version": f"Surum {APP_VERSION}",
        "about_desc": "Coklu kurali tek seferde uygulayabilen, GUI tabanli, ucretsiz ve acik kaynak bir yeniden adlandirma aracidir.",
        "about_developer": "Gelistiren",
        "about_contact": "Iletisim",
        "about_license": "Lisans: MIT",
        "about_close": "Kapat",
        "about_source": "Kaynak Kod",
    },
    "en": {
        "title": APP_NAME,
        "folder_section": "Folder Selection",
        "folder_label": "Folder:",
        "browse": "Browse...",
        "recent": "Recent",
        "recursive": "Include subfolders",
        "ext_filter": "Extension filter:",
        "ext_hint": "(e.g. .jpg,.png - leave empty for all files)",
        "sort_label": "Sort:",
        "sort_name_asc": "Name (A-Z)",
        "sort_name_desc": "Name (Z-A)",
        "sort_date_asc": "Modified (old->new)",
        "sort_date_desc": "Modified (new->old)",
        "sort_size_asc": "Size (small->large)",
        "sort_size_desc": "Size (large->small)",
        "dnd_hint": "(you can drag & drop a folder here)",
        "ops_section": "Operations (combine as many as you need)",
        "find_replace": "Find and Replace",
        "find": "Find:",
        "replace": "Replace:",
        "regex": "Regex",
        "multi_fr": "Multi Find/Replace",
        "multi_fr_hint": (
            "One pair per line:  FIND  REPLACE  (separate with TAB or whitespace). "
            "A single token deletes that text. Lines starting with '#' are ignored."
        ),
        "multi_example": "# Example:\n# oldWord newWord\n# IMG_ photo_\n",
        "prefix_add": "Add Prefix",
        "suffix_add": "Add Suffix",
        "suffix_hint": "(inserted before the extension)",
        "text": "Text:",
        "numbering": "Numbering",
        "base_name": "Base name:",
        "start": "Start:",
        "pad": "Padding:",
        "case_conv": "Case Conversion",
        "case_lower": "lower",
        "case_upper": "UPPER",
        "case_title": "Title Case",
        "preview": "Preview",
        "apply": "Apply",
        "undo": "Undo",
        "clear": "Clear",
        "about": "About",
        "profile": "Profile",
        "save_profile": "Save Profile...",
        "load_profile": "Load Profile...",
        "preview_section": "Preview",
        "exclude_selected": "Exclude Selected (Del)",
        "include_selected": "Include Selected",
        "include_all": "Include All",
        "col_old": "Old Name",
        "col_new": "New Name",
        "col_status": "Status",
        "ready": "Ready. Pick a folder and click 'Preview'. | Shortcuts: Ctrl+O / Ctrl+P / Ctrl+Enter / Ctrl+Z",
        "status_ok": "OK",
        "status_same": "Unchanged",
        "status_conflict": "Conflict!",
        "status_exists": "Exists!",
        "status_excluded": "Excluded",
        "err_title": "Error",
        "warn_title": "Warning",
        "info_title": "Info",
        "err_invalid_folder": "Please choose a valid folder.",
        "warn_need_op": "You must select at least one operation.",
        "no_files": "No files found.",
        "need_preview": "Run 'Preview' first.",
        "nothing_to_rename": "Nothing to rename.",
        "conflict_warn": "{n} files have conflicts. They will be skipped. Continue?",
        "confirm_apply": "{n} files will be renamed. Confirm?",
        "done": "Done",
        "done_msg": "Success: {s}\nFailed: {f}",
        "done_status": "Done. Success: {s}, Failed: {f}. You can use 'Undo' to revert.",
        "undo_none": "Nothing to undo.",
        "undo_confirm": "{n} files will be restored. Are you sure?",
        "undone": "Undone",
        "undo_status": "Reverted. {n} files.",
        "cleared": "Cleared.",
        "summary": "Total: {t} files   |   Will change: {ok}   |   Excluded: {ex}   |   Problems: {c}",
        "regex_err": "Regex error: {e}",
        "language": "Language:",
        "theme": "Theme:",
        "light": "Light",
        "dark": "Dark",
        # Profile
        "profile_saved": "Profile saved.",
        "profile_loaded": "Profile loaded.",
        "profile_load_err": "Could not load profile: {e}",
        "profile_save_title": "Save Profile",
        "profile_load_title": "Load Profile",
        "json_files": "JSON files",
        # Tooltips
        "tt_browse": "Choose folder (Ctrl+O)",
        "tt_recent": "Recently used folders",
        "tt_theme": "Toggle light / dark theme",
        "tt_preview": "Show new names — review before applying (Ctrl+P)",
        "tt_apply": "Apply the renaming (Ctrl+Enter)",
        "tt_undo": "Undo the last operation (Ctrl+Z)",
        "tt_clear": "Clear all fields",
        "tt_save_profile": "Save current settings to a .json file (Ctrl+S)",
        "tt_load_profile": "Load a saved .json profile (Ctrl+L)",
        "tt_regex": "Interpret the Find text as a Python regex",
        "tt_exclude": "Exclude selected rows from renaming (Del)",
        "tt_include": "Include selected rows again",
        # About
        "about_title": "About",
        "about_app_name": APP_NAME,
        "about_version": f"Version {APP_VERSION}",
        "about_desc": "A free, open-source, GUI-based bulk file renamer that can combine multiple rules in a single pass.",
        "about_developer": "Developed by",
        "about_contact": "Contact",
        "about_license": "License: MIT",
        "about_close": "Close",
        "about_source": "Source Code",
    },
}


def resource_path(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


# ---------- Config persistence ----------
class Config:
    def __init__(self):
        self.data = {}
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, encoding="utf-8") as f:
                    self.data = json.load(f)
        except (OSError, json.JSONDecodeError):
            self.data = {}

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def add_recent(self, folder):
        lst = [f for f in self.get("recent", []) if f != folder]
        lst.insert(0, folder)
        self.set("recent", lst[:MAX_RECENT])


# ---------- Tooltip ----------
class Tooltip:
    def __init__(self, widget, text, theme):
        self.widget = widget
        self.text = text
        self.theme = theme
        self.tip = None
        self.after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def set_text(self, text):
        self.text = text

    def set_theme(self, theme):
        self.theme = theme

    def _schedule(self, _evt=None):
        self._cancel()
        self.after_id = self.widget.after(500, self._show)

    def _cancel(self):
        if self.after_id:
            try:
                self.widget.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None

    def _show(self):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")
        lbl = tk.Label(
            self.tip,
            text=self.text,
            bg=self.theme["tooltip_bg"],
            fg=self.theme["tooltip_fg"],
            relief="solid",
            borderwidth=0,
            font=("Segoe UI", 9),
            padx=8,
            pady=4,
        )
        lbl.pack()

    def _hide(self, _evt=None):
        self._cancel()
        if self.tip:
            try:
                self.tip.destroy()
            except tk.TclError:
                pass
            self.tip = None


# ---------- Main App ----------
class RenamerApp:
    def __init__(self, root):
        self.root = root
        self.config = Config()

        self.lang = self.config.get("lang", "tr")
        self.theme_name = self.config.get("theme", "light")
        self.theme = DARK_THEME if self.theme_name == "dark" else LIGHT_THEME
        self.t = STRINGS[self.lang]

        self.root.title(self.t["title"])
        self.root.geometry("1060x960")
        self.root.minsize(980, 800)

        self._set_icon()

        self.last_operations = []        # [(new_path, old_path), ...]
        self.preview_data = []           # [(old_path, new_path, status_key, excluded_bool), ...]
        self.tooltips = []               # for theme updates

        # UI vars
        self.lang_var = tk.StringVar(value="Turkce" if self.lang == "tr" else "English")
        self.theme_var = tk.StringVar(value=self.t["dark"] if self.theme_name == "dark" else self.t["light"])
        self.folder_var = tk.StringVar()
        self.recursive_var = tk.BooleanVar(value=False)
        self.ext_var = tk.StringVar(value="")
        self.sort_var = tk.StringVar(value="name_asc")
        self.fr_enabled = tk.BooleanVar()
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.regex_var = tk.BooleanVar()
        self.multi_fr_enabled = tk.BooleanVar()
        self.prefix_enabled = tk.BooleanVar()
        self.prefix_var = tk.StringVar()
        self.suffix_enabled = tk.BooleanVar()
        self.suffix_var = tk.StringVar()
        self.num_enabled = tk.BooleanVar()
        self.basename_var = tk.StringVar(value="dosya")
        self.start_var = tk.IntVar(value=1)
        self.pad_var = tk.IntVar(value=3)
        self.case_enabled = tk.BooleanVar()
        self.case_type = tk.StringVar(value="lower")
        self.status_var = tk.StringVar(value=self.t["ready"])

        self._sort_keys = [
            "name_asc", "name_desc", "date_asc", "date_desc", "size_asc", "size_desc",
        ]

        self._style = ttk.Style()
        self._apply_theme()
        self._build_ui()
        self._apply_theme()  # yeniden uygula (widget'lar olustuktan sonra)
        self._bind_shortcuts()

        # drag-drop
        if DND_AVAILABLE:
            try:
                self.folder_entry.drop_target_register(DND_FILES)
                self.folder_entry.dnd_bind("<<Drop>>", self._on_folder_drop)
                self.tree.drop_target_register(DND_FILES)
                self.tree.dnd_bind("<<Drop>>", self._on_folder_drop)
            except tk.TclError:
                pass

    def _set_icon(self):
        for fname in ("app.ico", "icon_256.png"):
            path = resource_path(fname)
            if os.path.exists(path):
                try:
                    if fname.endswith(".ico"):
                        self.root.iconbitmap(default=path)
                    else:
                        self._icon_img = tk.PhotoImage(file=path)
                        self.root.iconphoto(True, self._icon_img)
                    return
                except tk.TclError:
                    continue

    # ---------- Theme ----------
    def _apply_theme(self):
        th = self.theme
        s = self._style
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        self.root.configure(bg=th["bg"])

        s.configure(".", background=th["bg"], foreground=th["fg"],
                    font=("Segoe UI", 10))
        s.configure("TFrame", background=th["bg"])
        s.configure("TLabel", background=th["bg"], foreground=th["fg"])
        s.configure("Hint.TLabel", background=th["bg"], foreground=th["muted"],
                    font=("Segoe UI", 9))
        s.configure("Title.TLabel", background=th["bg"], foreground=th["title_fg"],
                    font=("Segoe UI", 14, "bold"))
        s.configure("Header.TLabel", background=th["bg"], foreground=th["title_fg"],
                    font=("Segoe UI", 10, "bold"))

        s.configure("TLabelframe", background=th["frame_bg"], bordercolor=th["frame_border"],
                    relief="flat")
        s.configure("TLabelframe.Label",
                    background=th["bg"], foreground=th["title_fg"],
                    font=("Segoe UI", 10, "bold"))

        s.configure("TCheckbutton", background=th["bg"], foreground=th["fg"],
                    focuscolor=th["bg"])
        s.map("TCheckbutton",
              background=[("active", th["bg"])],
              foreground=[("disabled", th["muted"])])
        s.configure("TRadiobutton", background=th["bg"], foreground=th["fg"],
                    focuscolor=th["bg"])
        s.map("TRadiobutton", background=[("active", th["bg"])])

        s.configure("TEntry",
                    fieldbackground=th["entry_bg"],
                    foreground=th["entry_fg"],
                    bordercolor=th["btn_border"],
                    lightcolor=th["btn_border"],
                    darkcolor=th["btn_border"],
                    insertcolor=th["fg"])
        s.map("TEntry",
              fieldbackground=[("readonly", th["entry_bg"])],
              foreground=[("readonly", th["entry_fg"])])

        s.configure("TCombobox",
                    fieldbackground=th["entry_bg"],
                    background=th["btn_bg"],
                    foreground=th["entry_fg"],
                    bordercolor=th["btn_border"],
                    arrowcolor=th["fg"])
        s.map("TCombobox",
              fieldbackground=[("readonly", th["entry_bg"])],
              foreground=[("readonly", th["entry_fg"])],
              selectbackground=[("!focus", th["entry_bg"])],
              selectforeground=[("!focus", th["entry_fg"])])
        self.root.option_add("*TCombobox*Listbox.background", th["entry_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", th["entry_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", th["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", th["accent_fg"])

        s.configure("TSpinbox",
                    fieldbackground=th["entry_bg"],
                    foreground=th["entry_fg"],
                    background=th["btn_bg"],
                    bordercolor=th["btn_border"],
                    arrowcolor=th["fg"])

        # Normal buton
        s.configure("TButton",
                    background=th["btn_bg"],
                    foreground=th["btn_fg"],
                    bordercolor=th["btn_border"],
                    focuscolor=th["btn_bg"],
                    padding=(12, 6))
        s.map("TButton",
              background=[("active", th["btn_hover"])],
              bordercolor=[("active", th["accent"])])

        # Accent (ana) buton
        s.configure("Accent.TButton",
                    background=th["accent"],
                    foreground=th["accent_fg"],
                    bordercolor=th["accent"],
                    focuscolor=th["accent"],
                    font=("Segoe UI", 10, "bold"),
                    padding=(14, 7))
        s.map("Accent.TButton",
              background=[("active", th["accent_hover"])],
              bordercolor=[("active", th["accent_hover"])])

        # Treeview
        s.configure("Treeview",
                    background=th["tree_bg"],
                    fieldbackground=th["tree_bg"],
                    foreground=th["tree_fg"],
                    bordercolor=th["frame_border"],
                    rowheight=26,
                    font=("Segoe UI", 10))
        s.configure("Treeview.Heading",
                    background=th["tree_heading_bg"],
                    foreground=th["tree_heading_fg"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat",
                    padding=(6, 6))
        s.map("Treeview.Heading", background=[("active", th["btn_hover"])])
        s.map("Treeview", background=[("selected", th["tree_sel"])],
              foreground=[("selected", th["fg"])])

        # Scrollbar
        s.configure("Vertical.TScrollbar",
                    background=th["btn_bg"], troughcolor=th["bg"],
                    bordercolor=th["bg"], arrowcolor=th["fg"])
        s.configure("Horizontal.TScrollbar",
                    background=th["btn_bg"], troughcolor=th["bg"],
                    bordercolor=th["bg"], arrowcolor=th["fg"])

        # Separator
        s.configure("TSeparator", background=th["frame_border"])

        # Text widget (tk) manuel renklendirme
        if hasattr(self, "multi_fr_text"):
            self.multi_fr_text.configure(
                bg=th["entry_bg"], fg=th["entry_fg"],
                insertbackground=th["fg"],
                selectbackground=th["accent"], selectforeground=th["accent_fg"],
                highlightbackground=th["btn_border"],
                highlightcolor=th["accent"],
                borderwidth=1, relief="solid",
            )

        # Status bar
        if hasattr(self, "status_label"):
            self.status_label.configure(
                background=th["status_bg"],
                foreground=th["status_fg"],
            )

        # Treeview tag renkleri
        if hasattr(self, "tree"):
            self.tree.tag_configure("ok", background=th["tag_ok_bg"], foreground=th["tag_ok_fg"])
            self.tree.tag_configure("same", background=th["tag_same_bg"], foreground=th["tag_same_fg"])
            self.tree.tag_configure("conflict", background=th["tag_conflict_bg"], foreground=th["tag_conflict_fg"])
            self.tree.tag_configure("excluded", background=th["tag_excluded_bg"], foreground=th["tag_excluded_fg"])

        # Tooltip tema guncellemesi
        for tt in self.tooltips:
            tt.set_theme(th)

    def _toggle_theme(self, _evt=None):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.theme = DARK_THEME if self.theme_name == "dark" else LIGHT_THEME
        self.theme_var.set(self.t["dark"] if self.theme_name == "dark" else self.t["light"])
        self.config.set("theme", self.theme_name)
        self._apply_theme()

    # ---------- UI ----------
    def _section_title(self, parent, text):
        """LabelFrame yerine bir baslik + icerik frame donduren modern gorunum."""
        wrapper = ttk.Frame(parent)
        header = ttk.Label(wrapper, text=text, style="Header.TLabel")
        header.pack(anchor=tk.W, padx=4, pady=(0, 4))
        card = ttk.Frame(wrapper, style="Card.TFrame", padding=14)
        card.configure(style="TLabelframe")
        card.pack(fill=tk.BOTH, expand=True)
        return wrapper, card

    def _add_tooltip(self, widget, key):
        tt = Tooltip(widget, self.t.get(key, ""), self.theme)
        tt._key = key
        self.tooltips.append(tt)
        return tt

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill=tk.BOTH, expand=True)

        # --- Top bar ---
        top = ttk.Frame(outer)
        top.pack(fill=tk.X, pady=(0, 10))

        # Sol: baslik
        title_frame = ttk.Frame(top)
        title_frame.pack(side=tk.LEFT)
        ttk.Label(title_frame, text=APP_NAME, style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(title_frame, text=f"  v{APP_VERSION}", style="Hint.TLabel").pack(side=tk.LEFT)

        # Sag: kontroller
        controls = ttk.Frame(top)
        controls.pack(side=tk.RIGHT)

        self.lang_label = ttk.Label(controls, text=self.t["language"])
        self.lang_label.pack(side=tk.LEFT, padx=(0, 4))
        self.lang_combo = ttk.Combobox(
            controls, textvariable=self.lang_var,
            values=["Turkce", "English"], state="readonly", width=10,
        )
        self.lang_combo.pack(side=tk.LEFT, padx=(0, 12))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.theme_label = ttk.Label(controls, text=self.t["theme"])
        self.theme_label.pack(side=tk.LEFT, padx=(0, 4))
        self.theme_btn = ttk.Button(controls, textvariable=self.theme_var,
                                    command=self._toggle_theme, width=8)
        self.theme_btn.pack(side=tk.LEFT, padx=(0, 12))
        self._add_tooltip(self.theme_btn, "tt_theme")

        self.about_btn = ttk.Button(controls, text=self.t["about"],
                                    command=self.show_about, width=12)
        self.about_btn.pack(side=tk.LEFT)

        # --- Folder section ---
        folder_wrap, folder_card = self._section_title(outer, self.t["folder_section"])
        folder_wrap.pack(fill=tk.X, pady=(0, 12))
        self._folder_header = folder_wrap.winfo_children()[0]

        # Row 1: folder entry + recent dropdown + browse
        row1 = ttk.Frame(folder_card)
        row1.pack(fill=tk.X)
        self.folder_label = ttk.Label(row1, text=self.t["folder_label"])
        self.folder_label.pack(side=tk.LEFT)

        self.folder_entry = ttk.Entry(row1, textvariable=self.folder_var)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 6))

        self.recent_btn = ttk.Button(row1, text="▼ " + self.t["recent"],
                                     command=self._show_recent_menu, width=10)
        self.recent_btn.pack(side=tk.LEFT, padx=(0, 6))
        self._add_tooltip(self.recent_btn, "tt_recent")

        self.browse_btn = ttk.Button(row1, text=self.t["browse"],
                                     command=self.browse_folder, width=12)
        self.browse_btn.pack(side=tk.LEFT)
        self._add_tooltip(self.browse_btn, "tt_browse")

        # Row 2: dnd hint (if available) + recursive
        row2 = ttk.Frame(folder_card)
        row2.pack(fill=tk.X, pady=(8, 0))
        self.recursive_cb = ttk.Checkbutton(row2, text=self.t["recursive"],
                                            variable=self.recursive_var)
        self.recursive_cb.pack(side=tk.LEFT)
        self.dnd_hint_label = ttk.Label(
            row2,
            text=self.t["dnd_hint"] if DND_AVAILABLE else "",
            style="Hint.TLabel",
        )
        self.dnd_hint_label.pack(side=tk.RIGHT)

        # Row 3: ext filter + sort
        row3 = ttk.Frame(folder_card)
        row3.pack(fill=tk.X, pady=(8, 0))
        self.ext_filter_label = ttk.Label(row3, text=self.t["ext_filter"])
        self.ext_filter_label.pack(side=tk.LEFT)
        ttk.Entry(row3, textvariable=self.ext_var, width=24).pack(
            side=tk.LEFT, padx=(8, 6)
        )
        self.ext_hint_label = ttk.Label(row3, text=self.t["ext_hint"], style="Hint.TLabel")
        self.ext_hint_label.pack(side=tk.LEFT)

        self.sort_label = ttk.Label(row3, text=self.t["sort_label"])
        self.sort_label.pack(side=tk.RIGHT, padx=(0, 8))
        self.sort_combo = ttk.Combobox(
            row3, state="readonly", width=26,
            values=self._sort_values(),
        )
        self.sort_combo.current(0)
        self.sort_combo.pack(side=tk.RIGHT)
        self.sort_combo.bind("<<ComboboxSelected>>", self._on_sort_change)

        # --- Operations ---
        ops_wrap, ops_card = self._section_title(outer, self.t["ops_section"])
        ops_wrap.pack(fill=tk.X, pady=(0, 12))
        self._ops_header = ops_wrap.winfo_children()[0]

        # 1) Find/Replace
        self.fr_cb = ttk.Checkbutton(ops_card, text=self.t["find_replace"],
                                     variable=self.fr_enabled)
        self.fr_cb.grid(row=0, column=0, sticky=tk.W, padx=(0, 12), pady=3)
        self.find_label = ttk.Label(ops_card, text=self.t["find"])
        self.find_label.grid(row=0, column=1, sticky=tk.E)
        ttk.Entry(ops_card, textvariable=self.find_var, width=20).grid(
            row=0, column=2, padx=6)
        self.replace_label = ttk.Label(ops_card, text=self.t["replace"])
        self.replace_label.grid(row=0, column=3, sticky=tk.E)
        ttk.Entry(ops_card, textvariable=self.replace_var, width=20).grid(
            row=0, column=4, padx=6)
        self.regex_cb = ttk.Checkbutton(ops_card, text=self.t["regex"],
                                        variable=self.regex_var)
        self.regex_cb.grid(row=0, column=5, padx=6)
        self._add_tooltip(self.regex_cb, "tt_regex")

        # 2) Multi FR
        self.multi_fr_cb = ttk.Checkbutton(ops_card, text=self.t["multi_fr"],
                                           variable=self.multi_fr_enabled)
        self.multi_fr_cb.grid(row=1, column=0, sticky=tk.NW, pady=8)

        multi_frame = ttk.Frame(ops_card)
        multi_frame.grid(row=1, column=1, columnspan=6, sticky=tk.EW, padx=6, pady=8)
        ops_card.columnconfigure(1, weight=1)

        self.multi_hint_label = ttk.Label(
            multi_frame, text=self.t["multi_fr_hint"],
            style="Hint.TLabel", wraplength=820, justify=tk.LEFT,
        )
        self.multi_hint_label.pack(anchor=tk.W)

        text_container = ttk.Frame(multi_frame)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self.multi_fr_text = tk.Text(
            text_container, height=6, width=70, wrap=tk.NONE,
            font=("Consolas", 10), undo=True, borderwidth=1, relief="solid",
        )
        sb_y = ttk.Scrollbar(text_container, orient=tk.VERTICAL,
                             command=self.multi_fr_text.yview)
        sb_x = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL,
                             command=self.multi_fr_text.xview)
        self.multi_fr_text.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        self.multi_fr_text.grid(row=0, column=0, sticky=tk.NSEW)
        sb_y.grid(row=0, column=1, sticky=tk.NS)
        sb_x.grid(row=1, column=0, sticky=tk.EW)
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)
        self.multi_fr_text.insert("1.0", self.t["multi_example"])

        # 3) Prefix
        self.prefix_cb = ttk.Checkbutton(ops_card, text=self.t["prefix_add"],
                                         variable=self.prefix_enabled)
        self.prefix_cb.grid(row=2, column=0, sticky=tk.W, pady=6)
        self.prefix_text_label = ttk.Label(ops_card, text=self.t["text"])
        self.prefix_text_label.grid(row=2, column=1, sticky=tk.E)
        ttk.Entry(ops_card, textvariable=self.prefix_var, width=20).grid(
            row=2, column=2, padx=6, pady=6)

        # 4) Suffix
        self.suffix_cb = ttk.Checkbutton(ops_card, text=self.t["suffix_add"],
                                         variable=self.suffix_enabled)
        self.suffix_cb.grid(row=3, column=0, sticky=tk.W, pady=6)
        self.suffix_text_label = ttk.Label(ops_card, text=self.t["text"])
        self.suffix_text_label.grid(row=3, column=1, sticky=tk.E)
        ttk.Entry(ops_card, textvariable=self.suffix_var, width=20).grid(
            row=3, column=2, padx=6, pady=6)
        self.suffix_hint_label = ttk.Label(ops_card, text=self.t["suffix_hint"], style="Hint.TLabel")
        self.suffix_hint_label.grid(row=3, column=3, columnspan=3, sticky=tk.W)

        # 5) Numbering
        self.num_cb = ttk.Checkbutton(ops_card, text=self.t["numbering"],
                                      variable=self.num_enabled)
        self.num_cb.grid(row=4, column=0, sticky=tk.W, pady=6)
        self.basename_label = ttk.Label(ops_card, text=self.t["base_name"])
        self.basename_label.grid(row=4, column=1, sticky=tk.E)
        ttk.Entry(ops_card, textvariable=self.basename_var, width=20).grid(
            row=4, column=2, padx=6, pady=6)
        self.start_label = ttk.Label(ops_card, text=self.t["start"])
        self.start_label.grid(row=4, column=3, sticky=tk.E)
        ttk.Spinbox(ops_card, from_=0, to=999999, textvariable=self.start_var, width=8).grid(
            row=4, column=4, sticky=tk.W, padx=6)
        self.pad_label = ttk.Label(ops_card, text=self.t["pad"])
        self.pad_label.grid(row=4, column=5, sticky=tk.E)
        ttk.Spinbox(ops_card, from_=1, to=10, textvariable=self.pad_var, width=5).grid(
            row=4, column=6, sticky=tk.W, padx=6)

        # 6) Case
        self.case_cb = ttk.Checkbutton(ops_card, text=self.t["case_conv"],
                                       variable=self.case_enabled)
        self.case_cb.grid(row=5, column=0, sticky=tk.W, pady=6)
        self.case_type = tk.StringVar(value="lower")
        case_box = ttk.Frame(ops_card)
        case_box.grid(row=5, column=1, columnspan=6, sticky=tk.W, padx=6)
        self.case_lower_rb = ttk.Radiobutton(case_box, text=self.t["case_lower"],
                                             variable=self.case_type, value="lower")
        self.case_lower_rb.pack(side=tk.LEFT, padx=6)
        self.case_upper_rb = ttk.Radiobutton(case_box, text=self.t["case_upper"],
                                             variable=self.case_type, value="upper")
        self.case_upper_rb.pack(side=tk.LEFT, padx=6)
        self.case_title_rb = ttk.Radiobutton(case_box, text=self.t["case_title"],
                                             variable=self.case_type, value="title")
        self.case_title_rb.pack(side=tk.LEFT, padx=6)

        # --- Action buttons ---
        btns = ttk.Frame(outer)
        btns.pack(fill=tk.X, pady=(0, 10))

        self.preview_btn = ttk.Button(btns, text="🔍  " + self.t["preview"],
                                      command=self.preview, style="Accent.TButton", width=16)
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 6))
        self._add_tooltip(self.preview_btn, "tt_preview")

        self.apply_btn = ttk.Button(btns, text="✓  " + self.t["apply"],
                                    command=self.apply, width=16)
        self.apply_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.apply_btn, "tt_apply")

        self.undo_btn = ttk.Button(btns, text="↶  " + self.t["undo"],
                                   command=self.undo, width=14)
        self.undo_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.undo_btn, "tt_undo")

        self.clear_btn = ttk.Button(btns, text=self.t["clear"],
                                    command=self.clear_all, width=12)
        self.clear_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.clear_btn, "tt_clear")

        ttk.Separator(btns, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.save_profile_btn = ttk.Button(btns, text="💾  " + self.t["save_profile"],
                                           command=self.save_profile, width=18)
        self.save_profile_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.save_profile_btn, "tt_save_profile")

        self.load_profile_btn = ttk.Button(btns, text="📂  " + self.t["load_profile"],
                                           command=self.load_profile, width=18)
        self.load_profile_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.load_profile_btn, "tt_load_profile")

        # --- Preview area ---
        preview_wrap, preview_card = self._section_title(outer, self.t["preview_section"])
        preview_wrap.pack(fill=tk.BOTH, expand=True)
        self._preview_header = preview_wrap.winfo_children()[0]

        # Tree toolbar
        tree_tools = ttk.Frame(preview_card)
        tree_tools.pack(fill=tk.X, pady=(0, 6))
        self.exclude_btn = ttk.Button(tree_tools, text="✗  " + self.t["exclude_selected"],
                                      command=self.exclude_selected, width=22)
        self.exclude_btn.pack(side=tk.LEFT, padx=(0, 6))
        self._add_tooltip(self.exclude_btn, "tt_exclude")
        self.include_btn = ttk.Button(tree_tools, text="✓  " + self.t["include_selected"],
                                      command=self.include_selected, width=20)
        self.include_btn.pack(side=tk.LEFT, padx=6)
        self._add_tooltip(self.include_btn, "tt_include")
        self.include_all_btn = ttk.Button(tree_tools, text=self.t["include_all"],
                                          command=self.include_all, width=18)
        self.include_all_btn.pack(side=tk.LEFT, padx=6)

        # Tree
        tree_container = ttk.Frame(preview_card)
        tree_container.pack(fill=tk.BOTH, expand=True)
        columns = ("old", "new", "status")
        self.tree = ttk.Treeview(
            tree_container, columns=columns, show="headings",
            height=14, selectmode="extended",
        )
        self.tree.heading("old", text=self.t["col_old"])
        self.tree.heading("new", text=self.t["col_new"])
        self.tree.heading("status", text=self.t["col_status"])
        self.tree.column("old", width=420)
        self.tree.column("new", width=420)
        self.tree.column("status", width=120, anchor=tk.CENTER)
        scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<Double-Button-1>", self._on_tree_double)
        self.tree.bind("<space>", lambda _e: self.toggle_selected_excluded())
        self.tree.bind("<Delete>", lambda _e: self.exclude_selected())

        # Status bar
        self.status_label = tk.Label(outer, textvariable=self.status_var,
                                     anchor=tk.W, padx=10, pady=6,
                                     bg=self.theme["status_bg"],
                                     fg=self.theme["status_fg"],
                                     font=("Segoe UI", 9))
        self.status_label.pack(fill=tk.X, pady=(10, 0))

    # ---------- Shortcuts ----------
    def _bind_shortcuts(self):
        self.root.bind_all("<Control-o>", lambda _e: self.browse_folder())
        self.root.bind_all("<Control-O>", lambda _e: self.browse_folder())
        self.root.bind_all("<Control-p>", lambda _e: self.preview())
        self.root.bind_all("<Control-P>", lambda _e: self.preview())
        self.root.bind_all("<Control-Return>", lambda _e: self.apply())
        self.root.bind_all("<Control-z>", lambda _e: self.undo())
        self.root.bind_all("<Control-Z>", lambda _e: self.undo())
        self.root.bind_all("<Control-s>", lambda _e: self.save_profile())
        self.root.bind_all("<Control-S>", lambda _e: self.save_profile())
        self.root.bind_all("<Control-l>", lambda _e: self.load_profile())
        self.root.bind_all("<Control-L>", lambda _e: self.load_profile())
        self.root.bind_all("<F1>", lambda _e: self.show_about())

    # ---------- Sort combobox ----------
    def _sort_values(self):
        return [self.t[f"sort_{k}"] for k in self._sort_keys]

    def _on_sort_change(self, _evt=None):
        idx = self.sort_combo.current()
        if idx >= 0:
            self.sort_var.set(self._sort_keys[idx])

    def _get_sort_key(self):
        return self.sort_var.get() or "name_asc"

    # ---------- Recent folders ----------
    def _show_recent_menu(self):
        recent = self.config.get("recent", [])
        menu = tk.Menu(self.root, tearoff=0,
                       bg=self.theme["frame_bg"], fg=self.theme["fg"],
                       activebackground=self.theme["accent"],
                       activeforeground=self.theme["accent_fg"])
        if not recent:
            menu.add_command(label="(empty)", state=tk.DISABLED)
        else:
            for path in recent:
                display = path if len(path) < 80 else "..." + path[-77:]
                menu.add_command(label=display,
                                 command=lambda p=path: self.folder_var.set(p))
        x = self.recent_btn.winfo_rootx()
        y = self.recent_btn.winfo_rooty() + self.recent_btn.winfo_height()
        menu.tk_popup(x, y)

    # ---------- Language ----------
    def _on_lang_change(self, _evt=None):
        v = self.lang_var.get()
        new_lang = "en" if v == "English" else "tr"
        if new_lang != self.lang:
            self.lang = new_lang
            self.t = STRINGS[self.lang]
            self.config.set("lang", self.lang)
            self._apply_translations()

    def _apply_translations(self):
        t = self.t
        self.root.title(t["title"])
        self.lang_label.configure(text=t["language"])
        self.theme_label.configure(text=t["theme"])
        self.theme_var.set(t["dark"] if self.theme_name == "dark" else t["light"])
        self.about_btn.configure(text=t["about"])
        self._folder_header.configure(text=t["folder_section"])
        self.folder_label.configure(text=t["folder_label"])
        self.browse_btn.configure(text=t["browse"])
        self.recent_btn.configure(text="▼ " + t["recent"])
        self.recursive_cb.configure(text=t["recursive"])
        self.ext_filter_label.configure(text=t["ext_filter"])
        self.ext_hint_label.configure(text=t["ext_hint"])
        self.sort_label.configure(text=t["sort_label"])
        self.sort_combo.configure(values=self._sort_values())
        self.sort_combo.current(self._sort_keys.index(self._get_sort_key()))
        self.dnd_hint_label.configure(text=t["dnd_hint"] if DND_AVAILABLE else "")
        self._ops_header.configure(text=t["ops_section"])
        self.fr_cb.configure(text=t["find_replace"])
        self.find_label.configure(text=t["find"])
        self.replace_label.configure(text=t["replace"])
        self.regex_cb.configure(text=t["regex"])
        self.multi_fr_cb.configure(text=t["multi_fr"])
        self.multi_hint_label.configure(text=t["multi_fr_hint"])
        self.prefix_cb.configure(text=t["prefix_add"])
        self.prefix_text_label.configure(text=t["text"])
        self.suffix_cb.configure(text=t["suffix_add"])
        self.suffix_text_label.configure(text=t["text"])
        self.suffix_hint_label.configure(text=t["suffix_hint"])
        self.num_cb.configure(text=t["numbering"])
        self.basename_label.configure(text=t["base_name"])
        self.start_label.configure(text=t["start"])
        self.pad_label.configure(text=t["pad"])
        self.case_cb.configure(text=t["case_conv"])
        self.case_lower_rb.configure(text=t["case_lower"])
        self.case_upper_rb.configure(text=t["case_upper"])
        self.case_title_rb.configure(text=t["case_title"])
        self.preview_btn.configure(text="🔍  " + t["preview"])
        self.apply_btn.configure(text="✓  " + t["apply"])
        self.undo_btn.configure(text="↶  " + t["undo"])
        self.clear_btn.configure(text=t["clear"])
        self.save_profile_btn.configure(text="💾  " + t["save_profile"])
        self.load_profile_btn.configure(text="📂  " + t["load_profile"])
        self._preview_header.configure(text=t["preview_section"])
        self.exclude_btn.configure(text="✗  " + t["exclude_selected"])
        self.include_btn.configure(text="✓  " + t["include_selected"])
        self.include_all_btn.configure(text=t["include_all"])
        self.tree.heading("old", text=t["col_old"])
        self.tree.heading("new", text=t["col_new"])
        self.tree.heading("status", text=t["col_status"])
        self.status_var.set(t["ready"])

        # Tooltip metinleri
        for tt in self.tooltips:
            key = getattr(tt, "_key", None)
            if key:
                tt.set_text(t.get(key, ""))

        # Onizleme durumlarini yenile
        self._refresh_preview_labels()

    def _refresh_preview_labels(self):
        status_map = {
            "ok": self.t["status_ok"],
            "same": self.t["status_same"],
            "conflict": self.t["status_conflict"],
            "exists": self.t["status_exists"],
            "excluded": self.t["status_excluded"],
        }
        ids = self.tree.get_children()
        for item_id, rec in zip(ids, self.preview_data):
            old, new, key, excluded = rec
            vals = list(self.tree.item(item_id, "values"))
            if excluded:
                vals[2] = status_map["excluded"]
            else:
                vals[2] = status_map.get(key, vals[2])
            self.tree.item(item_id, values=vals)

    # ---------- About ----------
    def show_about(self):
        t = self.t
        win = tk.Toplevel(self.root)
        win.title(t["about_title"])
        win.geometry("520x580")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()
        win.configure(bg=self.theme["bg"])

        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 520) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 580) // 2
        win.geometry(f"+{max(0, x)}+{max(0, y)}")

        # Main frame
        container = ttk.Frame(win, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Icon
        icon_path = resource_path("icon_256.png")
        if os.path.exists(icon_path):
            try:
                img = tk.PhotoImage(file=icon_path)
                factor = max(1, img.width() // 90)
                img = img.subsample(factor, factor)
                self._about_icon = img
                ttk.Label(container, image=img).pack(pady=(0, 10))
            except tk.TclError:
                pass

        ttk.Label(container, text=t["about_app_name"],
                  font=("Segoe UI", 16, "bold"),
                  foreground=self.theme["title_fg"],
                  background=self.theme["bg"]).pack()
        ttk.Label(container, text=t["about_version"],
                  foreground=self.theme["muted"],
                  background=self.theme["bg"]).pack(pady=(2, 12))

        ttk.Label(container, text=t["about_desc"],
                  wraplength=460, justify=tk.CENTER,
                  foreground=self.theme["fg"],
                  background=self.theme["bg"]).pack(pady=(0, 14))

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=4)

        ttk.Label(container, text=f"{t['about_developer']}: Ayberk Baglan",
                  font=("Segoe UI", 11, "bold"),
                  foreground=self.theme["title_fg"],
                  background=self.theme["bg"]).pack(pady=(10, 4))

        ttk.Label(container, text=t["about_contact"] + ":",
                  font=("Segoe UI", 10, "bold"),
                  foreground=self.theme["fg"],
                  background=self.theme["bg"]).pack(anchor=tk.CENTER, pady=(4, 4))

        links_frame = ttk.Frame(container)
        links_frame.pack()
        links = [
            ("🔗  GitHub", "https://github.com/ayberkbgln"),
            ("💼  LinkedIn", "https://www.linkedin.com/in/ayberkbaglan/"),
            ("𝕏  X / Twitter", "https://x.com/yulewiz"),
            ("✉  ayberkbaglan@gmail.com", "mailto:ayberkbaglan@gmail.com"),
        ]
        for label, url in links:
            self._make_link(links_frame, label, url).pack(pady=2)

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)

        bottom = ttk.Frame(container)
        bottom.pack(fill=tk.X, pady=(0, 4))
        self._make_link(bottom, "📦  " + t["about_source"],
                        "https://github.com/ayberkbgln/bulk-file-renamer"
                        ).pack(side=tk.LEFT)
        ttk.Label(bottom, text=t["about_license"],
                  foreground=self.theme["muted"],
                  background=self.theme["bg"]).pack(side=tk.RIGHT)

        ttk.Button(container, text=t["about_close"], command=win.destroy,
                   width=14).pack(pady=(16, 0))

        # Esc kapat
        win.bind("<Escape>", lambda _e: win.destroy())

    def _make_link(self, parent, text, url):
        lbl = tk.Label(parent, text=text, fg=self.theme["link"],
                       bg=self.theme["bg"], cursor="hand2",
                       font=("Segoe UI", 10, "underline"))
        lbl.bind("<Button-1>", lambda _e, u=url: webbrowser.open(u))
        return lbl

    # ---------- Drag & Drop ----------
    def _on_folder_drop(self, event):
        data = event.data or ""
        # tkinterdnd2 birden fazla dosya icin: {C:/a b} {C:/c}
        if data.startswith("{") and "}" in data:
            path = data[1:data.index("}")]
        else:
            path = data.split()[0] if data else ""
        if path and os.path.isdir(path):
            self.folder_var.set(path)
        elif path and os.path.isfile(path):
            # Dosya birakildiysa klasorunu al
            self.folder_var.set(os.path.dirname(path))

    # ---------- Logic ----------
    def browse_folder(self):
        folder = filedialog.askdirectory(title=self.t["folder_label"])
        if folder:
            self.folder_var.set(folder)

    def _sort_files(self, files, key):
        if key == "name_asc":
            return sorted(files, key=lambda p: os.path.basename(p).lower())
        if key == "name_desc":
            return sorted(files, key=lambda p: os.path.basename(p).lower(), reverse=True)
        if key == "date_asc":
            return sorted(files, key=lambda p: os.path.getmtime(p))
        if key == "date_desc":
            return sorted(files, key=lambda p: os.path.getmtime(p), reverse=True)
        if key == "size_asc":
            return sorted(files, key=lambda p: os.path.getsize(p))
        if key == "size_desc":
            return sorted(files, key=lambda p: os.path.getsize(p), reverse=True)
        return files

    def get_files(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror(self.t["err_title"], self.t["err_invalid_folder"])
            return []

        self.config.add_recent(folder)

        exts_raw = self.ext_var.get().strip()
        exts = None
        if exts_raw:
            exts = [e.strip().lower() for e in exts_raw.split(",") if e.strip()]
            exts = [e if e.startswith(".") else "." + e for e in exts]

        files = []
        if self.recursive_var.get():
            for root, _dirs, fns in os.walk(folder):
                for fn in fns:
                    path = os.path.join(root, fn)
                    if exts is None or os.path.splitext(fn)[1].lower() in exts:
                        files.append(path)
        else:
            for fn in os.listdir(folder):
                path = os.path.join(folder, fn)
                if os.path.isfile(path):
                    if exts is None or os.path.splitext(fn)[1].lower() in exts:
                        files.append(path)

        files = self._sort_files(files, self._get_sort_key())
        return files

    def _parse_multi_rules(self):
        raw = self.multi_fr_text.get("1.0", tk.END)
        rules = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "\t" in line:
                parts = line.split("\t", 1)
                find = parts[0].strip()
                replace = parts[1].strip() if len(parts) > 1 else ""
            else:
                m = re.match(r"^(\S+)\s+(.*)$", line)
                if m:
                    find = m.group(1)
                    replace = m.group(2).rstrip()
                else:
                    find = stripped
                    replace = ""
            if find:
                rules.append((find, replace))
        return rules

    def _compute_new_name(self, old_path, index):
        folder = os.path.dirname(old_path)
        fn = os.path.basename(old_path)
        stem, ext = os.path.splitext(fn)

        if self.fr_enabled.get():
            find = self.find_var.get()
            replace = self.replace_var.get()
            if find:
                if self.regex_var.get():
                    try:
                        stem = re.sub(find, replace, stem)
                    except re.error as e:
                        raise ValueError(self.t["regex_err"].format(e=e))
                else:
                    stem = stem.replace(find, replace)

        if self.multi_fr_enabled.get():
            for find, replace in self._parse_multi_rules():
                stem = stem.replace(find, replace)

        if self.num_enabled.get():
            base = self.basename_var.get()
            try:
                start = int(self.start_var.get())
                pad = int(self.pad_var.get())
            except (tk.TclError, ValueError):
                start, pad = 1, 3
            num = str(start + index).zfill(max(1, pad))
            stem = f"{base}{num}" if base else num

        if self.prefix_enabled.get():
            stem = self.prefix_var.get() + stem
        if self.suffix_enabled.get():
            stem = stem + self.suffix_var.get()

        if self.case_enabled.get():
            ct = self.case_type.get()
            if ct == "lower":
                stem = stem.lower()
                ext = ext.lower()
            elif ct == "upper":
                stem = stem.upper()
                ext = ext.lower()
            elif ct == "title":
                stem = stem.title()

        return os.path.join(folder, stem + ext)

    def preview(self):
        self.tree.delete(*self.tree.get_children())
        self.preview_data = []

        any_op = any([
            self.fr_enabled.get(), self.multi_fr_enabled.get(),
            self.prefix_enabled.get(), self.suffix_enabled.get(),
            self.num_enabled.get(), self.case_enabled.get(),
        ])
        if not any_op:
            messagebox.showwarning(self.t["warn_title"], self.t["warn_need_op"])
            return

        files = self.get_files()
        if not files:
            self.status_var.set(self.t["no_files"])
            return

        try:
            seen_new = set()
            for i, old in enumerate(files):
                new = self._compute_new_name(old, i)
                if old == new:
                    key = "same"
                elif new in seen_new:
                    key = "conflict"
                elif os.path.exists(new) and os.path.normcase(new) != os.path.normcase(old):
                    key = "exists"
                else:
                    key = "ok"
                seen_new.add(new)
                self.preview_data.append([old, new, key, False])
                status_text = {
                    "ok": self.t["status_ok"],
                    "same": self.t["status_same"],
                    "conflict": self.t["status_conflict"],
                    "exists": self.t["status_exists"],
                }[key]
                tag = "conflict" if key in ("conflict", "exists") else key
                self.tree.insert("", tk.END,
                                 values=(os.path.basename(old),
                                         os.path.basename(new), status_text),
                                 tags=(tag,))
        except ValueError as e:
            messagebox.showerror(self.t["err_title"], str(e))
            return

        self._update_summary()

    def _update_summary(self):
        ok_count = sum(1 for rec in self.preview_data
                       if rec[2] == "ok" and not rec[3])
        excluded_count = sum(1 for rec in self.preview_data if rec[3])
        conflict_count = sum(1 for rec in self.preview_data
                             if rec[2] in ("conflict", "exists") and not rec[3])
        self.status_var.set(self.t["summary"].format(
            t=len(self.preview_data), ok=ok_count,
            ex=excluded_count, c=conflict_count,
        ))

    # --- Row inclusion/exclusion ---
    def _on_tree_double(self, _evt=None):
        self.toggle_selected_excluded()

    def exclude_selected(self):
        for item_id in self.tree.selection():
            idx = self.tree.index(item_id)
            if 0 <= idx < len(self.preview_data):
                self.preview_data[idx][3] = True
        self._refresh_tree_rows()
        self._update_summary()

    def include_selected(self):
        for item_id in self.tree.selection():
            idx = self.tree.index(item_id)
            if 0 <= idx < len(self.preview_data):
                self.preview_data[idx][3] = False
        self._refresh_tree_rows()
        self._update_summary()

    def include_all(self):
        for rec in self.preview_data:
            rec[3] = False
        self._refresh_tree_rows()
        self._update_summary()

    def toggle_selected_excluded(self):
        for item_id in self.tree.selection():
            idx = self.tree.index(item_id)
            if 0 <= idx < len(self.preview_data):
                self.preview_data[idx][3] = not self.preview_data[idx][3]
        self._refresh_tree_rows()
        self._update_summary()

    def _refresh_tree_rows(self):
        status_map = {
            "ok": self.t["status_ok"],
            "same": self.t["status_same"],
            "conflict": self.t["status_conflict"],
            "exists": self.t["status_exists"],
            "excluded": self.t["status_excluded"],
        }
        for item_id, rec in zip(self.tree.get_children(), self.preview_data):
            old, new, key, excluded = rec
            if excluded:
                status = status_map["excluded"]
                tag = "excluded"
            elif key in ("conflict", "exists"):
                status = status_map[key]
                tag = "conflict"
            else:
                status = status_map[key]
                tag = key
            self.tree.item(item_id, values=(os.path.basename(old),
                                            os.path.basename(new), status),
                           tags=(tag,))

    # --- Apply / Undo ---
    def apply(self):
        if not self.preview_data:
            messagebox.showwarning(self.t["warn_title"], self.t["need_preview"])
            return

        ok_items = [rec for rec in self.preview_data
                    if rec[2] == "ok" and not rec[3]]
        if not ok_items:
            messagebox.showinfo(self.t["info_title"], self.t["nothing_to_rename"])
            return

        conflicts = [rec for rec in self.preview_data
                     if rec[2] in ("conflict", "exists") and not rec[3]]
        if conflicts:
            if not messagebox.askyesno(self.t["warn_title"],
                                       self.t["conflict_warn"].format(n=len(conflicts))):
                return

        if not messagebox.askyesno(self.t["info_title"],
                                   self.t["confirm_apply"].format(n=len(ok_items))):
            return

        temp_map = []
        failed = 0
        for rec in ok_items:
            old, new = rec[0], rec[1]
            tmp = old + ".___rntmp___"
            try:
                os.rename(old, tmp)
                temp_map.append((tmp, new, old))
            except OSError:
                failed += 1

        success = 0
        self.last_operations = []
        for tmp, new, orig in temp_map:
            try:
                os.makedirs(os.path.dirname(new), exist_ok=True)
                os.rename(tmp, new)
                self.last_operations.append((new, orig))
                success += 1
            except OSError:
                try:
                    os.rename(tmp, orig)
                except OSError:
                    pass
                failed += 1

        messagebox.showinfo(self.t["done"],
                            self.t["done_msg"].format(s=success, f=failed))
        self.status_var.set(self.t["done_status"].format(s=success, f=failed))
        self.preview()

    def undo(self):
        if not self.last_operations:
            messagebox.showinfo(self.t["info_title"], self.t["undo_none"])
            return
        if not messagebox.askyesno(self.t["info_title"],
                                   self.t["undo_confirm"].format(n=len(self.last_operations))):
            return
        success = 0
        failed = 0
        for new, old in reversed(self.last_operations):
            try:
                os.rename(new, old)
                success += 1
            except OSError:
                failed += 1
        self.last_operations = []
        messagebox.showinfo(self.t["undone"],
                            self.t["done_msg"].format(s=success, f=failed))
        self.status_var.set(self.t["undo_status"].format(n=success))
        self.preview()

    def clear_all(self):
        for var in (
            self.fr_enabled, self.multi_fr_enabled, self.prefix_enabled,
            self.suffix_enabled, self.num_enabled, self.case_enabled,
            self.regex_var, self.recursive_var,
        ):
            var.set(False)
        for var in (self.find_var, self.replace_var, self.prefix_var,
                    self.suffix_var, self.ext_var):
            var.set("")
        self.basename_var.set("dosya")
        self.start_var.set(1)
        self.pad_var.set(3)
        self.case_type.set("lower")
        self.sort_combo.current(0)
        self.sort_var.set("name_asc")
        self.multi_fr_text.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())
        self.preview_data = []
        self.status_var.set(self.t["cleared"])

    # --- Profiles ---
    def _gather_profile(self):
        return {
            "version": 1,
            "find_replace": {
                "enabled": self.fr_enabled.get(),
                "find": self.find_var.get(),
                "replace": self.replace_var.get(),
                "regex": self.regex_var.get(),
            },
            "multi_fr": {
                "enabled": self.multi_fr_enabled.get(),
                "rules": self.multi_fr_text.get("1.0", tk.END).rstrip("\n"),
            },
            "prefix": {"enabled": self.prefix_enabled.get(),
                       "text": self.prefix_var.get()},
            "suffix": {"enabled": self.suffix_enabled.get(),
                       "text": self.suffix_var.get()},
            "numbering": {
                "enabled": self.num_enabled.get(),
                "base": self.basename_var.get(),
                "start": int(self.start_var.get() or 1),
                "pad": int(self.pad_var.get() or 3),
            },
            "case": {"enabled": self.case_enabled.get(),
                     "type": self.case_type.get()},
            "recursive": self.recursive_var.get(),
            "ext_filter": self.ext_var.get(),
            "sort": self._get_sort_key(),
        }

    def _apply_profile(self, data):
        fr = data.get("find_replace", {})
        self.fr_enabled.set(fr.get("enabled", False))
        self.find_var.set(fr.get("find", ""))
        self.replace_var.set(fr.get("replace", ""))
        self.regex_var.set(fr.get("regex", False))

        mfr = data.get("multi_fr", {})
        self.multi_fr_enabled.set(mfr.get("enabled", False))
        self.multi_fr_text.delete("1.0", tk.END)
        self.multi_fr_text.insert("1.0", mfr.get("rules", ""))

        pre = data.get("prefix", {})
        self.prefix_enabled.set(pre.get("enabled", False))
        self.prefix_var.set(pre.get("text", ""))

        suf = data.get("suffix", {})
        self.suffix_enabled.set(suf.get("enabled", False))
        self.suffix_var.set(suf.get("text", ""))

        num = data.get("numbering", {})
        self.num_enabled.set(num.get("enabled", False))
        self.basename_var.set(num.get("base", "dosya"))
        self.start_var.set(int(num.get("start", 1)))
        self.pad_var.set(int(num.get("pad", 3)))

        ca = data.get("case", {})
        self.case_enabled.set(ca.get("enabled", False))
        self.case_type.set(ca.get("type", "lower"))

        self.recursive_var.set(data.get("recursive", False))
        self.ext_var.set(data.get("ext_filter", ""))

        sort_key = data.get("sort", "name_asc")
        if sort_key in self._sort_keys:
            self.sort_var.set(sort_key)
            self.sort_combo.current(self._sort_keys.index(sort_key))

    def save_profile(self):
        path = filedialog.asksaveasfilename(
            title=self.t["profile_save_title"],
            defaultextension=".json",
            filetypes=[(self.t["json_files"], "*.json")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._gather_profile(), f, indent=2, ensure_ascii=False)
            self.status_var.set(self.t["profile_saved"] + f"  ({os.path.basename(path)})")
        except OSError as e:
            messagebox.showerror(self.t["err_title"], str(e))

    def load_profile(self):
        path = filedialog.askopenfilename(
            title=self.t["profile_load_title"],
            filetypes=[(self.t["json_files"], "*.json")],
        )
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self._apply_profile(data)
            self.status_var.set(self.t["profile_loaded"] + f"  ({os.path.basename(path)})")
        except (OSError, json.JSONDecodeError, ValueError) as e:
            messagebox.showerror(
                self.t["err_title"], self.t["profile_load_err"].format(e=e)
            )


def main():
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    RenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
