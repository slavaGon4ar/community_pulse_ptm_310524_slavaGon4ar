from flask import Blueprint, request, jsonify
from app import db
from app.models.questions import Category
from app.schemas.question import CategoryBase


category_bp = Blueprint('categories', __name__, url_prefix='/categories')

# Эндпоинт для создания новой категории
@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category_schema = CategoryBase(**data)
    new_category = Category(name=category_schema.name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"id": new_category.id, "name": new_category.name}), 201

# Эндпоинт для получения списка всех категорий
@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_schema = [CategoryBase.from_orm(category).dict() for category in categories]
    return jsonify(category_schema), 200

# Эндпоинт для обновления категории по ID
@category_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get_or_404(id)
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name}), 200

# Эндпоинт для удаления категории по ID
@category_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204
