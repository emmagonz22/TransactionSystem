from flask import Blueprint, request, jsonify
from models.transfer import Transfer
from db import db
from sqlalchemy import func, desc, extract

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



@transfer_bp.route("/amount-over-time", methods=["GET"])
def get_transfer_amount_over_time():
    session = db.session
    # total amount of transfer overtime
    transfer_over_time = (
        session.query(
            Transfer.date,
            func.sum(Transfer.amount).label("total_amount")
        )
        .group_by(Transfer.date)
        .order_by(Transfer.date)
        .all()
    )

    # returns the json
    results = [
        {"date": record.date, "total_amount": record.total_amount} for record in transfer_over_time
    ]
    print(results)
    return jsonify(results), 200


@transfer_bp.route("/quantity-over-time", methods=["GET"])
def get_transfer_quantity_over_time():
    session = db.session
    # get the quantity of transfer over time in terms of years
    transfer_quantity_over_time = (
        session.query(
            Transfer.date,
            func.count(Transfer.trid).label("transfer_count"),
            extract('year', Transfer.date).label("year")
        )
        .group_by(Transfer.date, "year")
        .order_by(Transfer.date)
        .all()
    )

    # return in format json
    results = [
        {"date": record.date, "year": record.year, "transfer_count": record.transfer_count} for record in transfer_quantity_over_time
    ]
    

    return jsonify(results), 200


@transfer_bp.route("/top-senders", methods=["GET"])
def top_senders():
    session = db.session
    # get top 5 senders by transfer amount
    top_five_senders = (
        session.query(Transfer.sender_id, func.sum(Transfer.amount).label("total_sent"))
        .group_by(Transfer.sender_id)
        .order_by(desc("total_sent"))
        .limit(5)
        .all()
    )
    
    #format in json format
    results = [
        {
            "sender_id": sender.sender_id,
            "total_sent": float(sender.total_sent)
        }
        for sender in top_five_senders
    ]


    return jsonify(results), 200