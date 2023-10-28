#!/usr/bin/python3
'''Create a new view for Review'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<place_id>.reviews', methods=['GET'], strict_slashes=False
        )
def reviews(place_id):
    '''Retrieve all reviews'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    rev = [review.to_dict() for review in place.reviews]
    return jsonify(rev)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''Retrieve a review'''
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_review(review_id):
    '''Delete a review'''
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False
        )
def post_review(place_id):
    '''Create a review'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    ob_user = storage.get(User, body['user_id'])
    if ob_user is None:
        abort(404)
    if 'text' not in body:
        abort(400, 'Missing text')
    body['place_id'] = place_id
    new_rev = Review(**body)
    new_rev.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update(review_id):
    '''Update a review'''
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
