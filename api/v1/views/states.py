#!/usr/bin/python3
"""api states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ """
    objects = storage.all(State).values()
    all_obj = []
    for obj in objects:
        all_obj.append(obj.to_dict())
    return jsonify(all_obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ """
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ """
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ """
    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()
    if not body.get("name"):
        abort(400, "Missing name")
    new_state = State(**body)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    body = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
