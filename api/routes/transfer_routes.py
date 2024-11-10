from flask import Blueprint, request, jsonify
from models.transfer import Transfer
from db import db

transfer_bp = Blueprint("transfer", __name__, url_prefix="/transfers")


@transfer_bp.route("/", methods=["POST"])
def create_transfer():
    data = request.get_json()
    session = db.session
    new_transfer = Transfer(**data)
    session.add(new_transfer)
    session.commit()
    return jsonify({"message": "Transfer created", "trid": new_transfer.trid}), 201

@transfer_bp.route("/<int:trid>", methods=["GET"])
def get_transfer(trid):
    session = db.session
    transfer = session.query(Transfer).get(trid)
    if not transfer:
        return jsonify({"message": "Transfer not found"}), 404
    return jsonify({
        "trid": transfer.trid,
        "sender_id": transfer.sender_id,
        "recipient_id": transfer.recipient_id,
        "amount": transfer.amount,
        "date": transfer.date
    })

@transfer_bp.route("/<int:trid>", methods=["PUT"])
def update_transfer(trid):
    session = db.session
    transfer = session.query(Transfer).get(trid)
    if not transfer:
        return jsonify({"message": "Transfer not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(transfer, key, value)
    session.commit()
    return jsonify({"message": "Transfer updated"})

@transfer_bp.route("/<int:trid>", methods=["DELETE"])
def delete_transfer(trid):
    session = db.session
    transfer = session.query(Transfer).get(trid)
    if not transfer:
        return jsonify({"message": "Transfer not found"}), 404
    session.delete(transfer)
    session.commit()
    return jsonify({"message": "Transfer deleted"})
