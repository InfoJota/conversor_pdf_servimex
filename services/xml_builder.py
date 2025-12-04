"""Construtor de XML no padrão ABRASF para NFSe.

Gera XML compatível com o padrão da Associação Brasileira das Secretarias
de Finanças das Capitais (ABRASF) versão 2.x.
"""

import xml.etree.ElementTree as ET
from models.nfse import NFSeData


class AbrasfXmlBuilder:
    """Constrói estrutura XML ABRASF a partir de dados de NFSe."""
    def __init__(self) -> None:
        self.namespace = "http://www.abrasf.org.br/nfse.xsd"
        ET.register_namespace("", self.namespace)

    def build_tree(self, data: NFSeData) -> ET.ElementTree:
        """Constrói árvore XML completa para uma NFSe.
        
        Args:
            data: Dados da NFSe a serem convertidos em XML
            
        Returns:
            ElementTree com estrutura XML ABRASF completa
        """
        root = ET.Element("ListaNfse")
        root.append(self.build_comp_nfse(data))
        return ET.ElementTree(root)

    def build_comp_nfse(self, data: NFSeData) -> ET.Element:
        comp_nfse = ET.Element("CompNfse")
        nfse = ET.SubElement(comp_nfse, "Nfse")
        inf = ET.SubElement(nfse, "InfNfse", Id=f"NFS{data.numero}")

        ET.SubElement(inf, "Numero").text = data.numero
        ET.SubElement(inf, "CodigoVerificacao").text = data.codigo_verificacao
        ET.SubElement(inf, "DataEmissao").text = data.data_iso

        ident_rps = ET.SubElement(inf, "IdentificacaoRps")
        ET.SubElement(ident_rps, "Numero").text = data.numero
        ET.SubElement(ident_rps, "Serie").text = data.serie_rps
        ET.SubElement(ident_rps, "Tipo").text = data.tipo_rps

        ET.SubElement(inf, "NaturezaOperacao").text = data.natureza_operacao
        ET.SubElement(inf, "OptanteSimplesNacional").text = data.optante_simples
        ET.SubElement(inf, "IncentivadorCultural").text = data.incentivador_cultural
        ET.SubElement(inf, "Competencia").text = data.competencia

        servico = ET.SubElement(inf, "Servico")
        valores = ET.SubElement(servico, "Valores")
        ET.SubElement(valores, "ValorServicos").text = self._fmt(data.valores.valor_servicos)
        ET.SubElement(valores, "IssRetido").text = "2"
        ET.SubElement(valores, "ValorPis").text = self._fmt(data.valores.pis)
        ET.SubElement(valores, "ValorCofins").text = self._fmt(data.valores.cofins)
        ET.SubElement(valores, "ValorIr").text = self._fmt(data.valores.irrf)
        ET.SubElement(valores, "ValorInss").text = self._fmt(data.valores.inss)
        ET.SubElement(valores, "ValorCsll").text = self._fmt(data.valores.csll)

        prestador = data.prestador
        ET.SubElement(servico, "ItemListaServico").text = prestador.item_lista_servico
        ET.SubElement(servico, "CodigoMunicipio").text = prestador.municipio
        ET.SubElement(servico, "Discriminacao").text = data.discriminacao

        prestador_node = ET.SubElement(inf, "PrestadorServico")
        ident_prestador = ET.SubElement(prestador_node, "IdentificacaoPrestador")
        ET.SubElement(ident_prestador, "Cnpj").text = prestador.cnpj
        ET.SubElement(ident_prestador, "InscricaoMunicipal").text = prestador.inscricao_municipal
        ET.SubElement(prestador_node, "RazaoSocial").text = prestador.razao_social

        endereco = ET.SubElement(prestador_node, "Endereco")
        ET.SubElement(endereco, "Endereco").text = prestador.endereco
        ET.SubElement(endereco, "Numero").text = prestador.numero
        ET.SubElement(endereco, "Complemento").text = prestador.complemento
        ET.SubElement(endereco, "Bairro").text = prestador.bairro
        ET.SubElement(endereco, "CodigoMunicipio").text = prestador.municipio
        ET.SubElement(endereco, "Uf").text = prestador.uf
        ET.SubElement(endereco, "Cep").text = prestador.cep

        return comp_nfse

    def _fmt(self, value: float) -> str:
        return f"{value:.2f}"
