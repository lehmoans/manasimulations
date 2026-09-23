import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import yaml

from .config.configuration import CaseConfigurationManager


class CaseConfigurationGUI:
    """Small desktop editor for AutoFluent case YAML configurations."""

    def __init__(self, manager=None):
        self.manager = manager or CaseConfigurationManager()
        self.root = tk.Tk()
        self.root.title("AutoFluent Case Configuration")
        self.root.geometry("900x650")

        self.text = None
        self.saved_cases = None
        self.status = tk.StringVar(value="Ready")
        self._build()

    def _build(self):
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="New", command=self.new_case).pack(
            side="left", padx=3
        )
        ttk.Button(toolbar, text="Load Current", command=self.load_current).pack(
            side="left", padx=3
        )
        ttk.Button(toolbar, text="Load Saved", command=self.load_saved).pack(
            side="left", padx=3
        )
        ttk.Button(toolbar, text="Save", command=self.save_current).pack(
            side="left", padx=3
        )
        ttk.Button(toolbar, text="Save As...", command=self.save_as).pack(
            side="left", padx=3
        )

        ttk.Label(toolbar, text="Saved cases:").pack(side="left", padx=(18, 4))
        self.saved_cases = ttk.Combobox(toolbar, state="readonly", width=28)
        self.saved_cases.pack(side="left", padx=3)

        frame = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        frame.pack(fill="both", expand=True)

        self.text = tk.Text(frame, wrap="none", undo=True)
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w",
            padding=5,
        ).pack(fill="x")

        self.refresh_saved_cases()
        self.new_case()

    def refresh_saved_cases(self):
        cases = self.manager.list_saved()
        self.saved_cases["values"] = cases
        if cases:
            self.saved_cases.set(cases[0])
        else:
            self.saved_cases.set("")

    def set_data(self, data):
        self.text.delete("1.0", "end")
        self.text.insert(
            "1.0",
            yaml.safe_dump(
                data,
                sort_keys=False,
                default_flow_style=False,
                allow_unicode=True,
            ),
        )

    def get_data(self):
        raw = self.text.get("1.0", "end")
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            raise ValueError("The case configuration must contain a YAML mapping.")
        return data

    def new_case(self):
        self.set_data(
            {
                "save_dir": {"path": None},
                "geometry": {"file": None},
                "meshing": {"enabled": True},
                "solver": {"enabled": True},
                "post_process": {"enabled": True},
            }
        )
        self.status.set("New case configuration")

    def load_current(self):
        try:
            self.set_data(self.manager.load_current())
            self.status.set(f"Loaded {self.manager.case_path}")
        except Exception as exc:
            messagebox.showerror("Load error", str(exc))

    def load_saved(self):
        name = self.saved_cases.get().strip()
        if not name:
            messagebox.showinfo(
                "Saved cases",
                "There are no saved case configurations.",
            )
            return

        try:
            self.set_data(self.manager.load_saved(name))
            self.status.set(f"Loaded saved case: {name}")
        except Exception as exc:
            messagebox.showerror("Load error", str(exc))

    def save_current(self):
        try:
            data = self.get_data()
            path = self.manager.save_current(data)
            self.status.set(f"Saved current case: {path}")
        except Exception as exc:
            messagebox.showerror("Save error", str(exc))

    def save_as(self):
        try:
            data = self.get_data()
        except Exception as exc:
            messagebox.showerror("Configuration error", str(exc))
            return

        name = simpledialog.askstring(
            "Save case configuration",
            "Name for the saved case:",
            parent=self.root,
        )
        if not name:
            return

        try:
            path = self.manager.save_as(data, name, overwrite=False)
        except FileExistsError:
            overwrite = messagebox.askyesno(
                "Already exists",
                f"{name} already exists. Overwrite it?",
            )
            if not overwrite:
                return
            path = self.manager.save_as(data, name, overwrite=True)
        except Exception as exc:
            messagebox.showerror("Save error", str(exc))
            return

        self.refresh_saved_cases()
        self.saved_cases.set(path.stem)
        self.status.set(f"Saved configuration: {path}")

    def run(self):
        self.root.mainloop()


def launch_gui():
    CaseConfigurationGUI().run()
