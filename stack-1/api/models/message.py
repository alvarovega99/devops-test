from mongoengine import Document, StringField, ReferenceField
from models.users import User

class Message(Document):
    content = StringField()
    user = ReferenceField(User)
