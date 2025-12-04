from pathlib import Path
from pdfminer.high_level import extract_text


class PDFInvoiceReader:
    def read_text(self, pdf_path: Path) -> str:
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF nao encontrado: {pdf_path}")
        return extract_text(str(pdf_path))
