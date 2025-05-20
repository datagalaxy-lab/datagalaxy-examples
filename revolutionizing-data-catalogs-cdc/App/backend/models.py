from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for the many-to-many relationship between CatalogItem and Tag
catalog_item_tags = db.Table(
    'catalog_item_tags',
    db.Column('catalog_item_id', db.Integer, db.ForeignKey('catalog_item.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # One-to-many: One Category has many CatalogItems
    items = db.relationship('CatalogItem', back_populates='category')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-many: A Tag can belong to many CatalogItems
    items = db.relationship('CatalogItem', secondary=catalog_item_tags, back_populates='tags')

class CatalogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Relationship to Category (one-to-many)
    category = db.relationship('Category', back_populates='items')
    # Relationship to Tag (many-to-many)
    tags = db.relationship('Tag', secondary=catalog_item_tags, back_populates='items')
