from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from sqlalchemy import func, desc
from db import db

transaction_bp = Blueprint("transaction", __name__, url_prefix="/transaction")

@transaction_bp.route("/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    session = db.session
    new_transaction = Transaction(**data)
    session.add(new_transaction)
    session.commit()
    return jsonify({"message": "Transaction created", "tid": new_transaction.tid}), 201

@transaction_bp.route("/<int:tid>", methods=["GET"])
def get_transaction(tid):
    session = db.session
    transactions = session.query(Transaction).filter_by(tid=tid).all()
    if not transactions:
        return jsonify({"message": "No transactions found for the provided transaction ID"}), 404
    
    # Return all entries with the same transaction ID
    result = [
        {
            "eid": transaction.eid,
            "tid": transaction.tid,
            "item_name": transaction.item_name,
            "price": transaction.price,
            "price_per_item": transaction.price_per_item,
            "quantity": transaction.quantity,
            "phone": transaction.phone,
            "store": transaction.store
        }
        for transaction in transactions
    ]
    
    return jsonify(result), 200


@transaction_bp.route("/<int:tid>", methods=["DELETE"])
def delete_transaction(tid):
    session = db.session
    transactions = session.query(Transaction).filter_by(tid=tid).all()
    if not transactions:
        return jsonify({"message": "No transactions found for the provided transaction ID"}), 404
    
    for transaction in transactions:
        session.delete(transaction)
    
    session.commit()
    return jsonify({"message": "All transactions with the provided transaction ID were deleted"})



@transaction_bp.route("/entry", methods=["POST"])
def create_entry():
    # Create a new entry within a transaction.
    data = request.get_json()
    required_fields = ["tid", "item_name", "price", "price_per_item", "quantity", "phone", "store"]
    
    # Validate required fields
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' is a required field"}), 400
    
    session = db.session
    new_entry = Transaction(
        tid=data["tid"],
        item_name=data["item_name"],
        price=data["price"],
        price_per_item=data.get("price_per_item"),  # Optional field
        quantity=data["quantity"],
        phone=data.get("phone"),  # Optional field
        store=data["store"]
    )
    
    session.add(new_entry)
    session.commit()
    return jsonify({"message": "Entry created", "eid": new_entry.eid}), 201


@transaction_bp.route("/<int:tid>", methods=["GET"])
def get_entry(eid):
    session = db.session
    transaction = session.query(Transaction).get(eid)
    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404
    return jsonify({
        "eid": transaction.eid,
        "tid": transaction.tid,
        "item_name": transaction.item_name,
        "price": transaction.price,
        "price_per_item": transaction.price_per_item,
        "quantity": transaction.quantity,
        "phone": transaction.phone,
        "store": transaction.store
    })

@transaction_bp.route("/entry/<int:eid>", methods=["PUT"])
def update_entry(eid):
    # Update a specific entry by its entry ID (eid).
    session = db.session
    entry = session.query(Transaction).get(eid)
    if not entry:
        return jsonify({"message": "Entry not found"}), 404
    
    data = request.get_json()
    for key, value in data.items():
        setattr(entry, key, value)
    
    session.commit()
    return jsonify({"message": "Entry updated"})

@transaction_bp.route("/entry/<int:eid>", methods=["DELETE"])
def delete_entry(eid):
    # Delete a specific entry by its entry ID (eid).
    session = db.session
    entry = session.query(Transaction).get(eid)
    if not entry:
        return jsonify({"message": "Entry not found"}), 404
    
    session.delete(entry)
    session.commit()
    return jsonify({"message": "Entry deleted"})

# ---Statistics---
@transaction_bp.route("/top-sold-items", methods=["GET"])
def get_top_sold_items():
    session = db.session

    # Get top 5 solf items (using quantity)
    top_items = (
        session.query(Transaction.item_name, func.sum(Transaction.quantity).label("total_quantity"))
        .group_by(Transaction.item_name)
        .order_by(desc("total_quantity"))
        .limit(5)
        .all()
    )

    # Format the data as a list of dictionaries
    top_items_data = [{"item_name": item[0], "total_quantity": item[1]} for item in top_items]

    return jsonify(top_items_data), 200


@transaction_bp.route("/top-five-stores-by-amount", methods=["GET"])
def get_top_five_stores_by_amout():
    session = db.session
    # Query to get the top 5 stores with the most sales
    top_stores = ( 
        session.query(Transaction.store, func.count(Transaction.eid).label("total_sales"))
        .group_by(Transaction.store)
        .order_by(func.count(Transaction.eid).desc())
        .limit(5)
        .all()
    )
    # store in dictionary to return as json
    results = [
        {"store": store[0], "total_sales": store[1]} for store in top_stores
    ]
    return jsonify(results), 200

@transaction_bp.route("/top-five-stores-by-profit", methods=["GET"])
def get_top_five_stores_by_profit():
    session = db.session
    # query and calculate totl profit 
    top_stores = (
        session.query(
            Transaction.store,
            func.sum(Transaction.price).label("total_profit")
        )
        .group_by(Transaction.store)
        .order_by(desc("total_profit"))
        .limit(5)
        .all()
    )
    
    # store in dictionary to return as json
    results = [
        {"store": store.store, "total_profit": store.total_profit} for store in top_stores
    ]
    return jsonify(results), 200