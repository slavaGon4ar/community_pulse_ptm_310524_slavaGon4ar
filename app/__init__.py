from flask import Flask
import os
import dotenv
from config import DevelopmentConfig, TestingConfig, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Импортируем маршруты из других модулей
from app.routers.questions import questions_bp  # Импортируем Blueprint для вопросов.
from app.routers.responses import response_bp  # Импортируем Blueprint для ответов.
from app.routers.categories import category_bp # Импортируем Blueprint для категорий.
from app.routers.home import home_bp  # Импортируем Blueprint для главной страницы.



dotenv.load_dotenv()  # Загружаем переменные окружения из файла .env
config_name = os.getenv('FLASK_ENV')  # Получаем значение переменной окружения 'FLASK_ENV'

# Устанавливаем конфигурацию приложения в зависимости от значения переменной окружения
config_set_up = {
    'production': Config,  # Конфигурация для рабочего окружения
    'development': DevelopmentConfig,  # Конфигурация для разработки
    'testing': TestingConfig,  # Конфигурация для тестирования
}.get(config_name)  # Получаем соответствующий класс конфигурации на основе значения config_name


def create_app():  # Определяем функцию для создания экземпляра приложения Flask

    app = Flask(__name__)  # Создаем экземпляр приложения Flask
    app.config.from_object(config_set_up)  # Загружаем конфигурацию приложения из объекта config_set_up
    db.init_app(app)  # Инициализируем объект базы данных с приложением
    migrate.init_app(app, db)  # Инициализируем миграции с приложением и объектом базы данных

    app.register_blueprint(home_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)
    app.register_blueprint(category_bp)

    return app
