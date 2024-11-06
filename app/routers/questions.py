from flask import Blueprint, jsonify, request, make_response  # Импортируем необходимые модули из Flask
from app.models.questions import Questions  # Импортируем модель Questions из модуля models
from app import db  # Импортируем объект базы данных db из модуля community_app

# Создаем новый Blueprint для обработки вопросов с префиксом URL '/questions'
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])  # Определяем маршрут для получения всех вопросов
def get_all_questions():
    questions: list[Questions] = Questions.query.all()  # Получаем все вопросы из базы данных
    questions_data: list[dict] = [  # Формируем список словарей с данными вопросов
        {
            'id': question.id,  # Добавляем ID вопроса
            'text': question.text,  # Добавляем текст вопроса
            'created_at': question.created_at  # Добавляем дату создания вопроса
        }
        for question in questions]  # Перебираем все вопросы
    response = make_response(jsonify(questions_data), 200)  # Формируем ответ в формате JSON с кодом 200
    # response.headers["Custom-Header"] = "our custom header"  # Закомментированный пример добавления пользовательского заголовка

    return response  # Возвращаем ответ


@questions_bp.route('/add', methods=['POST'])  # Определяем маршрут для добавления нового вопроса
def add_new_questions():
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    if not data or 'text' not in data:  # Проверяем, что данные предоставлены и содержат текст вопроса
        return jsonify(  # Возвращаем ошибку, если данные отсутствуют
            {
                'message': 'NO DATA PROVIDED'  # Сообщение об ошибке
            }
        ), 400  # Код ошибки 400 (Bad Request)

    question: Questions = Questions(text=data['text'])  # Создаем новый объект Questions с текстом из запроса
    db.session.add(question)  # Добавляем новый вопрос в сессию базы данных
    db.session.commit()  # Сохраняем изменения в базе данных

    return jsonify(  # Возвращаем успешный ответ
        {
            "message": "NEW QUESTION added",  # Сообщение об успешном добавлении
            "question_id": question.id  # ID нового вопроса
        }
    ), 201  # Код успеха 201 (Created)


@questions_bp.route('/<int:id>', methods=['PUT'])  # Определяем маршрут для обновления вопроса по его ID
def update_question(id):
    """Обновление конкретного вопроса по его ID."""
    question = Questions.query.get(id)  # Получаем вопрос из базы данных по ID
    if question is None:  # Проверяем, существует ли вопрос
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404  # Возвращаем ошибку, если вопрос не найден

    data = request.get_json()  # Получаем данные из запроса в формате JSON
    if 'text' in data:  # Проверяем, предоставлен ли текст вопроса
        question.text = data['text']  # Обновляем текст вопроса
        db.session.commit()  # Сохраняем изменения в базе данных
        return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200  # Возвращаем успешный ответ
    else:
        return jsonify(
            {'message': "Текст вопроса не предоставлен"}), 400  # Возвращаем ошибку, если текст не предоставлен


@questions_bp.route('/<int:id>', methods=['DELETE'])  # Определяем маршрут для удаления вопроса по его ID
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    question = Questions.query.get(id)  # Получаем вопрос из базы данных по ID
    if question is None:  # Проверяем, существует ли вопрос
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404  # Возвращаем ошибку, если вопрос не найден

    db.session.delete(question)  # Удаляем вопрос из сессии базы данных
    db.session.commit()  # Сохраняем изменения в базе данных
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200  # Возвращаем успешный ответ
