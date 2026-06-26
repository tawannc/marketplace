import requests
import xml.etree.ElementTree as ET

def calcular_frete(cep_origem, cep_destino, peso=1, comprimento=20, altura=5, largura=15):
    url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"

    params = {
        "nCdEmpresa": "",
        "sDsSenha": "",
        "nCdServico": "04510,04014",  # 04510 = PAC, 04014 = SEDEX
        "sCepOrigem": cep_origem,
        "sCepDestino": cep_destino,
        "nVlPeso": peso,
        "nCdFormato": 1,
        "nVlComprimento": comprimento,
        "nVlAltura": altura,
        "nVlLargura": largura,
        "nVlDiametro": 0,
        "sCdMaoPropria": "N",
        "nVlValorDeclarado": 0,
        "sCdAvisoRecebimento": "N",
        "StrRetorno": "xml"
    }

    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)

    resultados = []

    for servico in root.findall(".//cServico"):
        resultados.append({
            "codigo": servico.find("Codigo").text,
            "valor": servico.find("Valor").text,
            "prazo": servico.find("PrazoEntrega").text,
            "erro": servico.find("Erro").text,
            "msg": servico.find("MsgErro").text,
        })

    return resultados
