import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '6ddc470b93ea6b43e950a0ad94121b27b17391a513b1c8d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = "shukranjsp@gmail.com"
app.config['MAIL_PASSWORD'] = 'hmkw zipe bidz dyrz'
mail = Mail(app)
from flaskblog import routes, models # noqa