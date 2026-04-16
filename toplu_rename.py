"""
Bulk File Renamer / Toplu Dosya Yeniden Adlandirici
GUI ile coklu islem destegi: bul/degistir, coklu kural listesi, onek/sonek,
numaralandirma, harf donusumu. Dil secici (TR/EN) ve About dahil.

Author: Ayberk Baglan
GitHub: https://github.com/ayberkbgln
"""

import os
import re
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ---------- Localization ----------
STRINGS = {
    "tr": {
        "title": "Toplu Dosya Yeniden Adlandirici",
        "folder_section": "Klasor Secimi",
        "folder_label": "Klasor:",
        "browse": "Gozat...",
        "recursive": "Alt klasorleri de dahil et",
        "ext_filter": "Uzanti filtresi:",
        "ext_hint": "(orn: .jpg,.png - bos birakilirsa tum dosyalar)",
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
        "preview_section": "Onizleme",
        "col_old": "Eski Ad",
        "col_new": "Yeni Ad",
        "col_status": "Durum",
        "ready": "Hazir. Klasor secip 'Onizleme'ye basin.",
        "status_ok": "OK",
        "status_same": "Degismez",
        "status_conflict": "Cakisma!",
        "status_exists": "Mevcut!",
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
        "summary": "Toplam: {t} dosya   |   Degisecek: {ok}   |   Sorunlu: {c}",
        "regex_err": "Regex hatasi: {e}",
        "language": "Dil:",
        # About
        "about_title": "Hakkinda",
        "about_app_name": "Toplu Dosya Yeniden Adlandirici",
        "about_version": "Surum 1.1.0",
        "about_desc": "Coklu kurali tek seferde uygulayabilen, GUI tabanli, ucretsiz ve acik kaynak bir yeniden adlandirma aracidir.",
        "about_developer": "Gelistiren",
        "about_contact": "Iletisim",
        "about_license": "Lisans: MIT",
        "about_close": "Kapat",
        "about_source": "Kaynak Kod",
    },
    "en": {
        "title": "Bulk File Renamer",
        "folder_section": "Folder Selection",
        "folder_label": "Folder:",
        "browse": "Browse...",
        "recursive": "Include subfolders",
        "ext_filter": "Extension filter:",
        "ext_hint": "(e.g. .jpg,.png - leave empty for all files)",
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
        "preview_section": "Preview",
        "col_old": "Old Name",
        "col_new": "New Name",
        "col_status": "Status",
        "ready": "Ready. Pick a folder and click 'Preview'.",
        "status_ok": "OK",
        "status_same": "Unchanged",
        "status_conflict": "Conflict!",
        "status_exists": "Exists!",
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
        "summary": "Total: {t} files   |   Will change: {ok}   |   Problematic: {c}",
        "regex_err": "Regex error: {e}",
        "language": "Language:",
        # About
        "about_title": "About",
        "about_app_name": "Bulk File Renamer",
        "about_version": "Version 1.1.0",
        "about_desc": "A free, open-source, GUI-based bulk file renamer that can combine multiple rules in a single pass.",
        "about_developer": "Developed by",
        "about_contact": "Contact",
        "about_license": "License: MIT",
        "about_close": "Close",
        "about_source": "Source Code",
    },
}


