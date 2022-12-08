from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from helpers import Formulario_login
from models import Usuarios


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