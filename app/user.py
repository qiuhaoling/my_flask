from flask import request, abort
from flask_login import login_user, logout_user, login_required
from flask_restful import Resource

from app import db, api, login_manager
from app.model import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(id))


class UserAuth(Resource):
    @login_required
    def get(self):
        return 202

    def post(self):
        logout_user()
        parser = request.get_json()
        if parser is None:
            abort(400)
        username = parser.get('username')
        password = parser.get('password')
        if username is None or password is None:
            abort(400)
        if User.query.filter_by(username=username).first() is None:
            abort(403)
        user = User.query.filter_by(username=username).first()
        if user.verify_password(password) is False:
            abort(403)
        login_user(user, True)
        return 202

    def delete(self):
        logout_user()
        return 205


api.add_resource(UserAuth, '/auth')


class UserManage(Resource):
    def post(self):
        parser = request.get_json()
        username = parser.get('username')
        password = parser.get('password')
        email = parser.get('email')
        if username is None or password is None or email is None:
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(403)  # existing user
        user = User.query.filter_by(username=username).first()
        user.hash_password(password)
        user.email = email
        db.session.add(user)
        db.session.commit()
        login_user(user=user, remember=True)
        return 201

    @login_required
    def delete(self):
        parser = request.get_json()
        username = parser.get('username')
        password = parser.get('password')
        if username is None or password is None:
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is None:
            abort(403)  # existing user
        user = User.query.filter_by(username=username).first()
        db.session.remove(user)
        db.session.commit()
        return 200

    def put(self):
        parser = request.get_json()
        username = parser.get('username')
        password = parser.get('password')
        email = parser.get('email')
        if username is None or password is None or email is None:
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is None:
            abort(400)  # existing user
        user = User.query.filter_by(username=username).first()
        user.hash_password(password)
        user.email = email
        db.session.update(user)
        db.session.commit()
        login_user(user=user, remember=True)


api.add_resource(UserManage, '/usermanage')
