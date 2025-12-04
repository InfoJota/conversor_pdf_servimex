from pathlib import Path
from typing import Optional


class DirectorySelector:
    def choose_directory(self) -> Optional[Path]:
        directory = self._prompt_with_tk()
        if directory:
            return directory
        path = input("Informe o diretorio com os PDFs da ServiMax: ").strip()
        return Path(path) if path else None

    def _prompt_with_tk(self) -> Optional[Path]:
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            selected = filedialog.askdirectory(title="Selecione a pasta com os PDFs para conversao")
            root.destroy()
            return Path(selected) if selected else None
        except Exception:
            return None


class ConsoleView:
    def info(self, message: str) -> None:
        print(message)

    def error(self, message: str) -> None:
        print(f"ERRO: {message}")
