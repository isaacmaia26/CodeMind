"""CodeMind graphical interface."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

from codemind.explainer import CodeMindExplainer
from codemind.speaker import speak


SAMPLE_CODE = '''import os

def greet(name):
    if name:
        print("Hello", name)
    else:
        print("No name")

for user in ["Portuga"]:
    greet(user)
'''


class CodeMindApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CodeMind - Python Code Explainer")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)
        self.explainer = CodeMindExplainer()
        self.mode = tk.StringVar(value="beginner")
        self._build_ui()

    def _build_ui(self) -> None:
        self.root.configure(bg="#111111")

        header = tk.Frame(self.root, bg="#111111")
        header.pack(fill="x", padx=18, pady=(16, 8))

        title = tk.Label(
            header,
            text="CodeMind",
            font=("Segoe UI", 28, "bold"),
            bg="#111111",
            fg="#A970FF",
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header,
            text="  O teu código Python explicado em linguagem humana",
            font=("Segoe UI", 12),
            bg="#111111",
            fg="#DDDDDD",
        )
        subtitle.pack(side="left", pady=(12, 0))

        controls = tk.Frame(self.root, bg="#111111")
        controls.pack(fill="x", padx=18, pady=8)

        tk.Radiobutton(
            controls,
            text="Modo iniciante",
            variable=self.mode,
            value="beginner",
            bg="#111111",
            fg="#FFFFFF",
            selectcolor="#222222",
            activebackground="#111111",
            activeforeground="#A970FF",
        ).pack(side="left")

        tk.Radiobutton(
            controls,
            text="Modo técnico",
            variable=self.mode,
            value="technical",
            bg="#111111",
            fg="#FFFFFF",
            selectcolor="#222222",
            activebackground="#111111",
            activeforeground="#A970FF",
        ).pack(side="left", padx=12)

        self._button(controls, "Analisar", self.analyze).pack(side="right", padx=4)
        self._button(controls, "Falar", self.speak_result).pack(side="right", padx=4)
        self._button(controls, "Abrir .py", self.open_file).pack(side="right", padx=4)
        self._button(controls, "Exemplo", self.load_sample).pack(side="right", padx=4)
        self._button(controls, "Limpar", self.clear).pack(side="right", padx=4)

        main = tk.PanedWindow(self.root, orient="horizontal", bg="#111111", sashwidth=6)
        main.pack(fill="both", expand=True, padx=18, pady=(8, 18))

        left = tk.Frame(main, bg="#171717")
        right = tk.Frame(main, bg="#171717")
        main.add(left, minsize=420)
        main.add(right, minsize=420)

        tk.Label(left, text="Código Python", font=("Segoe UI", 12, "bold"), bg="#171717", fg="#FFFFFF").pack(anchor="w", padx=12, pady=(10, 4))
        self.code_box = tk.Text(left, wrap="none", bg="#0B0B0B", fg="#EAEAEA", insertbackground="#A970FF", font=("Consolas", 11), relief="flat")
        self.code_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        tk.Label(right, text="Explicação", font=("Segoe UI", 12, "bold"), bg="#171717", fg="#FFFFFF").pack(anchor="w", padx=12, pady=(10, 4))
        self.output_box = tk.Text(right, wrap="word", bg="#0B0B0B", fg="#EAEAEA", insertbackground="#A970FF", font=("Segoe UI", 11), relief="flat")
        self.output_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.load_sample()

    def _button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#A970FF",
            fg="#FFFFFF",
            activebackground="#7B2CFF",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=14,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def analyze(self) -> None:
        code = self.code_box.get("1.0", "end")
        explanation = self.explainer.explain(code, self.mode.get())
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", explanation)

    def speak_result(self) -> None:
        text = self.output_box.get("1.0", "end").strip()
        if not text:
            self.analyze()
            text = self.output_box.get("1.0", "end").strip()
        success, message = speak(text)
        if not success:
            messagebox.showwarning("CodeMind", message)

    def open_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if not path:
            return
        with open(path, "r", encoding="utf-8", errors="replace") as file:
            self.code_box.delete("1.0", "end")
            self.code_box.insert("1.0", file.read())
        self.analyze()

    def load_sample(self) -> None:
        self.code_box.delete("1.0", "end")
        self.code_box.insert("1.0", SAMPLE_CODE)
        self.analyze()

    def clear(self) -> None:
        self.code_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")


def run_app() -> None:
    root = tk.Tk()
    app = CodeMindApp(root)
    root.mainloop()
