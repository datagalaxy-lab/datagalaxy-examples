import os
from flask import Flask, request, jsonify, abort
from models import db, CatalogItem, Category, Tag
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so the React app can access the API

# Use environment variable or default settings (note: "db" is the name of the Postgres service in docker-compose)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'postgresql://postgres:postgres@db:5432/catalogdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ----------------------------
# CatalogItem Endpoints
# ----------------------------

@app.route('/api/items', methods=['GET'])
def get_items():
    items = CatalogItem.query.all()
    items_list = []
    for item in items:
        items_list.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'category': {'id': item.category.id, 'name': item.category.name} if item.category else None,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in item.tags]
        })
    return jsonify(items_list)

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Name is required")
    name = data['name']
    description = data.get('description', '')
    category_id = data.get('category_id')
    tag_ids = data.get('tag_ids', [])

    new_item = CatalogItem(name=name, description=description)
    if category_id:
        category = Category.query.get(category_id)
        if category:
            new_item.category = category
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_item.tags = tags

    db.session.add(new_item)
    db.session.commit()
    return jsonify({
        'id': new_item.id, 
        'name': new_item.name, 
        'description': new_item.description,
        'category': {'id': new_item.category.id, 'name': new_item.category.name} if new_item.category else None,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in new_item.tags]
    }), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = CatalogItem.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'category': {'id': item.category.id, 'name': item.category.name} if item.category else None,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in item.tags]
    })

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = CatalogItem.query.get_or_404(item_id)
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Name is required")
    
    item.name = data.get('name')
    item.description = data.get('description', '')
    category_id = data.get('category_id')
    tag_ids = data.get('tag_ids', [])

    if category_id:
        category = Category.query.get(category_id)
        item.category = category
    else:
        item.category = None

    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        item.tags = tags
    else:
        item.tags = []

    db.session.commit()
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'category': {'id': item.category.id, 'name': item.category.name} if item.category else None,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in item.tags]
    })

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = CatalogItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

# ----------------------------
# Category Endpoints
# ----------------------------

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    data = [{'id': cat.id, 'name': cat.name, 'description': cat.description} for cat in categories]
    return jsonify(data)

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Name is required for category")
    category = Category(name=data['name'], description=data.get('description', ''))
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name, 'description': category.description}), 201

# ----------------------------
# Tag Endpoints
# ----------------------------

@app.route('/api/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    data = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify(data)

@app.route('/api/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Name is required for tag")
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify({'id': tag.id, 'name': tag.name}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
