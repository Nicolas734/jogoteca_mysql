from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__) 
app.secret_key = 'lira'
#esse name faz uma referência ao próprio arquivo, garantindo que isso vai fazer rodar a aplicação.

class Jogo:
    def __init__(self,nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo("Skyrim", "RPG", "PC")
jogo2 = Jogo("Fallout new vegas", "RPG", "PC")
jogo3 =Jogo("The Witcher 3", "RPG", "PC")
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, username, senha):
        self.nome = nome
        self.username = username
        self.senha = senha

usuario1 = Usuario("Nicolas", "Nicolas734", "12345")
usuario2 = Usuario("Natalia", "A LIRA", "lira")
usuario3 = Usuario("Rodrigo", "Digao_calcada", "calcada")
usuario4 = Usuario("Raniel", "Agro_boy", "agro_tec")
usuario5 = Usuario("Rafael", "veio", "rafel")

usuarios = {
    usuario1.username:usuario1,
    usuario2.username:usuario2,
    usuario3.username:usuario3,
    usuario4.username:usuario4,
    usuario5.username:usuario5
    }

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista, titulo_pagina="Jogoteca")


@app.route('/novo_jogo')
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
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login de Usuario", titulo_pagina="Login", proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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


app.run(debug = True)