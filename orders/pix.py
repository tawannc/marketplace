def gerar_pix(total, pedido_id):
    chave_pix = "61991974350"
    nome_recebedor = "Marketplace"
    cidade = "GOIANIA"

    payload = f"""
000201
010212
52040000
5303986
540{str(total).replace('.', '')}
5802BR
5913{nome_recebedor}
6007{cidade}
62070503*** 
6304
""".strip()

    return payload
