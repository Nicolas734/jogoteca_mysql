from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import db, app
import time

from helpers import recupera_imagem, deleta_arquivo, Formulario_jogo, Formulario_login

from models import Jogos, Usuarios

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', titulo_pagina="Jogoteca", jogos = lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in  session or session['usuario_logado'] == None:
        flash('Acesso não permitido...')
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        formulario = Formulario_jogo()
        return render_template("novo.html", titulo="Cadastrar novo jogo", titulo_pagina="Cadastro de jogos", formulario=formulario)


@app.route('/criar', methods=['POST'])
def criar():
    formulario = Formulario_jogo(request.form)

    if not formulario.validate_on_submit():
        redirect(url_for('novo'))

    nome = formulario.nome.data
    categoria = formulario.categoria.data
    console = formulario.console.data
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo já existente...")
        return redirect(url_for('index'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo_jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        uploads_path = app.config['UPLOADS_PATH']
        timestamp = time.time()
        arquivo.save(f'{uploads_path}/capa_{novo_jogo.nome.lower().replace(" ","_")}_{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


# UPDATE

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in  session or session['usuario_logado'] == None:
        flash('Acesso não permitido...')
        return redirect(url_for('login',proxima=url_for('editar',id=id)))
    else:
        jogo = Jogos.query.filter_by(id=id).first()
        formulario = Formulario_jogo()
        formulario.nome.data = jogo.nome
        formulario.categoria.data = jogo.categoria
        formulario.console.data = jogo.console
        capa_jogo = recupera_imagem(id, jogo)
        return render_template("editar.html", titulo="Editando jogo", titulo_pagina="Edição de jogos", id=id, capa_jogo=capa_jogo, formulario=formulario)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    jogo = Jogos.query.filter_by(id=id).first()

    formulario = Formulario_jogo(request.form)

    if formulario.validate_on_submit():

        jogo.nome = formulario.nome.data
        jogo.categoria = formulario.categoria.data
        jogo.console = formulario.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        uploads_path = app.config['UPLOADS_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo)
        arquivo.save(f'{uploads_path}/capa_{jogo.nome.lower().replace(" ","_")}_{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


# DELETE

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario_logado' not in  session or session['usuario_logado'] == None:
        flash('Acesso não permitido...')
        return redirect(url_for('login'))
    else:
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Jogo deletado com sucesso!')

        return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    formulario = Formulario_login()
    return render_template('login.html', titulo="Login de Usuario", titulo_pagina="Login", proxima=proxima, formulario=formulario)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    formulario = Formulario_login(request.form)
    usuario = Usuarios.query.filter_by(username=formulario.username.data).first()
    if usuario:
        if formulario.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso...')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuario não logado...')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso...')
    return redirect(url_for('login'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)