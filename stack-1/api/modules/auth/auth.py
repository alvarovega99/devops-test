from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.users import User
from modules.logs.graylog_logger import GraylogLogger

class AuthAPI:
    def __init__(self, app):
        self.app = app
        self.graylog_connection = GraylogLogger()

        @app.route('/register', methods=['POST'])
        def register():
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return jsonify({'error': 'Username and password are required'}), 400

                if User.objects(username=username):
                    return jsonify({'error': 'Username already exists'}), 400

                hashed_password = generate_password_hash(password)
                print(hashed_password)
                new_user = User(username=username, password=hashed_password)
                print(new_user)
                new_user.save()

                self.graylog_connection.log('New user registered: {}'.format(username))

                return jsonify({'message': 'User registered successfully'}), 201
            except Exception as e:
                self.graylog_connection.log('Error in register endpoint: {}'.format(str(e)))
                return jsonify({'error': 'Internal Server Error'}), 500
            
        @app.route('/login', methods=['POST'])
        def login():
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                user = User.objects(username=username).first()

                if not user or not check_password_hash(user.password, password):
                    self.graylog_connection.log('Failed login attempt for user: {}'.format(username))
                    return jsonify({'error': 'Invalid username or password'}), 401
                
                self.graylog_connection.log('New user login: {}'.format(username))
                access_token = create_access_token(identity=str(user.id))
                return jsonify({'access_token': access_token}), 200
            except Exception as e:
                self.graylog_connection.log('Error in login endpoint: {}'.format(str(e)))
                return jsonify({'error': 'Internal Server Error'}), 500
