"""
Toplu Dosya Yeniden Adlandirici
GUI ile coklu islem destegi: bul/degistir, onek/sonek, numaralandirma, harf donusumu.
"""

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class RenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toplu Dosya Yeniden Adlandirici")
        self.root.geometry("980x900")
        self.root.minsize(900, 750)

        self.last_operations = []   # geri al icin: [(new_path, old_path), ...]
        self.preview_data = []      # [(old_path, new_path, status), ...]

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Klasor secimi
        folder_frame = ttk.LabelFrame(main, text="Klasor Secimi", padding=10)
        folder_frame.pack(fill=tk.X, pady=5)

        ttk.Label(folder_frame, text="Klasor:").grid(row=0, column=0, sticky=tk.W)
        self.folder_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.folder_var, width=80).grid(
            row=0, column=1, padx=5, sticky=tk.EW
        )
        ttk.Button(folder_frame, text="Gozat...", command=self.browse_folder).grid(
            row=0, column=2, padx=5
        )

        self.recursive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            folder_frame,
            text="Alt klasorleri de dahil et",
            variable=self.recursive_var,
        ).grid(row=1, column=1, sticky=tk.W, pady=(6, 0))

        ttk.Label(folder_frame, text="Uzanti filtresi:").grid(row=2, column=0, sticky=tk.W, pady=(6, 0))
        self.ext_var = tk.StringVar(value="")
        ttk.Entry(folder_frame, textvariable=self.ext_var, width=30).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=(6, 0)
        )
        ttk.Label(
            folder_frame,
            text="(orn: .jpg,.png — bos birakilirsa tum dosyalar)",
            foreground="#666",
        ).grid(row=2, column=2, sticky=tk.W, pady=(6, 0))

        folder_frame.columnconfigure(1, weight=1)

        # Islemler
        ops_frame = ttk.LabelFrame(
            main,
            text="Islemler (istediginiz kadarini ayni anda kullanabilirsiniz)",
            padding=10,
        )
        ops_frame.pack(fill=tk.X, pady=5)

        # 1) Bul / Degistir
        self.fr_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Bul ve Degistir", variable=self.fr_enabled
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(ops_frame, text="Bul:").grid(row=0, column=1, sticky=tk.E)
        self.find_var = tk.StringVar()
        ttk.Entry(ops_frame, textvariable=self.find_var, width=18).grid(
            row=0, column=2, padx=5
        )
        ttk.Label(ops_frame, text="Degistir:").grid(row=0, column=3, sticky=tk.E)
        self.replace_var = tk.StringVar()
        ttk.Entry(ops_frame, textvariable=self.replace_var, width=18).grid(
            row=0, column=4, padx=5
        )
        self.regex_var = tk.BooleanVar()
        ttk.Checkbutton(ops_frame, text="Regex", variable=self.regex_var).grid(
            row=0, column=5, padx=5
        )

        # 2) Coklu Bul/Degistir (Liste)
        self.multi_fr_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Coklu Bul/Degistir", variable=self.multi_fr_enabled
        ).grid(row=1, column=0, sticky=tk.NW, pady=6)

        multi_frame = ttk.Frame(ops_frame)
        multi_frame.grid(row=1, column=1, columnspan=6, sticky=tk.EW, padx=5, pady=6)
        ops_frame.columnconfigure(1, weight=1)

        ttk.Label(
            multi_frame,
            text=(
                "Her satira bir cift:  BUL  DEGISTIR  (TAB veya bosluk ile ayirin). "
                "Tek kelime yazarsaniz o metin silinir. '#' ile baslayan satirlar atlanir."
            ),
            foreground="#666",
            wraplength=780,
            justify=tk.LEFT,
        ).pack(anchor=tk.W)

        text_container = ttk.Frame(multi_frame)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

        self.multi_fr_text = tk.Text(
            text_container, height=7, width=70, wrap=tk.NONE, font=("Consolas", 10),
            undo=True,
        )
        sb_y = ttk.Scrollbar(
            text_container, orient=tk.VERTICAL, command=self.multi_fr_text.yview
        )
        sb_x = ttk.Scrollbar(
            text_container, orient=tk.HORIZONTAL, command=self.multi_fr_text.xview
        )
        self.multi_fr_text.configure(
            yscrollcommand=sb_y.set, xscrollcommand=sb_x.set
        )
        self.multi_fr_text.grid(row=0, column=0, sticky=tk.NSEW)
        sb_y.grid(row=0, column=1, sticky=tk.NS)
        sb_x.grid(row=1, column=0, sticky=tk.EW)
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)

        # Ornek metin (placeholder)
        self.multi_fr_text.insert(
            "1.0",
            "# Ornek:\n# eskiKelime yeniKelime\n# IMG_ foto_\n",
        )

        # 3) Onek
        self.prefix_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Onek Ekle", variable=self.prefix_enabled
        ).grid(row=2, column=0, sticky=tk.W, pady=6)
        ttk.Label(ops_frame, text="Metin:").grid(row=2, column=1, sticky=tk.E)
        self.prefix_var = tk.StringVar()
        ttk.Entry(ops_frame, textvariable=self.prefix_var, width=18).grid(
            row=2, column=2, padx=5, pady=6
        )

        # 4) Sonek
        self.suffix_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Sonek Ekle", variable=self.suffix_enabled
        ).grid(row=3, column=0, sticky=tk.W, pady=6)
        ttk.Label(ops_frame, text="Metin:").grid(row=3, column=1, sticky=tk.E)
        self.suffix_var = tk.StringVar()
        ttk.Entry(ops_frame, textvariable=self.suffix_var, width=18).grid(
            row=3, column=2, padx=5, pady=6
        )
        ttk.Label(ops_frame, text="(uzantidan once eklenir)", foreground="#666").grid(
            row=3, column=3, columnspan=3, sticky=tk.W
        )

        # 5) Numaralandirma
        self.num_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Numaralandir", variable=self.num_enabled
        ).grid(row=4, column=0, sticky=tk.W, pady=6)
        ttk.Label(ops_frame, text="Taban ad:").grid(row=4, column=1, sticky=tk.E)
        self.basename_var = tk.StringVar(value="dosya")
        ttk.Entry(ops_frame, textvariable=self.basename_var, width=18).grid(
            row=4, column=2, padx=5, pady=6
        )
        ttk.Label(ops_frame, text="Baslangic:").grid(row=4, column=3, sticky=tk.E)
        self.start_var = tk.IntVar(value=1)
        ttk.Spinbox(
            ops_frame, from_=0, to=999999, textvariable=self.start_var, width=8
        ).grid(row=4, column=4, sticky=tk.W, padx=5)
        ttk.Label(ops_frame, text="Basamak:").grid(row=4, column=5, sticky=tk.E)
        self.pad_var = tk.IntVar(value=3)
        ttk.Spinbox(
            ops_frame, from_=1, to=10, textvariable=self.pad_var, width=5
        ).grid(row=4, column=6, sticky=tk.W, padx=5)

        # 6) Harf Donusumu
        self.case_enabled = tk.BooleanVar()
        ttk.Checkbutton(
            ops_frame, text="Harf Donusumu", variable=self.case_enabled
        ).grid(row=5, column=0, sticky=tk.W, pady=6)
        self.case_type = tk.StringVar(value="lower")
        case_box = ttk.Frame(ops_frame)
        case_box.grid(row=5, column=1, columnspan=6, sticky=tk.W, padx=5)
        ttk.Radiobutton(case_box, text="kucuk", variable=self.case_type, value="lower").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(case_box, text="BUYUK", variable=self.case_type, value="upper").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(case_box, text="Ilk Harfler", variable=self.case_type, value="title").pack(side=tk.LEFT, padx=5)

        # Butonlar
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Onizleme", command=self.preview, width=14).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Uygula", command=self.apply, width=14).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Geri Al", command=self.undo, width=14).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Temizle", command=self.clear_all, width=14).pack(
            side=tk.LEFT, padx=5
        )

        # Onizleme tablosu
        preview_frame = ttk.LabelFrame(main, text="Onizleme", padding=5)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("old", "new", "status")
        self.tree = ttk.Treeview(
            preview_frame, columns=columns, show="headings", height=15
        )
        self.tree.heading("old", text="Eski Ad")
        self.tree.heading("new", text="Yeni Ad")
        self.tree.heading("status", text="Durum")
        self.tree.column("old", width=380)
        self.tree.column("new", width=380)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        # Durum renkleri
        self.tree.tag_configure("ok", background="#e8f5e9")
        self.tree.tag_configure("same", background="#f5f5f5", foreground="#888")
        self.tree.tag_configure("conflict", background="#ffebee")

        scroll = ttk.Scrollbar(
            preview_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Durum cubugu
        self.status_var = tk.StringVar(value="Hazir. Klasor secip 'Onizleme'ye basin.")
        ttk.Label(
            main, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=4
        ).pack(fill=tk.X, pady=(5, 0))

    # ---------- Logic ----------
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Klasor secin")
        if folder:
            self.folder_var.set(folder)

    def get_files(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Hata", "Lutfen gecerli bir klasor secin.")
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
        """Coklu bul/degistir metin kutusundan kurallari ayikla.
        Her satir: 'bul<TAB>degistir' ya da 'bul<bosluk(lar)>degistir'.
        Tek kelimeli satir: o kelime silinir (replace="").
        Bos satirlar ve '#' ile baslayanlar atlanir.
        """
        raw = self.multi_fr_text.get("1.0", tk.END)
        rules = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # TAB varsa oncelikli ayraç
            if "\t" in line:
                parts = line.split("\t", 1)
                find = parts[0].strip()
                replace = parts[1].strip() if len(parts) > 1 else ""
            else:
                # Ilk boşluk grubuna göre ayir
                m = re.match(r"^(\S+)\s+(.*)$", line)
                if m:
                    find = m.group(1)
                    replace = m.group(2).rstrip()
                else:
                    # Tek kelime: sil
                    find = stripped
                    replace = ""
            if find:
                rules.append((find, replace))
        return rules

    def _compute_new_name(self, old_path, index):
        folder = os.path.dirname(old_path)
        fn = os.path.basename(old_path)
        stem, ext = os.path.splitext(fn)

        # 1) Bul/Degistir
        if self.fr_enabled.get():
            find = self.find_var.get()
            replace = self.replace_var.get()
            if find:
                if self.regex_var.get():
                    try:
                        stem = re.sub(find, replace, stem)
                    except re.error as e:
                        raise ValueError(f"Regex hatasi: {e}")
                else:
                    stem = stem.replace(find, replace)

        # 1b) Coklu Bul/Degistir (liste)
        if self.multi_fr_enabled.get():
            for find, replace in self._parse_multi_rules():
                stem = stem.replace(find, replace)

        # 2) Numaralandirma (aktifse stem'i tamamen yeniden kurar)
        if self.num_enabled.get():
            base = self.basename_var.get()
            try:
                start = int(self.start_var.get())
                pad = int(self.pad_var.get())
            except (tk.TclError, ValueError):
                start, pad = 1, 3
            num = str(start + index).zfill(max(1, pad))
            stem = f"{base}{num}" if base else num

        # 3) Onek
        if self.prefix_enabled.get():
            stem = self.prefix_var.get() + stem

        # 4) Sonek
        if self.suffix_enabled.get():
            stem = stem + self.suffix_var.get()

        # 5) Harf donusumu
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
            messagebox.showwarning("Uyari", "En az bir islem secmelisiniz.")
            return

        files = self.get_files()
        if not files:
            self.status_var.set("Dosya bulunamadi.")
            return

        try:
            seen_new = set()
            for i, old in enumerate(files):
                new = self._compute_new_name(old, i)
                if old == new:
                    status, tag = "Degismez", "same"
                elif new in seen_new:
                    status, tag = "Cakisma!", "conflict"
                elif os.path.exists(new) and os.path.normcase(new) != os.path.normcase(old):
                    status, tag = "Mevcut!", "conflict"
                else:
                    status, tag = "OK", "ok"

                seen_new.add(new)
                self.preview_data.append((old, new, status))
                self.tree.insert(
                    "",
                    tk.END,
                    values=(os.path.basename(old), os.path.basename(new), status),
                    tags=(tag,),
                )
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return

        ok_count = sum(1 for _, _, s in self.preview_data if s == "OK")
        conflict_count = sum(
            1 for _, _, s in self.preview_data if s in ("Cakisma!", "Mevcut!")
        )
        self.status_var.set(
            f"Toplam: {len(files)} dosya   |   Degisecek: {ok_count}   |   Sorunlu: {conflict_count}"
        )

    def apply(self):
        if not self.preview_data:
            messagebox.showwarning("Uyari", "Once 'Onizleme' yapin.")
            return

        ok_items = [d for d in self.preview_data if d[2] == "OK"]
        if not ok_items:
            messagebox.showinfo("Bilgi", "Yeniden adlandirilacak dosya yok.")
            return

        conflicts = [d for d in self.preview_data if d[2] in ("Cakisma!", "Mevcut!")]
        if conflicts:
            if not messagebox.askyesno(
                "Cakisma Var",
                f"{len(conflicts)} dosyada cakisma/mevcut var. Bunlar atlanacak. Devam?",
            ):
                return

        if not messagebox.askyesno(
            "Onay", f"{len(ok_items)} dosya yeniden adlandirilacak. Onayliyor musunuz?"
        ):
            return

        # Iki asamali: once gecici ada, sonra hedef ada (ayni klasorde takas sorunlarina karsi)
        temp_map = []
        failed = 0
        for old, new, _ in ok_items:
            tmp = old + ".___rntmp___"
            try:
                os.rename(old, tmp)
                temp_map.append((tmp, new, old))
            except OSError as e:
                failed += 1
                print(f"Gecici adlandirma hatasi: {old}: {e}")

        success = 0
        self.last_operations = []
        for tmp, new, orig in temp_map:
            try:
                os.makedirs(os.path.dirname(new), exist_ok=True)
                os.rename(tmp, new)
                self.last_operations.append((new, orig))
                success += 1
            except OSError as e:
                # geri yuklemeye calis
                try:
                    os.rename(tmp, orig)
                except OSError:
                    pass
                failed += 1
                print(f"Adlandirma hatasi: {tmp} -> {new}: {e}")

        messagebox.showinfo(
            "Tamamlandi", f"Basarili: {success}\nBasarisiz: {failed}"
        )
        self.status_var.set(
            f"Tamamlandi. Basarili: {success}, Basarisiz: {failed}. 'Geri Al' ile eski haline donebilirsiniz."
        )
        self.preview()

    def undo(self):
        if not self.last_operations:
            messagebox.showinfo("Geri Al", "Geri alinacak islem yok.")
            return
        if not messagebox.askyesno(
            "Geri Al",
            f"{len(self.last_operations)} dosya eski adina dondurulecek. Emin misiniz?",
        ):
            return

        success = 0
        failed = 0
        for new, old in reversed(self.last_operations):
            try:
                os.rename(new, old)
                success += 1
            except OSError as e:
                failed += 1
                print(f"Geri alma hatasi: {new} -> {old}: {e}")

        self.last_operations = []
        messagebox.showinfo("Geri Alindi", f"Basarili: {success}\nBasarisiz: {failed}")
        self.status_var.set(f"Geri alindi. {success} dosya.")
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
        self.status_var.set("Temizlendi.")


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
