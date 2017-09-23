import os
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Repos
from . import api

GIT_DIR='C:\\Windows'
REPO_PREFIX='git@github.com:/home/repositories/'

def find_all_repos(file_dir):
    pathDir = os.listdir(file_dir)
    tempNames=[]
    for reponame in pathDir:
        tempNames.append(reponame)
        print reponame
    return tempNames

@api.route('/repos/', methods=['GET'])
def get_repositories():
    page = request.args.get('page', 1, type=int)
    pagination=Repos.query.order_by(Repos.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    repos = pagination.items
    prev=None
    if pagination.has_prev:
        prev = url_for('api.get_repositories', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_repositories', page=page+1, _external=True)
    return jsonify({'names': [repo.to_json() for repo in repos], 'prev': prev,'next': next,'count': pagination.total})


@api.route('/repos/update', methods=['GET'])
def update_repositories():
    NameList=find_all_repos(GIT_DIR)
    for name in NameList:
        tempRepo=Repos(name=name, url=REPO_PREFIX+name)
        print tempRepo.name
        db.session.add(tempRepo)
        db.session.commit()
    return "Repos updated!"

@api.route('/repos/<int:id>', methods=['GET'])
def get_repo(id):
    repo=Repos.query.get_or_404(id)
    return jsonify(repo.to_json())

@api.route('/repos/', methods=['POST'])
def new_repo():
    repo=Repos.from_json(request.json)
    db.session.add(repo)
    db.session.commit()
    return jsonify(repo.to_json()), 201, {'Location': url_for('api.get_repo', id=repo.id, _external=True)}
