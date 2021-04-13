from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_login import LoginManager
from flask_pagedown import PageDown


bootstrap = Bootstrap()
moment = Moment()
migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
pagedown = PageDown()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)

    from myproject.main.views import main as main_blueprint1
    from myproject.main.errors import error as main_blueprint2
    from myproject.auth.views import auth as auth_blueprint
    from myproject.api.authentication import api as api_blueprint

    app.register_blueprint(main_blueprint1)
    app.register_blueprint(main_blueprint2)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app