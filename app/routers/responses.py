from flask import Blueprint, jsonify, request  # Импортируем необходимые модули из Flask

from app.models.questions import Questions, Statistics  # Импортируем модели Questions и Statistics
from app.models.responses import Responses  # Импортируем модель Responses

from app import db  # Импортируем экземпляр базы данных

# Создаем Blueprint для управления маршрутом ответа
response_bp = Blueprint('response', __name__, url_prefix='/response')



# Определяем маршрут для получения всех ответов
@response_bp.route('/')
def get_all_responses():
    return "ALL RESPONSES"  # Возвращаем строку с сообщением о всех ответах

# # Определяем маршрут для добавления нового ответа
# @response_bp.route('/add', methods=['POST'])
# def add_new_responses():
#     return "RESPONSE IS ADDED"  # Возвращаем строку с сообщением о добавлении ответа

# Определяем маршрут для добавления нового ответа с обновлением статистики
@response_bp.route('/add', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос с обновлением статистики."""
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'message': "Некорректные данные"}), 400  # Если данные некорректные, возвращаем ошибку 400

    question = Questions.query.get(data['question_id'])  # Ищем вопрос по question_id
    if not question:
        return jsonify({'message': "Вопрос не найден"}), 404  # Если вопрос не найден, возвращаем ошибку 404

    # Создаем новый ответ
    response = Responses(
        question_id=question.id,  # Указываем id вопроса
        is_agree=data['is_agree']  # Указываем, согласен ли пользователь с вопросом
    )
    db.session.add(response)  # Добавляем ответ в сессию базы данных

    # Обновление статистики
    statistic = Statistics.query.filter_by(question_id=question.id).first()  # Ищем статистику для данного вопроса
    if not statistic:  # Если статистики нет, создаем новую
        statistic = Statistics(question_id=question.id, agree_count=0, disagree_count=0)
        db.session.add(statistic)  # Добавляем статистику в сессию базы данных

    # Обновляем счетчики согласия и несогласия
    if data['is_agree']:
        statistic.agree_count += 1  # Увеличиваем счетчик согласия
    else:
        statistic.disagree_count += 1  # Увеличиваем счетчик несогласия

    db.session.commit()  # Сохраняем изменения в базе данных

    return jsonify({'message': f"Ответ на вопрос {question.id} добавлен"}), 201  # Возвращаем сообщение об успешном добавлении ответа
