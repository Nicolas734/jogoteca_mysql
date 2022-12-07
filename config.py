import os

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

# caminho relativo da pasta uploads
UPLOADS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'