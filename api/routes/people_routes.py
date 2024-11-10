from flask import Blueprint, request, jsonify
from models.people import People
from db import db

people_bp = Blueprint("people", __name__, url_prefix="/people")

@people_bp.route("/", methods=["POST"])
def create_people():
    data = request.get_json()
    session = db.session
    new_people = People(**data)
    session.add(new_people)
    session.commit()
    return jsonify({"message": "People created", "pid" : new_people.pid}), 201

@people_bp.route("/<int:pid>", methods=["GET"])
def get_people(pid):
    session = db.session
    people = session.query(People).get(pid)
    if not people:
        return jsonify({"message": "People not found"}), 404
    return jsonify({
        "pid": people.pid,
        "first_name": people.first_name,
        "last_name": people.last_name,
        "telephone": people.telephone,
        "email": people.email,
        "city": people.city,
        "country": people.country,
        "android": people.android,
        "ios": people.ios,
        "desktop": people.desktop,
    })

@people_bp.route("/<int:pid>", methods=["PUT"])
def update_people(pid):
    session = db.session
    people = session.query(People).get(pid)
    if not people:
        return jsonify({"message": "People not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(people, key, value)
    session.commit()
    return jsonify({"message": "People updated"})

@people_bp.route("/<int:pid>", methods=["DELETE"])
def delete_people(pid):
    session = db.session
    people = session.query(People).get(pid)
    if not people:
        return jsonify({"message": "People not found"}), 404
    session.delete(people)
    session.commit()
    return jsonify({"message": "People deleted"})
