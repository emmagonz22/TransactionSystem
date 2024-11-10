from flask import Blueprint, request, jsonify
from models.promotion import Promotion
from db import db

promotion_bp = Blueprint("promotion", __name__, url_prefix="/promotions")


@promotion_bp.route("/", methods=["POST"])
def create_promotion():
    data = request.get_json()
    session = db.session
    new_promotion = Promotion(**data)
    session.add(new_promotion)
    session.commit()
    return jsonify({"message": "Promotion created", "prid": new_promotion.prid}), 201

@promotion_bp.route("/<int:prid>", methods=["GET"])
def get_promotion(prid):
    session = db.session
    promotion = session.query(Promotion).get(prid)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404
    return jsonify({
        "prid": promotion.prid,
        "client_email": promotion.client_email,
        "telephone": promotion.telephone,
        "promotion": promotion.promotion,
        "responded": promotion.responded
    })

@promotion_bp.route("/<int:prid>", methods=["PUT"])
def update_promotion(prid):
    session = db.session
    promotion = session.query(Promotion).get(prid)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(promotion, key, value)
    session.commit()
    return jsonify({"message": "Promotion updated"})

@promotion_bp.route("/<int:prid>", methods=["DELETE"])
def delete_promotion(prid):
    session = db.session
    promotion = session.query(Promotion).get(prid)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404
    session.delete(promotion)
    session.commit()
    return jsonify({"message": "Promotion deleted"})
