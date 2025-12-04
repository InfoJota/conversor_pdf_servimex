from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Prestador:
    cnpj: str
    inscricao_municipal: str
    razao_social: str
    endereco: str
    numero: str
    complemento: str
    bairro: str
    municipio: str
    uf: str
    cep: str
    item_lista_servico: str


DEFAULT_PRESTADOR = Prestador(
    cnpj="58149782000105",
    inscricao_municipal="11447",
    razao_social="SERVIMEX LOGISTICA LTDA",
    endereco="R AUGUSTO SEVERO",
    numero="7",
    complemento="ANDAR 3 ANDAR 5 ANDAR 6A",
    bairro="CENTRO",
    municipio="3548500",
    uf="SP",
    cep="11010919",
    item_lista_servico="0107",
)


@dataclass
class ValoresServico:
    valor_servicos: float = 0.0
    pis: float = 0.0
    cofins: float = 0.0
    csll: float = 0.0
    irrf: float = 0.0
    inss: float = 0.0
    iss: float = 0.0


@dataclass
class NFSeData:
    numero: str
    codigo_verificacao: str
    data_emissao: datetime
    valores: ValoresServico
    prestador: Prestador
    discriminacao: str = "Servicos conforme NFSe"
    natureza_operacao: str = "1"
    optante_simples: str = "2"
    incentivador_cultural: str = "2"
    serie_rps: str = "U"
    tipo_rps: str = "1"

    @property
    def competencia(self) -> str:
        return self.data_emissao.strftime("%Y-%m-%d")

    @property
    def data_iso(self) -> str:
        return self.data_emissao.strftime("%Y-%m-%dT%H:%M:%S")
