from app import db  # Импортируем объект базы данных db из модуля community_app


class Responses(db.Model):  # Определяем класс Responses, который представляет модель ответов в базе данных
    __tablename__ = 'responses'  # Указываем имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Определяем колонку id как первичный ключ типа Integer
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)  # Определяем колонку question_id как внешний ключ, ссылающийся на id вопроса, и не может быть пустой
    is_agree = db.Column(db.Boolean, nullable=False)  # Определяем колонку is_agree для хранения значения согласия (True или False) и не может быть пустой

    def __str__(self):  # Метод для строкового представления объекта Responses
        return f'Questions_id: {self.question_id}, Answer: {self.is_agree}'  # Возвращаем строку с id вопроса и ответом
