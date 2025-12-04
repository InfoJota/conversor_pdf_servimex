import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional
import time
from threading import Thread


class ConverterGUI:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Conversor NFSe - PDF para XML")
        self.window.geometry("600x300")
        self.window.resizable(False, False)
        
        self.directory_path: Optional[Path] = None
        self.converter_callback: Optional[Callable[[str], int]] = None
        
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        # Frame principal
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Conversor de NFSe - ServiMax",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para seleção de diretório
        dir_frame = tk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=10)
        
        dir_label = tk.Label(dir_frame, text="Pasta com PDFs:", font=("Arial", 10))
        dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.dir_entry = tk.Entry(dir_frame, width=40, font=("Arial", 10))
        self.dir_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        browse_btn = tk.Button(
            dir_frame,
            text="Selecionar...",
            command=self._browse_directory,
            font=("Arial", 10),
            width=12
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Botão converter
        self.convert_btn = tk.Button(
            main_frame,
            text="Converter PDFs para XML",
            command=self._start_conversion,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            width=25
        )
        self.convert_btn.pack(pady=20)
        
        # Label de status
        self.status_label = tk.Label(
            main_frame,
            text="Selecione uma pasta e clique em Converter",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(pady=10)
        
        # Label de tempo
        self.time_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 9),
            fg="blue"
        )
        self.time_label.pack()
        
    def _browse_directory(self) -> None:
        directory = filedialog.askdirectory(
            title="Selecione a pasta com os PDFs da NFSe"
        )
        if directory:
            self.directory_path = Path(directory)
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, str(self.directory_path))
            self.status_label.config(text="Pasta selecionada. Clique em Converter.", fg="blue")
    
    def _start_conversion(self) -> None:
        if not self.directory_path or not self.dir_entry.get():
            messagebox.showerror("Erro", "Por favor, selecione uma pasta primeiro.")
            return
        
        if not self.converter_callback:
            messagebox.showerror("Erro", "Callback de conversão não configurado.")
            return
        
        # Desabilita o botão durante a conversão
        self.convert_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processando...", fg="orange")
        self.time_label.config(text="")
        
        # Executa conversão em thread separada para não travar a UI
        thread = Thread(target=self._run_conversion)
        thread.daemon = True
        thread.start()
    
    def _run_conversion(self) -> None:
        start_time = time.time()
        
        try:
            # Chama o callback de conversão
            count = self.converter_callback(str(self.directory_path))
            
            elapsed_time = time.time() - start_time
            
            # Atualiza UI na thread principal
            self.window.after(0, self._show_success, count, elapsed_time)
            
        except Exception as exc:
            elapsed_time = time.time() - start_time
            self.window.after(0, self._show_error, str(exc), elapsed_time)
    
    def _show_success(self, count: int, elapsed_time: float) -> None:
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(
            text=f"✓ Conversão concluída com sucesso!",
            fg="green"
        )
        self.time_label.config(
            text=f"Tempo de processamento: {elapsed_time:.2f} segundos"
        )
        
        output_dir = self.directory_path / "PDF_Convertido"
        messagebox.showinfo(
            "Conversão Concluída",
            f"Sucesso!\n\n"
            f"Arquivos convertidos: {count}\n"
            f"Tempo: {elapsed_time:.2f}s\n\n"
            f"XMLs salvos em:\n{output_dir}"
        )
    
    def _show_error(self, error_msg: str, elapsed_time: float) -> None:
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✗ Erro na conversão", fg="red")
        self.time_label.config(
            text=f"Tempo até erro: {elapsed_time:.2f} segundos"
        )
        messagebox.showerror("Erro", f"Erro durante a conversão:\n\n{error_msg}")
    
    def set_converter_callback(self, callback: Callable[[str], int]) -> None:
        """Define o callback que será executado para converter os PDFs."""
        self.converter_callback = callback
    
    def run(self) -> None:
        """Inicia o loop principal da GUI."""
        self.window.mainloop()
