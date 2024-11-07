from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

"""
flask shell
db.create_all() -> cria banco de dados e inicia sessao
db.session.commit() -> executa alterações
exit()

"""