import re
from datetime import datetime
from typing import Optional

from models.nfse import NFSeData, Prestador, ValoresServico


class ServimaxParser:
    VALOR_SERVICO_PATTERN = re.compile(
        r"Valor\s*(?:de|dos)\s*Servi\S*os\s*R\$[: ]*.*?([\d\.,]+)",
        flags=re.IGNORECASE | re.DOTALL,
    )

    def __init__(self, prestador: Prestador, discriminacao: str = "Servicos conforme NFSe") -> None:
        self.prestador = prestador
        self.discriminacao = discriminacao

    def parse(self, content: str) -> NFSeData:
        numero = self._search(r"NFSe\s*(\d+)", content, fallback="0")
        codigo = self._search(r"C[oó]digo de Verifica[cç][aã]o\s*([\w\d]+)", content, fallback="XXXXXX")
        data_emissao = self._parse_data_emissao(content)

        valores = ValoresServico(
            valor_servicos=self._extract_valor_servico(content),
            pis=self._extract_imposto(r"PIS.*?R\$[: ]*([\d\.,]+)", content),
            cofins=self._extract_imposto(r"COFINS.*?R\$[: ]*([\d\.,]+)", content),
            csll=self._extract_imposto(r"CSLL.*?R\$[: ]*([\d\.,]+)", content),
            irrf=self._extract_imposto(r"IRRF.*?R\$[: ]*([\d\.,]+)", content),
            inss=self._extract_imposto(r"INSS.*?R\$[: ]*([\d\.,]+)", content),
            iss=self._extract_imposto(r"Valor ISS.*?R\$[: ]*([\d\.,]+)", content),
        )

        return NFSeData(
            numero=numero,
            codigo_verificacao=codigo,
            data_emissao=data_emissao,
            valores=valores,
            prestador=self.prestador,
            discriminacao=self.discriminacao,
        )

    def _extract_valor_servico(self, content: str) -> float:
        match = self.VALOR_SERVICO_PATTERN.search(content)
        return self._match_to_float(match)

    def _extract_imposto(self, pattern: str, content: str) -> float:
        match = re.search(pattern, content, flags=re.IGNORECASE | re.DOTALL)
        return self._match_to_float(match)

    def _match_to_float(self, match: Optional[re.Match]) -> float:
        if not match:
            return 0.0
        value = match.group(1).strip()
        if not value:
            return 0.0
        return float(value.replace(".", "").replace(",", "."))

    def _search(self, pattern: str, content: str, fallback: str = "") -> str:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        return match.group(1) if match else fallback

    def _parse_data_emissao(self, content: str) -> datetime:
        match = re.search(r"(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2}:\d{2})", content)
        if not match:
            return datetime.now()
        return datetime.strptime(f"{match.group(1)} {match.group(2)}", "%d/%m/%Y %H:%M:%S")
