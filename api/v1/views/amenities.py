#!/usr/bin/python3
""" amenity api """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenitties():
    """ """
    objects = storage.all(Amenity).values()
    all_obj = []
    for obj in objects:
        all_obj.append(obj.to_dict())
    return jsonify(all_obj)


@app_views.route('/amenities/<ame_id>', methods=['GET'], strict_slashes=False)
def get_amenity(ame_id):
    """ """
    obj = storage.get(Amenity, ame_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ """
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ """
    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()
    if not body.get("name"):
        abort(400, "Missing name")
    new_amenity = Amenity(**body)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<ame_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(ame_id):
    """ """
    obj = storage.get(Amenity, ame_id)
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
    return jsonify(obj.to_dict()), 200
