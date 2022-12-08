from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__) 
app.config.from_pyfile('config.py')

# cria a conexão entre a aplicação e o mysql
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from views import *

if __name__ == '__main__':
    app.run(debug = True)