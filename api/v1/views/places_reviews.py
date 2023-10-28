#!/usr/bin/python3
"""the places_reviews view for the API"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_reviews(place_id):
    """ """
    place = storage.get(Place, place_id)
    if place:
        review_list = [review.to_dict() for review in place.reviews]
        return jsonify(review_list)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def new_review(place_id):
    """ """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    body = request.get_json()
    if "user_id" not in body:
        abort(400, "Missing user_id")
    user_id = body["user_id"]
    if storage.get(User, user_id) is None:
        abort(404)
    if "text" not in body:
        abort(400, "Missing text")
    body["place_id"] = place_id
    new_review = Review(**body)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    body = request.get_json()
    ignored_keys = ["id", "user_id", "place_id" "created_at", "updated_at"]
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
