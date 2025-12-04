"""Serviço de leitura de arquivos PDF.

Extrai texto de PDFs de notas fiscais eletrônicas usando pdfminer.
"""

from pathlib import Path
from pdfminer.high_level import extract_text


class PDFInvoiceReader:
    """Leitor de PDFs de notas fiscais."""
    def read_text(self, pdf_path: Path) -> str:
        """Extrai texto completo de um arquivo PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Texto completo extraído do PDF
            
        Raises:
            FileNotFoundError: Se o PDF não existir
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF nao encontrado: {pdf_path}")
        return extract_text(str(pdf_path))
