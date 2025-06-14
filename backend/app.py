from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql+psycopg2://catalog_user:catalog_pass@localhost/catalog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Token blocklist
jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blocklist

# Models
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema": os.getenv('DB_SCHEMA', 'catalog')}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    products = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {"schema": os.getenv('DB_SCHEMA', 'catalog')}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DB_SCHEMA', 'catalog')}.users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# Authentication routes
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Username or email already exists"}), 409
    
    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Invalid username or password"}), 401
    
    # Convert user.id to string for JWT identity
    access_token = create_access_token(identity=str(user.id))
    
    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }
    return jsonify({"access_token": access_token, "user": user_info}), 200

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

# Product routes
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route("/products/user", methods=["GET"])
@jwt_required()
def get_user_products():
    # Convert string identity back to integer for database query
    user_id = int(get_jwt_identity())
    products = Product.query.filter_by(user_id=user_id).all()
    return jsonify([product.to_dict() for product in products])

@app.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    # Convert string identity back to integer for database query
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"message": "Missing required fields"}), 400
    
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=float(data['price']),
        user_id=user_id
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify(new_product.to_dict()), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    # Convert string identity back to integer for database query
    user_id = int(get_jwt_identity())
    product = Product.query.get_or_404(product_id)
    
    # Check if user owns the product
    if product.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    
    db.session.commit()
    
    return jsonify(product.to_dict())

@app.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    # Convert string identity back to integer for database query
    user_id = int(get_jwt_identity())
    product = Product.query.get_or_404(product_id)
    
    # Check if user owns the product
    if product.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Product deleted successfully"})

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Add sample data if database is empty
        if User.query.count() == 0:
            # Create a test user
            hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')
            test_user = User(username="testuser", email="test@example.com", password_hash=hashed_password)
            db.session.add(test_user)
            db.session.commit()
            
            # Create sample products
            if Product.query.count() == 0:
                product1 = Product(name='Laptop', description='A high-end laptop', price=1200.00, user_id=test_user.id)
                product2 = Product(name='Phone', description='Latest smartphone', price=800.00, user_id=test_user.id)
                db.session.add(product1)
                db.session.add(product2)
                db.session.commit()
    
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host=host, port=port)