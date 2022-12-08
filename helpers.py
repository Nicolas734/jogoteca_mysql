from jogoteca import app
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class Formulario_jogo(FlaskForm):
    nome = StringField('Nome do jogo', [validators.data_required(), validators.length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class Formulario_login(FlaskForm):
    username = StringField('Nome de usuario', [validators.data_required(), validators.length(min=1, max=50)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Entrar')


def recupera_imagem(id,jogo):
    for nome_arquivo in os.listdir(app.config['UPLOADS_PATH']):
        if f'capa_{jogo.nome.lower().replace(" ","_")}_{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'


def deleta_arquivo(jogo):
    arquivo = recupera_imagem(jogo.id,jogo)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOADS_PATH'], arquivo))