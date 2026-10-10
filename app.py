from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
db = SQLAlchemy()

def create_application():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER:PASSWORD@localhost:3306/AiStudyAssistant'
    app.secret_key = os.environ.get('SECRET_KEY', 'a-safe-fallback-for-local-dev')

    db.init_app(app) 
    login_manager = LoginManager() 
    login_manager.init_app(app) 

    from models import User 
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid) 
    bcrypt = Bcrypt(app)
    from routes import register_routes 
    register_routes(app,db,bcrypt) 
    migrate = Migrate(app,db) 
    return app
    
