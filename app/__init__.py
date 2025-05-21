from flask import Flask, render_template, url_for, redirect, request, abort, g, send_from_directory
from flask.sessions import SecureCookieSessionInterface
from flask_babel import Babel
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.initial import app
from app.models import User, Role, db
from app.initial import db
from flask_security import SQLAlchemyUserDatastore, Security

from config import Config

#migrate = Migrate(app, db)
#db = SQLAlchemy()
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

jwt = JWTManager(app)


# Регистрация путей Blueprint
from app.admin.routes import admin_bp

app.register_blueprint(admin_bp, url_prefix="/admin")


def get_locale():
    return 'ru'


babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

#@app.route('/registration.html')
#def serve_registration():
#    return render_template('registration.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Обрабатывает ВСЕ файлы из templates/"""
    # Для HTML - рендерим через render_template
    if filename.endswith('.html'):
        return render_template(filename)
    
    # Для остальных файлов (CSS/JS/изображения) - отдаём как статику
    return send_from_directory('templates', filename)

# Корневой маршрут
@app.route('/')
def index():
    return serve_static('index.html')

from app.api import auth_routes
from app.api import analytics
from app.api import dataset_routes

