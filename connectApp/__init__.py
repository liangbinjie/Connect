from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
import pathlib
import os 


db = SQLAlchemy()


UPLOAD_FOLDER = f'{pathlib.Path(__file__).parent.resolve()}/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .edit import edit as edit_blueprint
    app.register_blueprint(edit_blueprint)

    return app
