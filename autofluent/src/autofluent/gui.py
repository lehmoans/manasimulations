import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import yaml

from .config.configuration import CaseConfigurationManager


class CaseConfigurationGUI:
    """Recursive graphical editor for AutoFluent case configurations.

    Mapping nodes are configuration sections. Opening a section enables it and
    reveals its children. Collapsing a section disables it and serializes the
    whole section as null. Leaf nodes are the actual configuration variables.
    """

    def __init__(self, manager=None):
        self.manager = manager or CaseConfigurationManager()
        self.root = tk.Tk()
        self.root.title("AutoFluent Case Configuration")
        self.root.geometry("1050x760")

        self.saved_cases = None
        self.status = tk.StringVar(value="Ready")
        self._nodes = []
        self._data = {}
        self._build()

    def _build(self):
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(fill="x")

        for label, command in (
            ("New", self.new_case),
            ("Load Current", self.load_current),
            ("Load Saved", self.load_saved),
            ("Save", self.save_current),
            ("Save As...", self.save_as),
        ):
            ttk.Button(toolbar, text=label, command=command).pack(
                side="left", padx=3
            )

        ttk.Label(toolbar, text="Saved cases:").pack(side="left", padx=(18, 4))
        self.saved_cases = ttk.Combobox(toolbar, state="readonly", width=28)
        self.saved_cases.pack(side="left", padx=3)

        outer = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        self.form = ttk.Frame(self.canvas, padding=8)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.form, anchor="nw"
        )
        self.form.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_form)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w",
            padding=5,
        ).pack(fill="x")

        self.refresh_saved_cases()
        self.new_case()

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_form(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    @staticmethod
    def _blank_value(value):
        """Return a schema-shaped value with all leaves unset."""
        if isinstance(value, dict):
            return {key: CaseConfigurationGUI._blank_value(child)
                    for key, child in value.items()}
        if isinstance(value, list):
            return []
        return None

    def _schema_from_current(self):
        """Use case.yaml as the GUI schema while clearing its values."""
        data = self.manager.load_current()
        if not isinstance(data, dict) or not data:
            raise ValueError(
                "config/case.yaml must contain a non-empty YAML mapping "
                "before the GUI can build its configuration tree."
            )
        return self._blank_value(data)

    def _clear_form(self):
        for child in self.form.winfo_children():
            child.destroy()
        self._nodes = []

    def _make_node(self, parent, key, value, depth=0):
        if isinstance(value, dict):
            return self._make_section(parent, key, value, depth)

        return self._make_leaf(parent, key, value, depth)

    def _make_section(self, parent, key, value, depth):
        state = tk.BooleanVar(value=value is not None)
        expanded = state.get()

        row = ttk.Frame(parent)
        row.pack(fill="x", pady=(4, 0))

        arrow = ttk.Button(row, width=3)
        arrow.pack(side="left", padx=(depth * 22, 4))

        check = ttk.Checkbutton(
            row,
            text=str(key),
            variable=state,
            command=lambda: self._toggle_section(
                node, state, arrow, children_frame
            ),
        )
        check.pack(side="left")

        children_frame = ttk.Frame(parent)

        node = {
            "kind": "section",
            "key": key,
            "state": state,
            "value": value if isinstance(value, dict) else {},
            "children": [],
            "frame": children_frame,
        }
        self._nodes.append(node)

        def toggle():
            self._toggle_section(node, state, arrow, children_frame)

        arrow.configure(command=toggle)

        for child_key, child_value in node["value"].items():
            child = self._make_node(
                children_frame, child_key, child_value, depth + 1
            )
            node["children"].append(child)

        if expanded:
            children_frame.pack(fill="x")
        self._update_arrow(arrow, expanded)
        self._set_section_state(node, expanded)

        return node

    def _make_leaf(self, parent, key, value, depth):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2, padx=(depth * 22, 0))

        ttk.Label(row, text=f"{key}:", width=30, anchor="w").pack(side="left")

        if isinstance(value, bool):
            variable = tk.BooleanVar(value=value)
            widget = ttk.Checkbutton(row, variable=variable)
        else:
            variable = tk.StringVar(
                value="" if value is None else self._format_leaf(value)
            )
            widget = ttk.Entry(row, textvariable=variable, width=65)

        widget.pack(side="left", fill="x", expand=True)

        node = {
            "kind": "leaf",
            "key": key,
            "value": value,
            "variable": variable,
            "widget": widget,
            "bool": isinstance(value, bool),
        }
        self._nodes.append(node)
        return node

    @staticmethod
    def _format_leaf(value):
        if isinstance(value, (dict, list)):
            return yaml.safe_dump(
                value, default_flow_style=True, sort_keys=False
            ).strip()
        return str(value)

    @staticmethod
    def _parse_leaf(node):
        if node["bool"]:
            return bool(node["variable"].get())

        raw = node["variable"].get().strip()
        if raw == "":
            return None

        try:
            return yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Invalid YAML value for '{node['key']}': {exc}"
            ) from exc

    def _toggle_section(self, node, state, arrow, children_frame):
        enabled = bool(state.get())
        self._set_section_state(node, enabled)
        self._update_arrow(arrow, enabled)

        if enabled:
            children_frame.pack(fill="x")
        else:
            children_frame.pack_forget()

    @staticmethod
    def _set_section_state(node, enabled):
        node["state"].set(enabled)
        for child in node["children"]:
            if child["kind"] == "section":
                child["state"].set(enabled and child["state"].get())
                if not enabled:
                    child["frame"].pack_forget()

    @staticmethod
    def _update_arrow(arrow, expanded):
        arrow.configure(text="▼" if expanded else "▶")

    def _collect_node(self, node, parent_enabled=True):
        if node["kind"] == "leaf":
            if not parent_enabled:
                return None
            return self._parse_leaf(node)

        enabled = parent_enabled and bool(node["state"].get())
        if not enabled:
            return None

        result = {}
        for child in node["children"]:
            result[child["key"]] = self._collect_node(child, enabled)
        return result

    def get_data(self):
        data = {}
        for node in self._nodes:
            if node["kind"] == "section" and node.get("parent") is None:
                data[node["key"]] = self._collect_node(node)
            elif node["kind"] == "leaf" and node.get("parent") is None:
                data[node["key"]] = self._collect_node(node)

        return data

    def _set_parent_links(self):
        def visit(node, parent=None):
            node["parent"] = parent
            if node["kind"] == "section":
                for child in node["children"]:
                    visit(child, node)

        for node in self._nodes:
            if node.get("parent") is None:
                visit(node)

    def set_data(self, data):
        if not isinstance(data, dict):
            raise ValueError("The case configuration must contain a YAML mapping.")

        self._clear_form()

        for key, value in data.items():
            self._make_node(self.form, key, value)

        self._set_parent_links()

    def refresh_saved_cases(self):
        cases = self.manager.list_saved()
        self.saved_cases["values"] = cases
        self.saved_cases.set(cases[0] if cases else "")

    def new_case(self):
        try:
            self.set_data(self._schema_from_current())
            self.status.set(
                "New case configuration — sections open are enabled; "
                "closed sections are unset."
            )
        except Exception as exc:
            messagebox.showerror("New case error", str(exc))

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

    def _save_data(self):
        return self.get_data()

    def save_current(self):
        try:
            data = self._save_data()
            path = self.manager.save_current(data)
            self.status.set(f"Saved current case: {path}")
        except Exception as exc:
            messagebox.showerror("Save error", str(exc))

    def save_as(self):
        try:
            data = self._save_data()
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
