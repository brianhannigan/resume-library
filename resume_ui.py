from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from generate_resumes import (
    ResumeConfig,
    load_config,
    save_config,
    build_variant,
    find_soffice,
    safe_slug,  # uses your generator’s sanitizer
)

ROOT = Path(__file__).resolve().parent


class ResumeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Library Generator")
        self.geometry("980x740")

        self.cfg = load_config()
        self._build_ui()

    # -------------------------
    # UI Layout
    # -------------------------
    def _build_ui(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(
            main,
            text="Resume Generator (DOCX + TXT + ODT + PDF)",
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        # -------------------------
        # Profile Fields
        # -------------------------
        self.vars = {}

        def add_field(row, label, attr):
            ttk.Label(main, text=label).grid(row=row, column=0, sticky="w")
            v = tk.StringVar(value=getattr(self.cfg, attr, ""))
            self.vars[attr] = v
            ttk.Entry(main, textvariable=v, width=70).grid(row=row, column=1, columnspan=3, sticky="w")

        add_field(1, "Name", "name")
        add_field(2, "Phone", "phone")
        add_field(3, "Email", "email")
        add_field(4, "LinkedIn", "linkedin")
        add_field(5, "GitHub", "github")
        add_field(6, "Location", "location")

        # LibreOffice
        ttk.Label(main, text="LibreOffice (soffice.exe)").grid(row=7, column=0, sticky="w")
        self.vars["libreoffice_path"] = tk.StringVar(value=getattr(self.cfg, "libreoffice_path", ""))
        ttk.Entry(main, textvariable=self.vars["libreoffice_path"], width=70).grid(row=7, column=1, sticky="w")
        ttk.Button(main, text="Browse", command=self._browse_soffice).grid(row=7, column=2, sticky="w")

        # -------------------------
        # Formats Manager
        # -------------------------
        ttk.Label(main, text="Formats (used for folder routing + dropdown)").grid(row=8, column=0, sticky="w", pady=(12, 0))

        self.formats_list = tk.Listbox(main, height=5, exportselection=False)
        self.formats_list.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=(4, 0))
        self._load_formats_into_listbox()

        fmt_controls = ttk.Frame(main)
        fmt_controls.grid(row=9, column=2, columnspan=2, sticky="nw", padx=(10, 0))
        self.new_format = tk.StringVar()
        ttk.Entry(fmt_controls, textvariable=self.new_format, width=22).grid(row=0, column=0, sticky="w")
        ttk.Button(fmt_controls, text="Add Format", command=self._add_format).grid(row=0, column=1, padx=6)
        ttk.Button(fmt_controls, text="Remove Selected", command=self._remove_format).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Resume Format Dropdown
        ttk.Label(main, text="Resume Format").grid(row=10, column=0, sticky="w", pady=(10, 0))
        self.format_var = tk.StringVar(value=getattr(self.cfg, "resume_format", "classic"))
        self.format_combo = ttk.Combobox(main, textvariable=self.format_var, values=self._get_formats(), state="readonly", width=18)
        self.format_combo.grid(row=10, column=1, sticky="w", pady=(10, 0))

        # -------------------------
        # Variants Manager
        # -------------------------
        ttk.Label(main, text="Variants (checkbox list + output folders)").grid(row=11, column=0, sticky="w", pady=(14, 0))

        self.variants_list = tk.Listbox(main, height=6, exportselection=False)
        self.variants_list.grid(row=12, column=0, columnspan=2, sticky="nsew", pady=(4, 0))
        self._load_variants_into_listbox()

        var_controls = ttk.Frame(main)
        var_controls.grid(row=12, column=2, columnspan=2, sticky="nw", padx=(10, 0))
        self.new_variant = tk.StringVar()
        ttk.Entry(var_controls, textvariable=self.new_variant, width=22).grid(row=0, column=0, sticky="w")
        ttk.Button(var_controls, text="Add Variant", command=self._add_variant).grid(row=0, column=1, padx=6)
        ttk.Button(var_controls, text="Remove Selected", command=self._remove_variant).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Dynamic variant checkboxes (driven by variants list)
        ttk.Label(main, text="Select Variants to Generate").grid(row=13, column=0, sticky="w", pady=(14, 0))
        self.variant_check_frame = ttk.Frame(main)
        self.variant_check_frame.grid(row=14, column=0, columnspan=4, sticky="w")
        self.variant_vars = {}
        self._rebuild_variant_checkboxes()

        # ODT / PDF
        self.make_odt = tk.BooleanVar(value=True)
        self.make_pdf = tk.BooleanVar(value=True)

        ttk.Checkbutton(main, text="Generate ODT (LibreOffice required)", variable=self.make_odt).grid(row=15, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Checkbutton(main, text="Generate PDF (LibreOffice required)", variable=self.make_pdf).grid(row=16, column=0, columnspan=2, sticky="w")

        # Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=17, column=0, columnspan=4, pady=(18, 0), sticky="w")

        ttk.Button(btn_frame, text="Save Settings", command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate", command=self._generate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Open Output", command=self._open_output).pack(side="left", padx=5)

        # Log
        ttk.Label(main, text="Log").grid(row=18, column=0, sticky="w", pady=(18, 0))
        self.log = tk.Text(main, height=12)
        self.log.grid(row=19, column=0, columnspan=4, sticky="nsew")

        main.columnconfigure(1, weight=1)
        main.columnconfigure(0, weight=0)
        main.rowconfigure(19, weight=1)

        self._log("Ready.")

    # -------------------------
    # Helpers
    # -------------------------
    def _get_formats(self):
        formats = getattr(self.cfg, "formats", None) or ["classic", "madakor"]
        # show pretty (but still safe)
        return [safe_slug(f) for f in formats]

    def _get_variants(self):
        variants = getattr(self.cfg, "variants", None) or ["general", "python-backend", "cybersecurity", "ai-architect", "grc-analyst"]
        return [safe_slug(v, default="general") for v in variants]

    def _load_formats_into_listbox(self):
        self.formats_list.delete(0, "end")
        for f in self._get_formats():
            self.formats_list.insert("end", f)

    def _load_variants_into_listbox(self):
        self.variants_list.delete(0, "end")
        for v in self._get_variants():
            self.variants_list.insert("end", v)

    def _rebuild_variant_checkboxes(self):
        for child in self.variant_check_frame.winfo_children():
            child.destroy()

        self.variant_vars = {}
        variants = self._get_variants()

        # 3 columns of checkboxes
        cols = 3
        for idx, key in enumerate(variants):
            self.variant_vars[key] = tk.BooleanVar(value=True)
            r = idx // cols
            c = idx % cols
            ttk.Checkbutton(
                self.variant_check_frame,
                text=key.replace("-", " ").title(),
                variable=self.variant_vars[key],
            ).grid(row=r, column=c, sticky="w", padx=10, pady=2)

    # -------------------------
    # Format / Variant Manager Actions
    # -------------------------
    def _add_format(self):
        val = safe_slug(self.new_format.get())
        if not val:
            return
        formats = self._get_formats()
        if val not in formats:
            formats.append(val)
        self.cfg.formats = formats
        # keep current selected format valid
        if safe_slug(self.format_var.get()) not in formats:
            self.format_var.set(formats[0])
        self._load_formats_into_listbox()
        self.format_combo["values"] = formats
        self.new_format.set("")
        self._log(f"Added format: {val}")

    def _remove_format(self):
        sel = self.formats_list.curselection()
        if not sel:
            return
        idx = sel[0]
        formats = self._get_formats()
        removed = formats[idx]
        # prevent removing last format
        if len(formats) <= 1:
            messagebox.showwarning("Cannot remove", "You must keep at least one format.")
            return
        formats.pop(idx)
        self.cfg.formats = formats
        if safe_slug(self.format_var.get()) == removed:
            self.format_var.set(formats[0])
        self._load_formats_into_listbox()
        self.format_combo["values"] = formats
        self._log(f"Removed format: {removed}")

    def _add_variant(self):
        val = safe_slug(self.new_variant.get(), default="general")
        if not val:
            return
        variants = self._get_variants()
        if val not in variants:
            variants.append(val)
        self.cfg.variants = variants
        self._load_variants_into_listbox()
        self._rebuild_variant_checkboxes()
        self.new_variant.set("")
        self._log(f"Added variant: {val}")

    def _remove_variant(self):
        sel = self.variants_list.curselection()
        if not sel:
            return
        idx = sel[0]
        variants = self._get_variants()
        removed = variants[idx]
        if len(variants) <= 1:
            messagebox.showwarning("Cannot remove", "You must keep at least one variant.")
            return
        variants.pop(idx)
        self.cfg.variants = variants
        self._load_variants_into_listbox()
        self._rebuild_variant_checkboxes()
        self._log(f"Removed variant: {removed}")

    # -------------------------
    # Actions
    # -------------------------
    def _browse_soffice(self):
        path = filedialog.askopenfilename(
            title="Select soffice.exe",
            filetypes=[("LibreOffice", "soffice.exe"), ("All files", "*.*")]
        )
        if path:
            self.vars["libreoffice_path"].set(path)

    def _save(self):
        # persist formats/variants + all fields
        self.cfg = ResumeConfig(
            name=self.vars["name"].get(),
            phone=self.vars["phone"].get(),
            email=self.vars["email"].get(),
            linkedin=self.vars["linkedin"].get(),
            github=self.vars["github"].get(),
            location=self.vars["location"].get(),
            libreoffice_path=self.vars["libreoffice_path"].get(),
            resume_format=self.format_var.get(),
            formats=self._get_formats(),
            variants=self._get_variants(),
        )
        save_config(self.cfg)
        self._log("Settings saved.")

    def _generate(self):
        self._save()

        if (self.make_odt.get() or self.make_pdf.get()):
            if not find_soffice(self.cfg):
                messagebox.showerror(
                    "LibreOffice Missing",
                    "Could not find soffice.exe. Install LibreOffice or set path."
                )
                return

        selected_variants = [v for v, var in self.variant_vars.items() if var.get()]
        if not selected_variants:
            messagebox.showinfo("Nothing selected", "Select at least one variant to generate.")
            return

        # Set chosen format
        self.cfg.resume_format = self.format_var.get()

        for variant in selected_variants:
            try:
                files = build_variant(
                    variant,
                    self.cfg,
                    also_odt=self.make_odt.get(),
                    also_pdf=self.make_pdf.get(),
                )
                for k, v in files.items():
                    self._log(f"{variant} -> {k}: {v}")
            except Exception as e:
                self._log(f"ERROR ({variant}): {e}")
                messagebox.showerror("Error", f"{variant}: {e}")
                return

        self._log("All selected resumes generated.")

    def _open_output(self):
        output_dir = ROOT / "resumes"
        output_dir.mkdir(exist_ok=True)
        import os
        os.startfile(str(output_dir))

    def _log(self, message: str):
        self.log.insert("end", message + "\n")
        self.log.see("end")


if __name__ == "__main__":
    app = ResumeUI()
    app.mainloop()