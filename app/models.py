from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from flask import current_app, request, url_for
from . import db

class Repos(db.Model):
    __tablename__='repositories'
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.VARCHAR(20))
    url=db.Column(db.VARCHAR(100))
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description=db.Column(db.Text)
    author=db.Column(db.VARCHAR(20))

    def to_json(self):
        json_repos = {
            'name': self.name,
            'url': self.url,
            'author': self.author,
            'timestamp': self.timestamp,
            'description': self.description
        }
        return json_repos

    @staticmethod
    def from_json(json_repo):
        name= json_repo.get('name')
        url=json_repo.get('url')
        description = json_repo.get('description')
        author = json_repo.get('author')
        return Repos(name=name, url=url, description=description, author=author)
