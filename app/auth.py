from flask import request, abort, jsonify
from flask.ext.security import login_required,auth_token_required,login_user,logout_user,current_user,utils
from flask_restful import Resource

from app import db, api, user_datastore



class UserAuth(Resource):
    @login_required
    def get(self):
        return jsonify({"message": "Login as %s" % current_user.email})

    def post(self):
        parser = request.get_json()
        if parser is None:
            abort(400)
        email = parser.get('email')
        password = parser.get('password')
        if email is None or password is None:
            abort(400)
        if user_datastore.find_user(email=email) is None:
            abort(403)
        user = user_datastore.find_user(email=email)
        if user.verify_password(password) is False:
            abort(403)
        login_user(user, remember = True)
        return jsonify({"message": "Login as %s" % current_user.email})

    @login_required
    def delete(self):
        logout_user()
        return 200


api.add_resource(UserAuth, '/auth')


class UserManage(Resource):
    def post(self):
        parser = request.get_json()
        email = parser.get('email')
        password = parser.get('password')
        if email is None or password is None:
            abort(400)  # missing arguments
        user = user_datastore.create_user(email=email,password=utils.encrypt_password(password))
        login_user(user, remember = True)
        return 201

    @login_required
    def delete(self):
        parser = request.get_json()
        email = parser.get('email')
        password = parser.get('password')
        if email is None or password is None:
            abort(400)  # missing arguments
        if user_datastore.find_user(email=email) is None:
            abort(403)  # existing user
        user = user_datastore.find_user(email=email)
        user_datastore.delete_user(user)
        return 200
    @login_required
    def put(self):
        parser = request.get_json()
        password = parser.get('password')
        if password is None:
            abort(400)  # missing arguments
        user = current_user
        if user.verify_password(password) is False:
            abort(403)
        user.password = user.hash_password(password)
        db.session.update(user)
        db.session.commit()
        return 201

api.add_resource(UserManage, '/usermanage')

