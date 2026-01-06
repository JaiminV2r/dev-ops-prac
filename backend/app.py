from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# MongoDB connection
try:
    client = MongoClient(app.config['MONGODB_URI'], serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    db = client[app.config['DATABASE_NAME']]
    users_collection = db[app.config['COLLECTION_NAME']]
    print("✓ Successfully connected to MongoDB!")
except ConnectionFailure as e:
    print(f"✗ Failed to connect to MongoDB: {e}")
    db = None
    users_collection = None

# Frontend directory path
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')


@app.route('/')
def index():
    """Serve the main index.html page"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/success')
def success():
    """Serve the success page"""
    return send_from_directory(FRONTEND_DIR, 'success.html')


@app.route('/styles.css')
def styles():
    """Serve the CSS file"""
    return send_from_directory(FRONTEND_DIR, 'styles.css')


@app.route('/api', methods=['GET'])
def get_users():
    """
    Fetch all users from MongoDB users collection and return as JSON list
    """
    try:
        if users_collection is None:
            return jsonify({
                'error': 'Database connection not available',
                'data': []
            }), 500
        
        # Fetch all users from the collection
        users = list(users_collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
        
        return jsonify({
            'success': True,
            'count': len(users),
            'data': users
        }), 200
        
    except PyMongoError as e:
        return jsonify({
            'error': f'Database error: {str(e)}',
            'data': []
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'data': []
        }), 500


@app.route('/submit', methods=['POST'])
def submit_user():
    """
    Handle user registration form submission.
    Expects JSON data with name, email, and password fields.
    """
    try:
        if users_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not available'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validate fields
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        if not password:
            return jsonify({
                'success': False,
                'error': 'Password is required'
            }), 400
        
        # Check if email already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 400
        
        # Create user document
        user_data = {
            'name': name,
            'email': email,
            'password': password  # Note: In production, you should hash passwords!
        }
        
        # Insert into MongoDB
        result = users_collection.insert_one(user_data)
        
        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'User registered successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to insert user'
            }), 500
            
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
