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
)

ROOT = Path(__file__).resolve().parent


class ResumeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Library Generator")
        self.geometry("900x650")

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
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        # -------------------------
        # Profile Fields
        # -------------------------
        self.vars = {}

        def add_field(row, label, attr):
            ttk.Label(main, text=label).grid(row=row, column=0, sticky="w")
            v = tk.StringVar(value=getattr(self.cfg, attr))
            self.vars[attr] = v
            ttk.Entry(main, textvariable=v, width=65).grid(
                row=row, column=1, columnspan=2, sticky="w"
            )

        add_field(1, "Name", "name")
        add_field(2, "Phone", "phone")
        add_field(3, "Email", "email")
        add_field(4, "LinkedIn", "linkedin")
        add_field(5, "GitHub", "github")
        add_field(6, "Location", "location")

        # LibreOffice
        ttk.Label(main, text="LibreOffice (soffice.exe)").grid(row=7, column=0, sticky="w")
        self.vars["libreoffice_path"] = tk.StringVar(value=self.cfg.libreoffice_path)
        ttk.Entry(main, textvariable=self.vars["libreoffice_path"], width=65).grid(
            row=7, column=1, sticky="w"
        )
        ttk.Button(main, text="Browse", command=self._browse_soffice).grid(
            row=7, column=2, sticky="w"
        )

        # -------------------------
        # Variant Selection
        # -------------------------
        ttk.Label(main, text="Resume Variants").grid(row=8, column=0, sticky="w", pady=(18, 0))

        self.variant_vars = {
            "general": tk.BooleanVar(value=True),
            "python-backend": tk.BooleanVar(value=True),
            "cybersecurity": tk.BooleanVar(value=True),
            "ai-architect": tk.BooleanVar(value=True),
            "grc-analyst": tk.BooleanVar(value=True),
        }

        row = 9
        for key in self.variant_vars:
            ttk.Checkbutton(
                main,
                text=key.replace("-", " ").title(),
                variable=self.variant_vars[key],
            ).grid(row=row, column=1, sticky="w")
            row += 1

        # ODT / PDF
        self.make_odt = tk.BooleanVar(value=True)
        self.make_pdf = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            main,
            text="Generate ODT (LibreOffice required)",
            variable=self.make_odt,
        ).grid(row=row, column=1, sticky="w", pady=(10, 0))
        row += 1

        ttk.Checkbutton(
            main,
            text="Generate PDF (LibreOffice required)",
            variable=self.make_pdf,
        ).grid(row=row, column=1, sticky="w")
        row += 1

        # -------------------------
        # Buttons
        # -------------------------
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=(20, 0), sticky="w")

        ttk.Button(btn_frame, text="Save Settings", command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate", command=self._generate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Open Output", command=self._open_output).pack(side="left", padx=5)

        # -------------------------
        # Log Area
        # -------------------------
        ttk.Label(main, text="Log").grid(row=row + 1, column=0, sticky="w", pady=(20, 0))

        self.log = tk.Text(main, height=15)
        self.log.grid(row=row + 2, column=0, columnspan=3, sticky="nsew")

        main.columnconfigure(1, weight=1)
        main.rowconfigure(row + 2, weight=1)

        self._log("Ready.")

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
        self.cfg = ResumeConfig(
            name=self.vars["name"].get(),
            phone=self.vars["phone"].get(),
            email=self.vars["email"].get(),
            linkedin=self.vars["linkedin"].get(),
            github=self.vars["github"].get(),
            location=self.vars["location"].get(),
            libreoffice_path=self.vars["libreoffice_path"].get(),
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

        for variant, var in self.variant_vars.items():
            if var.get():
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
                    messagebox.showerror("Error", str(e))
                    return

        self._log("All selected resumes generated.")

    def _open_output(self):
        output_dir = ROOT / "resumes"
        output_dir.mkdir(exist_ok=True)
        import os
        os.startfile(str(output_dir))

    def _log(self, message):
        self.log.insert("end", message + "\n")
        self.log.see("end")


if __name__ == "__main__":
    app = ResumeUI()
    app.mainloop()