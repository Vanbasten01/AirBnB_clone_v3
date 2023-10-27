#!/usr/bin/python3
'''Create a new view for User'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    '''Retrieve all users'''
    objects = [user.to_dict() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''Retrieve a user'''
    obj = User.get(user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Delete a user'''
    obj = User.get(user_id)
    if obj is None:
        abort(404)
    obj.delete()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''Create a new user'''
    if not request.is_json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    if 'email' not in body:
        abort(400, 'Missing email')
    if 'password' not in body:
        abort(400, 'Missing password')
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Update a user'''
    obj = User.get(user_id)
    if obj is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    ignored_keys = ['id', 'email', 'created_at', 'updated_at', 'password']
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(obj, key, value)
    user.save()
    return jsonify(obj.to_dict()), 200
