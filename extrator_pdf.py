"""Ponto de entrada principal do Conversor NFSe ServiMax.

Aplicação desktop que converte PDFs de NFSe do sistema ServiMax (Prefeitura
de Santos/SP) para XML no padrão ABRASF, facilitando integração contábil.

Arquitetura:
    - Models: Estruturas de dados de domínio (NFSeData, Prestador, etc.)
    - Services: Lógica de negócio (PDF reader, parser, XML builder)
    - Controllers: Orquestração do fluxo de conversão
    - Views: Interface gráfica Tkinter

Uso:
    python extrator_pdf.py
"""

from pathlib import Path
from typing import Optional, Sequence

from controllers.converter import NFSeConverter
from models.nfse import DEFAULT_PRESTADOR
from services.pdf_reader import PDFInvoiceReader
from services.parser import ServimaxParser
from services.xml_builder import AbrasfXmlBuilder
from views.gui import ConverterGUI


def create_converter() -> NFSeConverter:
    reader = PDFInvoiceReader()
    parser = ServimaxParser(DEFAULT_PRESTADOR)
    builder = AbrasfXmlBuilder()
    return NFSeConverter(reader, parser, builder)


def converter_nfse_servimax(diretorio_pdf: str, saida_xml: Optional[str] = None) -> int:
    """Converte PDFs para XML e retorna o número de arquivos gerados."""
    directory = Path(diretorio_pdf)
    converter = create_converter()
    if saida_xml:
        outputs = converter.convert_directory(directory, Path(saida_xml))
    else:
        outputs = converter.convert_directory(directory)
    return len(outputs)


def main() -> None:
    gui = ConverterGUI()
    gui.set_converter_callback(converter_nfse_servimax)
    gui.run()


if __name__ == "__main__":
    main()
