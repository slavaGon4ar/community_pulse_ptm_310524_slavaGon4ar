class Config:  # Определяем базовый класс конфигурации
    DEBUG = False  # Устанавливаем режим отладки в False (выключен)
    TESTING = False  # Устанавливаем режим тестирования в False (выключен)
    # SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:example')  # Пример URI для базы данных SQLite в памяти (закомментировано)
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:parhat1994@localhost:3306/Community_pulse'  # Пример URI для подключения к MySQL (закомментировано)
    SQLALCHEMY_DATABASE_URI = ("sqlite:////Users/slavagon4ar/PycharmProjects/community_pulse/community_pulse_new/community_pulse_ptm_310524_slavaGon4ar/ptm-310524-slavaGon4ar.db")  # URI для
    # подключения к базе данных SQLite по указанному пути

class DevelopmentConfig(Config):  # Класс конфигурации для разработки, наследует от Config
    DEBUG = True  # Включаем режим отладки

class TestingConfig(Config):  # Класс конфигурации для тестирования, наследует от Config
    DEBUG = True  # Включаем режим отладки
    TESTING = True  # Включаем режим тестирования