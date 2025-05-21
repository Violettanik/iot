import os
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask
from app.models import db, User, Role, AccessLevel

# Создаем временное приложение
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.dirname(__file__), 'instance', 'mydatabase.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False# Инициализируем базу данных
db.init_app(app)

def initialize_database():
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        from flask_security import SQLAlchemyUserDatastore
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        
        # Создаем стандартные роли
        if not user_datastore.find_role('admin'):
            user_datastore.create_role(name='admin', description='Administrator')
            user_datastore.create_role(name='user', description='Regular user')
            db.session.commit()
        
        print("✅ Database tables created successfully!")
        
        # Проверяем структуру таблицы user
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = inspector.get_columns('user')
        print("Columns in 'user' table:")
        for col in columns:
            print(f"- {col['name']}: {col['type']}")

if __name__ == '__main__':
    # Создаем папку instance если ее нет
    os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)
    
    # Инициализируем БД
    initialize_database()
