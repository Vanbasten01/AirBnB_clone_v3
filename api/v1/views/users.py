#!/usr/bin/python3
'''Create a new view for User'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    '''Retrieve all users'''
    objects = [user.to_dict() for user in storage.all(User).values()]
    for objt in objects:
        if 'places' in objt:
            del objects['places']
        if 'reviews' in objt:
            del objects['reviews']
    return jsonify(objects)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''Retrieve a user'''
    obj = storage.get(User, user_id)
    if obj is None:
        return jsonify(error='Not found'), 404
    ob_user = obj.to_dict()
    if 'places' in ob_user:
        del ob_user['places']
    if 'reviews' in ob_user:
        del ob_user['reviews']
    return jsonify(ob_user)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Delete a user'''
    obj = storage.get(User, user_id)
    if obj is None:
        return jsonify(error='Not found'), 404
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''Create a new user'''
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400
    body = request.get_json()
    if 'email' not in body:
        return jsonify(error='Missing email'), 400
    if 'password' not in body:
        return jsonify(error='Missing password'), 400
    new_user = User(**body)
    new_user.save()
    ob_user = new_user.to_dict()
    if 'places' in ob_user:
        del ob_user['places']
    if 'reviews' in ob_user:
        del ob_user['reviews']
    return jsonify(ob_user), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Update a user'''
    obj = storage.get(User, user_id)
    if obj is None:
        return jsonify(error='Not found'), 404
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400
    body = request.get_json()
    ignored_keys = ['id', 'email', 'created_at', 'updated_at', 'password']
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(obj, key, value)
    obj.save()
    ob_user = obj.to_dict()
    if 'places' in ob_user:
        del ob_user['places']
    if 'reviews' in ob_user:
        del ob_user['reviews']
    return jsonify(ob_user), 200
