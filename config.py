SECRET_KEY = 'lira'

# configurações de conexão do banco
SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'jogoteca'
    )