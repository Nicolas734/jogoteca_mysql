from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import db, app

from models import Jogos, Usuarios

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', titulo_pagina="Jogoteca", jogos = lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in  session or session['usuario_logado'] == None:
        flash('Acesso não permitido...')
        return redirect(url_for('login',proxima=url_for('novo')))
    else:
        return render_template("novo.html", titulo="cadastrar novo jogo", titulo_pagina="Cadastro de jogos")


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo já existente...")
        return redirect(url_for('index'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo_jogo)
        db.session.commit()

    return redirect(url_for('index'))


# UPDATE

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in  session or session['usuario_logado'] == None:
        flash('Acesso não permitido...')
        return redirect(url_for('login',proxima=url_for('editar')))
    else:
        jogo = Jogos.query.filter_by(id=id).first()
        return render_template("editar.html", titulo="Editando jogo", titulo_pagina="Edição de jogos", jogo=jogo)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    pass


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login de Usuario", titulo_pagina="Login", proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(username=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso...')
            proxima_pagina = request.form['proxima']
            
            if(proxima_pagina is None):
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('novo'))
    else:
        flash('Usuario não logado...')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso...')
    return redirect(url_for('index'))