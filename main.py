from logging import FileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import DevConfig
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevConfig)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail= Mail(app)

login_manager=LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

import routes



