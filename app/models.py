#-*- coding: utf-8 -*-
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from flask import current_app, request, url_for
from . import db
import json

def is_json(myjson):
    if isinstance(myjson, str):  # 首先判断变量是否为字符串
        try:
            json.loads(myjson, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False

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
        print "json_repo:%s" % json_repo
        if json_repo is None:
            return "bad request"
        name = json_repo.get('name')
        #print name
        url = json_repo.get('url')
        description = json_repo.get('description')
        author = json_repo.get('author')
        return Repos(name=name, url=url, description=description, author=author)


