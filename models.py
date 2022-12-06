from jogoteca import db


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