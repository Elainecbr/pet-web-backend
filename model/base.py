from flask_sqlalchemy import SQLAlchemy

# Inicializa o objeto SQLAlchemy, mas não o vincula a um aplicativo Flask ainda.
# O vínculo é feito pela fábrica de aplicação em `__init__.py` para permitir testes
# e execução de scripts auxiliares.
db = SQLAlchemy()
