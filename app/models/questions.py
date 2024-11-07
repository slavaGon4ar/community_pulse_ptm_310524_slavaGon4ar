from app import db  # Импортируем объект базы данных db из модуля Community_pulse
from datetime import datetime  # Импортируем класс datetime для работы с датой и временем

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    questions = db.relationship('Questions', backref='category', lazy=True)

    def __str__(self):
        return f'Category: {self.name}'

class Questions(db.Model):  # Определяем класс Questions, который представляет модель вопросов в базе данных
    __tablename__ = 'questions'  # Указываем имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Определяем колонку id как первичный ключ типа Integer
    text = db.Column(db.String(255), nullable=False)  # Определяем колонку text, которая хранит строку до 255 символов и не может быть пустой
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Определяем колонку created_at, которая хранит дату и время создания вопроса (по умолчанию текущее время)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    responses = db.relationship('Responses', backref='question', lazy=True)  # Устанавливаем связь с моделью Responses, позволяя получать ответы на вопрос

    def __str__(self):  # Метод для строкового представления объекта Questions
        return f'Questions: {self.text}'  # Возвращаем строку с текстом вопроса


class Statistics(db.Model):  # Определяем класс Statistics, который представляет модель статистики в базе данных
    __tablename__ = 'statistics'  # Указываем имя таблицы в базе данных
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)  # Определяем колонку question_id как внешний ключ, ссылающийся на id вопроса, и делаем его первичным ключом
    agree_count = db.Column(db.Integer, nullable=False, default=0)  # Определяем колонку agree_count для хранения количества согласий (по умолчанию 0) и не может быть пустой
    disagree_count = db.Column(db.Integer, nullable=False, default=0)  # Определяем колонку disagree_count для хранения количества несогласий (по умолчанию 0) и не может быть пустой

    def __str__(self):  # Метод для строкового представления объекта Statistics
        return f'Statistics for question # {self.question_id}: agreed: {self.agree_count}, disagreed: {self.disagree_count}'  # Возвращаем строку с данными о статистике для конкретного вопроса