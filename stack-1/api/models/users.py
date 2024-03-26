from mongoengine import Document, StringField, ReferenceField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
