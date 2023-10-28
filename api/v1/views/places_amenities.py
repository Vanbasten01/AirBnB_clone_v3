#!/usr/bin/python3
'''Create a new view for the link between Place objects and Amenity objects'''
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False
        )
def get_places_amenities(place_id):
    '''Retrieve all amenities'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_amenity = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(all_amenity)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False
        )
def delete_places_amenities(place_id, amenity_id):
    '''Delete an amenity'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False
        )
def post_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
