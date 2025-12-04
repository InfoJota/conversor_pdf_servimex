from pathlib import Path
from typing import List, Optional
import xml.etree.ElementTree as ET

from services.pdf_reader import PDFInvoiceReader
from services.parser import ServimaxParser
from services.xml_builder import AbrasfXmlBuilder


class NFSeConverter:
    def __init__(
        self,
        reader: PDFInvoiceReader,
        parser: ServimaxParser,
        xml_builder: AbrasfXmlBuilder,
    ) -> None:
        self.reader = reader
        self.parser = parser
        self.xml_builder = xml_builder

    def convert_directory(self, directory: Path, output_path: Optional[Path] = None) -> List[Path]:
        directory = Path(directory)
        pdf_files = sorted(directory.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(f"Nenhum PDF encontrado em {directory}")

        per_file = output_path is None
        outputs: List[Path] = []

        if per_file:
            target_dir = directory / "PDF_Convertido"
            target_dir.mkdir(parents=True, exist_ok=True)
            for pdf in pdf_files:
                outputs.append(self._convert_per_file(pdf, target_dir))
            return outputs

        consolidated_root = ET.Element("ListaNfse")
        for pdf in pdf_files:
            comp_nfse = self._convert_to_element(pdf)
            consolidated_root.append(comp_nfse)
        target = self._resolve_output_path(output_path)
        ET.ElementTree(consolidated_root).write(target, encoding="utf-8", xml_declaration=True)
        outputs.append(target)
        return outputs

    def _convert_per_file(self, pdf_path: Path, target_dir: Path) -> Path:
        comp_nfse = self._convert_to_element(pdf_path)
        root = ET.Element("ListaNfse")
        root.append(comp_nfse)
        tree = ET.ElementTree(root)
        output_path = target_dir / f"{pdf_path.stem}.xml"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        return output_path

    def _convert_to_element(self, pdf_path: Path) -> ET.Element:
        xml_tree = self._convert_pdf(pdf_path)
        comp_nfse = xml_tree.getroot().find("CompNfse")
        if comp_nfse is None:
            raise ValueError("Estrutura XML invalida: CompNfse nao encontrado")
        return comp_nfse

    def _convert_pdf(self, pdf_path: Path) -> ET.ElementTree:
        content = self.reader.read_text(pdf_path)
        data = self.parser.parse(content)
        return self.xml_builder.build_tree(data)

    def _resolve_output_path(self, output: Path) -> Path:
        output = Path(output)
        if output.is_dir():
            output.mkdir(parents=True, exist_ok=True)
            return output / "nfse_comp_abrasf_CONSOLIDADO_vX.xml"
        output.parent.mkdir(parents=True, exist_ok=True)
        return output
