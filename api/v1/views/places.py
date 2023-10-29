#!/usr/bin/python3
"""  a new view for Place objects that handles CRUD """
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route("/cities/<id>/places", methods=["GET"], strict_slashes=False)
def all_places(id):
    """Retrieves all places"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place by its id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<plc_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(plc_id):
    """Deletes a place by its id"""
    place = storage.get(Place, plc_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<id>/places", methods=["POST"], strict_slashes=False)
def create_place(id):
    """Creates a place within a specific city"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    data["city_id"] = id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """Retrieve all Place objects depending of the JSON
    in the body of the request"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    states = body.get('states', [])
    cities = body.get('cities', [])
    amenities = body.get('amenities', [])
    all_places = [obj for obj in storage.all(Place).values()]
    places = []
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            places.extend(state.places)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.extend(city.places)
    if amenities:
        ameni_ties = set(amenities)
        places = [
                place for place in places if ameni_ties.issubset(
                    place.amenity_ids
                    )
                ]
    res = [place.to_dict() for place in places]
    return jsonify(res)
