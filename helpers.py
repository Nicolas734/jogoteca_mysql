from jogoteca import app
import os

def recupera_imagem(id,jogo):
    for nome_arquivo in os.listdir(app.config['UPLOADS_PATH']):
        if f'capa_{jogo.nome.lower().replace(" ","_")}_{id}.jpg' == nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'