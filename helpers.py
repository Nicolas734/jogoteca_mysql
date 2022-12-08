from jogoteca import app
import os

def recupera_imagem(id,jogo):
    for nome_arquivo in os.listdir(app.config['UPLOADS_PATH']):
        if f'capa_{jogo.nome.lower().replace(" ","_")}_{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'


def deleta_arquivo(jogo):
    arquivo = recupera_imagem(jogo.id,jogo)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOADS_PATH'], arquivo))