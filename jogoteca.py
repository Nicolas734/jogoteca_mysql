from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.secret_key = 'lira'
#esse name faz uma referência ao próprio arquivo, garantindo que isso vai fazer rodar a aplicação.


# configurações de conexão do banco
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'jogoteca'
    )

# cria a conexão entre a aplicação e o mysql
db = SQLAlchemy(app)


# representação das tabelas do banco de dados
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(50), nullable = False)
    categoria = db.Column(db.String(40), nullable = False)
    console = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.nome

class Usuarios(db.Model):
    username = db.Column(db.String(50), primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    senha = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.username


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
    print(jogo)
    if jogo:
        flash("Jogo já existente...")
        return redirect(url_for('index'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo_jogo)
        db.session.commit()

    return redirect(url_for('index'))


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


app.run(debug = True)