from flask import Blueprint, jsonify, request, make_response
from app.models.questions import Questions, Category  # Импортируем модели Questions и Category
from app import db
from app.schemas.question import QuestionCreate, QuestionResponse, CategoryBase  # Импортируем схемы для сериализации и валидации

# Создаем Blueprint для вопросов с префиксом '/questions'
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_all_questions():
    """Получение всех вопросов с информацией о категориях"""
    questions = Questions.query.all()
    questions_data = [
        {
            'id': question.id,
            'text': question.text,
            'created_at': question.created_at,
            'category': {
                'id': question.category.id,
                'name': question.category.name
            } if question.category else None
        }
        for question in questions
    ]
    return make_response(jsonify(questions_data), 200)


@questions_bp.route('/add', methods=['POST'])
def add_new_question():
    """Добавление нового вопроса с указанием категории"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'message': 'NO DATA PROVIDED'}), 400

    question_data = QuestionCreate(**data)  # Используем схему для валидации данных
    category = Category.query.get(question_data.category_id) if question_data.category_id else None

    question = Questions(text=question_data.text, category=category)
    db.session.add(question)
    db.session.commit()

    return jsonify({
        "message": "NEW QUESTION added",
        "question_id": question.id
    }), 201


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление вопроса по ID с поддержкой категории"""
    question = Questions.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if category:
            question.category = category
        else:
            return jsonify({'message': 'Указанная категория не найдена'}), 404

    db.session.commit()
    return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление вопроса по его ID"""
    question = Questions.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200
