from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flasgger import Swagger
from modules.auth.auth import AuthAPI
from modules.messages.messages import MessagesAPI

app = Flask(__name__)
app.config.from_pyfile('config.py')

CORS(app)

app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}

swagger = Swagger(app, template_file='config/swagger_conf.yml')

db = MongoEngine(app)

jwt = JWTManager(app)

auth_api = AuthAPI(app)
messages_api = MessagesAPI(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
