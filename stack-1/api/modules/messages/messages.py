from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import Message
from modules.logs.graylog_logger import GraylogLogger

class MessagesAPI:
    def __init__(self, app):
        self.app = app
        self.graylog_connection = GraylogLogger()

        @app.route("/messages/", methods=["GET"])
        @jwt_required()
        def get_messages():
            messages = Message.objects()
            formatted_messages = [{'id': str(message.id), 'content': message.content, 'user_id': str(message.user.id)} for message in messages]
            self.graylog_connection.log('Messages retrieved successfully')
            return jsonify(formatted_messages)

        @app.route("/messages/", methods=["POST"])
        @jwt_required()
        def create_message():
            current_user_id = get_jwt_identity()
            user_id = str(current_user_id)
            data = request.get_json()
            content = data.get('content')

            if not content:
                return jsonify({'error': 'Content is required'}), 400

            new_message = Message(content=content, user=user_id)
            new_message.save()

            self.graylog_connection.log('New message created by user: {}'.format(user_id))

            return jsonify({'message': 'Message created successfully'}), 201