def resource_path(rel: str) -> str:
    """Return absolute path to a resource, works for dev and for PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


class RenamerApp:
    def __init__(self, root):
        self.root = root
        self.lang = "tr"
        self.t = STRINGS[self.lang]

        self.root.title(self.t["title"])
        self.root.geometry("1000x920")
        self.root.minsize(920, 780)

        # Icon
        self._set_icon()

        self.last_operations = []   # geri al icin: [(new_path, old_path), ...]
        self.preview_data = []      # [(old_path, new_path, status_key), ...]

        # UI variables
        self.lang_var = tk.StringVar(value="Turkce")

        self._build_ui()

    def _set_icon(self):
        """Uygulama iconunu ayarla (ico veya png)."""
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

    # ---------- UI ----------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Ust bar: dil ve about
        top_bar = ttk.Frame(main)
        top_bar.pack(fill=tk.X, pady=(0, 6))

        self.lang_label = ttk.Label(top_bar, text=self.t["language"])
        self.lang_label.pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(
            top_bar,
            textvariable=self.lang_var,
            values=["Turkce", "English"],
            state="readonly",
            width=10,
        )
        self.lang_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.about_btn = ttk.Button(
            top_bar, text=self.t["about"], command=self.show_about, width=12
        )
        self.about_btn.pack(side=tk.RIGHT)

        # Klasor secimi
        self.folder_frame = ttk.LabelFrame(main, text=self.t["folder_section"], padding=10)
        self.folder_frame.pack(fill=tk.X, pady=5)

        self.folder_label = ttk.Label(self.folder_frame, text=self.t["folder_label"])
        self.folder_label.grid(row=0, column=0, sticky=tk.W)
        self.folder_var = tk.StringVar()
        ttk.Entry(self.folder_frame, textvariable=self.folder_var, width=80).grid(
            row=0, column=1, padx=5, sticky=tk.EW
        )
        self.browse_btn = ttk.Button(
            self.folder_frame, text=self.t["browse"], command=self.browse_folder
        )
        self.browse_btn.grid(row=0, column=2, padx=5)

        self.recursive_var = tk.BooleanVar(value=False)
        self.recursive_cb = ttk.Checkbutton(
            self.folder_frame, text=self.t["recursive"], variable=self.recursive_var
        )
        self.recursive_cb.grid(row=1, column=1, sticky=tk.W, pady=(6, 0))

        self.ext_filter_label = ttk.Label(self.folder_frame, text=self.t["ext_filter"])
        self.ext_filter_label.grid(row=2, column=0, sticky=tk.W, pady=(6, 0))
        self.ext_var = tk.StringVar(value="")
        ttk.Entry(self.folder_frame, textvariable=self.ext_var, width=30).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=(6, 0)
        )
        self.ext_hint_label = ttk.Label(
            self.folder_frame, text=self.t["ext_hint"], foreground="#666"
        )
        self.ext_hint_label.grid(row=2, column=2, sticky=tk.W, pady=(6, 0))

        self.folder_frame.columnconfigure(1, weight=1)

        # Islemler
        self.ops_frame = ttk.LabelFrame(main, text=self.t["ops_section"], padding=10)
        self.ops_frame.pack(fill=tk.X, pady=5)

        # 1) Bul / Degistir
        self.fr_enabled = tk.BooleanVar()
        self.fr_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["find_replace"], variable=self.fr_enabled
        )
        self.fr_cb.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.find_label = ttk.Label(self.ops_frame, text=self.t["find"])
        self.find_label.grid(row=0, column=1, sticky=tk.E)
        self.find_var = tk.StringVar()
        ttk.Entry(self.ops_frame, textvariable=self.find_var, width=18).grid(
            row=0, column=2, padx=5
        )
        self.replace_label = ttk.Label(self.ops_frame, text=self.t["replace"])
        self.replace_label.grid(row=0, column=3, sticky=tk.E)
        self.replace_var = tk.StringVar()
        ttk.Entry(self.ops_frame, textvariable=self.replace_var, width=18).grid(
            row=0, column=4, padx=5
        )
        self.regex_var = tk.BooleanVar()
        self.regex_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["regex"], variable=self.regex_var
        )
        self.regex_cb.grid(row=0, column=5, padx=5)

        # 2) Coklu Bul/Degistir
        self.multi_fr_enabled = tk.BooleanVar()
        self.multi_fr_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["multi_fr"], variable=self.multi_fr_enabled
        )
        self.multi_fr_cb.grid(row=1, column=0, sticky=tk.NW, pady=6)

        multi_frame = ttk.Frame(self.ops_frame)
        multi_frame.grid(row=1, column=1, columnspan=6, sticky=tk.EW, padx=5, pady=6)
        self.ops_frame.columnconfigure(1, weight=1)

        self.multi_hint_label = ttk.Label(
            multi_frame,
            text=self.t["multi_fr_hint"],
            foreground="#666",
            wraplength=800,
            justify=tk.LEFT,
        )
        self.multi_hint_label.pack(anchor=tk.W)

        text_container = ttk.Frame(multi_frame)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

        self.multi_fr_text = tk.Text(
            text_container, height=7, width=70, wrap=tk.NONE,
            font=("Consolas", 10), undo=True,
        )
        sb_y = ttk.Scrollbar(
            text_container, orient=tk.VERTICAL, command=self.multi_fr_text.yview
        )
        sb_x = ttk.Scrollbar(
            text_container, orient=tk.HORIZONTAL, command=self.multi_fr_text.xview
        )
        self.multi_fr_text.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        self.multi_fr_text.grid(row=0, column=0, sticky=tk.NSEW)
        sb_y.grid(row=0, column=1, sticky=tk.NS)
        sb_x.grid(row=1, column=0, sticky=tk.EW)
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)

        self.multi_fr_text.insert("1.0", self.t["multi_example"])

        # 3) Onek
        self.prefix_enabled = tk.BooleanVar()
        self.prefix_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["prefix_add"], variable=self.prefix_enabled
        )
        self.prefix_cb.grid(row=2, column=0, sticky=tk.W, pady=6)
        self.prefix_text_label = ttk.Label(self.ops_frame, text=self.t["text"])
        self.prefix_text_label.grid(row=2, column=1, sticky=tk.E)
        self.prefix_var = tk.StringVar()
        ttk.Entry(self.ops_frame, textvariable=self.prefix_var, width=18).grid(
            row=2, column=2, padx=5, pady=6
        )

        # 4) Sonek
        self.suffix_enabled = tk.BooleanVar()
        self.suffix_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["suffix_add"], variable=self.suffix_enabled
        )
        self.suffix_cb.grid(row=3, column=0, sticky=tk.W, pady=6)
        self.suffix_text_label = ttk.Label(self.ops_frame, text=self.t["text"])
        self.suffix_text_label.grid(row=3, column=1, sticky=tk.E)
        self.suffix_var = tk.StringVar()
        ttk.Entry(self.ops_frame, textvariable=self.suffix_var, width=18).grid(
            row=3, column=2, padx=5, pady=6
        )
        self.suffix_hint_label = ttk.Label(
            self.ops_frame, text=self.t["suffix_hint"], foreground="#666"
        )
        self.suffix_hint_label.grid(row=3, column=3, columnspan=3, sticky=tk.W)

        # 5) Numaralandirma
        self.num_enabled = tk.BooleanVar()
        self.num_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["numbering"], variable=self.num_enabled
        )
        self.num_cb.grid(row=4, column=0, sticky=tk.W, pady=6)
        self.basename_label = ttk.Label(self.ops_frame, text=self.t["base_name"])
        self.basename_label.grid(row=4, column=1, sticky=tk.E)
        self.basename_var = tk.StringVar(value="dosya")
        ttk.Entry(self.ops_frame, textvariable=self.basename_var, width=18).grid(
            row=4, column=2, padx=5, pady=6
        )
        self.start_label = ttk.Label(self.ops_frame, text=self.t["start"])
        self.start_label.grid(row=4, column=3, sticky=tk.E)
        self.start_var = tk.IntVar(value=1)
        ttk.Spinbox(
            self.ops_frame, from_=0, to=999999, textvariable=self.start_var, width=8
        ).grid(row=4, column=4, sticky=tk.W, padx=5)
        self.pad_label = ttk.Label(self.ops_frame, text=self.t["pad"])
        self.pad_label.grid(row=4, column=5, sticky=tk.E)
        self.pad_var = tk.IntVar(value=3)
        ttk.Spinbox(
            self.ops_frame, from_=1, to=10, textvariable=self.pad_var, width=5
        ).grid(row=4, column=6, sticky=tk.W, padx=5)

        # 6) Harf Donusumu
        self.case_enabled = tk.BooleanVar()
        self.case_cb = ttk.Checkbutton(
            self.ops_frame, text=self.t["case_conv"], variable=self.case_enabled
        )
        self.case_cb.grid(row=5, column=0, sticky=tk.W, pady=6)
        self.case_type = tk.StringVar(value="lower")
        case_box = ttk.Frame(self.ops_frame)
        case_box.grid(row=5, column=1, columnspan=6, sticky=tk.W, padx=5)
        self.case_lower_rb = ttk.Radiobutton(
            case_box, text=self.t["case_lower"], variable=self.case_type, value="lower"
        )
        self.case_lower_rb.pack(side=tk.LEFT, padx=5)
        self.case_upper_rb = ttk.Radiobutton(
            case_box, text=self.t["case_upper"], variable=self.case_type, value="upper"
        )
        self.case_upper_rb.pack(side=tk.LEFT, padx=5)
        self.case_title_rb = ttk.Radiobutton(
            case_box, text=self.t["case_title"], variable=self.case_type, value="title"
        )
        self.case_title_rb.pack(side=tk.LEFT, padx=5)

        # Butonlar
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=10)
        self.preview_btn = ttk.Button(
            btn_frame, text=self.t["preview"], command=self.preview, width=14
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        self.apply_btn = ttk.Button(
            btn_frame, text=self.t["apply"], command=self.apply, width=14
        )
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        self.undo_btn = ttk.Button(
            btn_frame, text=self.t["undo"], command=self.undo, width=14
        )
        self.undo_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn = ttk.Button(
            btn_frame, text=self.t["clear"], command=self.clear_all, width=14
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Onizleme tablosu
        self.preview_frame = ttk.LabelFrame(
            main, text=self.t["preview_section"], padding=5
        )
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("old", "new", "status")
        self.tree = ttk.Treeview(
            self.preview_frame, columns=columns, show="headings", height=15
        )
        self.tree.heading("old", text=self.t["col_old"])
        self.tree.heading("new", text=self.t["col_new"])
        self.tree.heading("status", text=self.t["col_status"])
        self.tree.column("old", width=400)
        self.tree.column("new", width=400)
        self.tree.column("status", width=110, anchor=tk.CENTER)

        self.tree.tag_configure("ok", background="#e8f5e9")
        self.tree.tag_configure("same", background="#f5f5f5", foreground="#888")
        self.tree.tag_configure("conflict", background="#ffebee")

        scroll = ttk.Scrollbar(
            self.preview_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Durum cubugu
        self.status_var = tk.StringVar(value=self.t["ready"])
        self.status_label = ttk.Label(
            main, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=4
        )
        self.status_label.pack(fill=tk.X, pady=(5, 0))

    # ---------- Language ----------
    def _on_lang_change(self, _evt=None):
        v = self.lang_var.get()
        new_lang = "en" if v == "English" else "tr"
        if new_lang != self.lang:
            self.lang = new_lang
            self.t = STRINGS[self.lang]
            self._apply_translations()

    def _apply_translations(self):
        t = self.t
        self.root.title(t["title"])
        self.lang_label.configure(text=t["language"])
        self.about_btn.configure(text=t["about"])
        self.folder_frame.configure(text=t["folder_section"])
        self.folder_label.configure(text=t["folder_label"])
        self.browse_btn.configure(text=t["browse"])
        self.recursive_cb.configure(text=t["recursive"])
        self.ext_filter_label.configure(text=t["ext_filter"])
        self.ext_hint_label.configure(text=t["ext_hint"])
        self.ops_frame.configure(text=t["ops_section"])
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
        self.preview_btn.configure(text=t["preview"])
        self.apply_btn.configure(text=t["apply"])
        self.undo_btn.configure(text=t["undo"])
        self.clear_btn.configure(text=t["clear"])
        self.preview_frame.configure(text=t["preview_section"])
        self.tree.heading("old", text=t["col_old"])
        self.tree.heading("new", text=t["col_new"])
        self.tree.heading("status", text=t["col_status"])
        self.status_var.set(t["ready"])

        # Onizleme tablosunda durum metinlerini yenile
        status_map = {
            "ok": t["status_ok"],
            "same": t["status_same"],
            "conflict": t["status_conflict"],
            "exists": t["status_exists"],
        }
        for item_id, (_old, _new, key) in zip(self.tree.get_children(), self.preview_data):
            vals = list(self.tree.item(item_id, "values"))
            vals[2] = status_map.get(key, vals[2])
            self.tree.item(item_id, values=vals)

    # ---------- About ----------
    def show_about(self):
        t = self.t
        win = tk.Toplevel(self.root)
        win.title(t["about_title"])
        win.geometry("480x460")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        # Merkez
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 480) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 460) // 2
        win.geometry(f"+{max(0, x)}+{max(0, y)}")

        container = ttk.Frame(win, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Icon (varsa)
        icon_path = resource_path("icon_256.png")
        if os.path.exists(icon_path):
            try:
                img = tk.PhotoImage(file=icon_path)
                # Kucult
                img = img.subsample(max(1, img.width() // 80), max(1, img.height() // 80))
                self._about_icon = img
                ttk.Label(container, image=img).pack(pady=(0, 8))
            except tk.TclError:
                pass

        ttk.Label(
            container,
            text=t["about_app_name"],
            font=("Segoe UI", 14, "bold"),
        ).pack()
        ttk.Label(container, text=t["about_version"], foreground="#666").pack(pady=(0, 10))

        ttk.Label(
            container,
            text=t["about_desc"],
            wraplength=420,
            justify=tk.CENTER,
        ).pack(pady=(0, 12))

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=4)

        ttk.Label(
            container,
            text=f"{t['about_developer']}: Ayberk Baglan",
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(8, 4))

        # Iletisim linkleri
        ttk.Label(
            container, text=t["about_contact"] + ":", font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.CENTER, pady=(4, 2))

        links_frame = ttk.Frame(container)
        links_frame.pack()

        links = [
            ("GitHub", "https://github.com/ayberkbgln"),
            ("LinkedIn", "https://www.linkedin.com/in/ayberkbaglan/"),
            ("X / Twitter", "https://x.com/yulewiz"),
            ("E-mail", "mailto:ayberkbaglan@gmail.com"),
        ]
        for label, url in links:
            self._make_link(links_frame, label, url).pack(pady=1)

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)

        bottom = ttk.Frame(container)
        bottom.pack(fill=tk.X)
        self._make_link(
            bottom,
            t["about_source"],
            "https://github.com/ayberkbgln/bulk-file-renamer",
        ).pack(side=tk.LEFT)
        ttk.Label(bottom, text=t["about_license"], foreground="#666").pack(side=tk.RIGHT)

        ttk.Button(container, text=t["about_close"], command=win.destroy, width=12).pack(
            pady=(14, 0)
        )

    def _make_link(self, parent, text, url):
        lbl = ttk.Label(parent, text=text, foreground="#1a66d9", cursor="hand2")
        font_kwargs = {"font": ("Segoe UI", 10, "underline")}
        lbl.configure(**font_kwargs)
        lbl.bind("<Button-1>", lambda _e, u=url: webbrowser.open(u))
        return lbl

    # ---------- Logic ----------
    def browse_folder(self):
        folder = filedialog.askdirectory(title=self.t["folder_label"])
        if folder:
            self.folder_var.set(folder)

    def get_files(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror(self.t["err_title"], self.t["err_invalid_folder"])
            return []

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
            for fn in sorted(os.listdir(folder)):
                path = os.path.join(folder, fn)
                if os.path.isfile(path):
                    if exts is None or os.path.splitext(fn)[1].lower() in exts:
                        files.append(path)

        files.sort()
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

        any_op = any(
            [
                self.fr_enabled.get(),
                self.multi_fr_enabled.get(),
                self.prefix_enabled.get(),
                self.suffix_enabled.get(),
                self.num_enabled.get(),
                self.case_enabled.get(),
            ]
        )
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
                    key, tag = "same", "same"
                elif new in seen_new:
                    key, tag = "conflict", "conflict"
                elif os.path.exists(new) and os.path.normcase(new) != os.path.normcase(old):
                    key, tag = "exists", "conflict"
                else:
                    key, tag = "ok", "ok"

                seen_new.add(new)
                self.preview_data.append((old, new, key))
                status_text = {
                    "ok": self.t["status_ok"],
                    "same": self.t["status_same"],
                    "conflict": self.t["status_conflict"],
                    "exists": self.t["status_exists"],
                }[key]
                self.tree.insert(
                    "",
                    tk.END,
                    values=(os.path.basename(old), os.path.basename(new), status_text),
                    tags=(tag,),
                )
        except ValueError as e:
            messagebox.showerror(self.t["err_title"], str(e))
            return

        ok_count = sum(1 for _, _, k in self.preview_data if k == "ok")
        conflict_count = sum(1 for _, _, k in self.preview_data if k in ("conflict", "exists"))
        self.status_var.set(
            self.t["summary"].format(t=len(files), ok=ok_count, c=conflict_count)
        )

    def apply(self):
        if not self.preview_data:
            messagebox.showwarning(self.t["warn_title"], self.t["need_preview"])
            return

        ok_items = [d for d in self.preview_data if d[2] == "ok"]
        if not ok_items:
            messagebox.showinfo(self.t["info_title"], self.t["nothing_to_rename"])
            return

        conflicts = [d for d in self.preview_data if d[2] in ("conflict", "exists")]
        if conflicts:
            if not messagebox.askyesno(
                self.t["warn_title"], self.t["conflict_warn"].format(n=len(conflicts))
            ):
                return

        if not messagebox.askyesno(
            self.t["info_title"], self.t["confirm_apply"].format(n=len(ok_items))
        ):
            return

        temp_map = []
        failed = 0
        for old, new, _ in ok_items:
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

        messagebox.showinfo(
            self.t["done"], self.t["done_msg"].format(s=success, f=failed)
        )
        self.status_var.set(self.t["done_status"].format(s=success, f=failed))
        self.preview()

    def undo(self):
        if not self.last_operations:
            messagebox.showinfo(self.t["info_title"], self.t["undo_none"])
            return
        if not messagebox.askyesno(
            self.t["info_title"], self.t["undo_confirm"].format(n=len(self.last_operations))
        ):
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
        messagebox.showinfo(
            self.t["undone"], self.t["done_msg"].format(s=success, f=failed)
        )
        self.status_var.set(self.t["undo_status"].format(n=success))
        self.preview()

    def clear_all(self):
        for var in (
            self.fr_enabled,
            self.multi_fr_enabled,
            self.prefix_enabled,
            self.suffix_enabled,
            self.num_enabled,
            self.case_enabled,
            self.regex_var,
            self.recursive_var,
        ):
            var.set(False)
        for var in (
            self.find_var,
            self.replace_var,
            self.prefix_var,
            self.suffix_var,
            self.ext_var,
        ):
            var.set("")
        self.basename_var.set("dosya")
        self.start_var.set(1)
        self.pad_var.set(3)
        self.case_type.set("lower")
        self.multi_fr_text.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())
        self.preview_data = []
        self.status_var.set(self.t["cleared"])


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except tk.TclError:
        pass
    RenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
