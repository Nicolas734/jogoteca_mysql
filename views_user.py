from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from helpers import Formulario_login, Formulario_usuario
from models import Usuarios
from flask_bcrypt import check_password_hash, generate_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    formulario = Formulario_login()
    return render_template('login.html', titulo="Login de Usuario", titulo_pagina="Login", proxima=proxima, formulario=formulario)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    formulario = Formulario_login(request.form)
    usuario = Usuarios.query.filter_by(username=formulario.username.data).first()
    verificacao_senha = check_password_hash(usuario.senha, formulario.senha.data)
    if usuario and verificacao_senha:
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


@app.route('/novo_usuario')
def novo_usuario():
    formulario = Formulario_usuario()
    return render_template('novo_usuario.html', titulo="Cadastro de Usuario", titulo_pagina="Cadastro-Usuario", formulario = formulario)


@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    formulario = Formulario_usuario(request.form)

    if formulario.validate_on_submit():

        nome = formulario.nome.data
        username = formulario.username.data
        senha = generate_password_hash(formulario.senha.data).decode('utf-8')
        usuario =  Usuarios.query.filter_by(username=username).first()

        if usuario:
            flash("Nome de usuario ja em uso...")
            return redirect(url_for('novo_usuario'))

        else:
            novo_usuario = Usuarios(nome=nome, username=username, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
    
    return redirect(url_for('index'))