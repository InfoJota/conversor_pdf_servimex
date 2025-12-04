"""Modelos de dados para NFSe (Nota Fiscal de Serviços Eletrônica).

Este módulo contém as classes de domínio que representam os dados
extraídos de PDFs de NFSe e utilizados na geração de XML ABRASF.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Prestador:
    """Representa os dados do prestador de serviços.
    
    Attributes:
        cnpj: CNPJ do prestador sem formatação
        inscricao_municipal: Inscrição municipal
        razao_social: Razão social completa
        endereco: Logradouro
        numero: Número do endereço
        complemento: Complemento do endereço
        bairro: Bairro
        municipio: Código IBGE do município
        uf: Sigla da UF
        cep: CEP sem formatação
        item_lista_servico: Código do serviço na lista CNAE
    """
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
    """Representa os valores monetários da NFSe.
    
    Todos os valores são em reais (R$) e armazenados como float.
    """
    valor_servicos: float = 0.0
    pis: float = 0.0
    cofins: float = 0.0
    csll: float = 0.0
    irrf: float = 0.0
    inss: float = 0.0
    iss: float = 0.0


@dataclass
class NFSeData:
    """Representa uma NFSe completa extraída de PDF.
    
    Agrega todos os dados necessários para gerar o XML no padrão ABRASF.
    
    Attributes:
        numero: Número da NFSe
        codigo_verificacao: Código de verificação da nota
        data_emissao: Data e hora de emissão
        valores: Valores dos serviços e tributos
        prestador: Dados do prestador de serviços
        discriminacao: Descrição dos serviços prestados
        natureza_operacao: Código da natureza da operação
        optante_simples: Se é optante do Simples Nacional (1=Sim, 2=Não)
        incentivador_cultural: Se é incentivador cultural (1=Sim, 2=Não)
        serie_rps: Série do RPS
        tipo_rps: Tipo do RPS
    """
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
