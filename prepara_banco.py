import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456'
    )

    print("Conectado com sucesso...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome do usuario ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS jogoteca")

cursor.execute("CREATE DATABASE jogoteca")

cursor.execute("USE jogoteca")

# criando as tebelas
TABLES = {}
TABLES['jogos'] = ('''
    CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(50) NOT NULL,
        `categoria` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['usuarios'] = ('''
    CREATE TABLE `usuarios` (
        `nome` varchar(20) NOT NULL,
        `username` varchar(50) NOT NULL,
        `senha` varchar(100) NOT NULL,
        PRIMARY KEY (`username`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabelas_nome in TABLES:
    tabelas_sql = TABLES[tabelas_nome]
    try:
        print('Criando tabela {}:'.format(tabelas_nome), end=' ')
        cursor.execute(tabelas_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("já existe...")
        else:
            print(err.msg)
    else:
        print("OK")


# inserindo usuarios

usuario_sql = 'INSERT INTO usuarios (nome, username, senha) values (%s, %s, %s)'
usuarios = [ 
    ("Nicolas Lima", "Nicolas734", generate_password_hash("12345").decode('utf-8')),
    ("Natalia Bessa", "A LIRA", generate_password_hash("lira").decode('utf-8')),
    ("Rodrigo ribeiro", "digao_calcada", generate_password_hash("calcada").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from usuarios')
print(' --------------- Usuarios ---------------')
for user in cursor.fetchall():
    print(user[1])



# inserindo jogos

jogos_sql = 'INSERT INTO jogos (nome, categoria, console) values (%s, %s, %s)'
jogos = [ 
    ("Skyrim", "RPG", "PC"),
    ("Fallout new vegas", "RPG", "PC"),
    ("The Witcher 3", "RPG", "PC")
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogos')
print(' --------------- Jogos ---------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito

conn.commit()

cursor.close()
conn.close()