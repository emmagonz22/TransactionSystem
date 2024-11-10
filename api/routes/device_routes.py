from flask import Blueprint, request, jsonify
from models.device import Device
from db import db

device_bp = Blueprint("device", __name__, url_prefix="/device")


@device_bp.route("/<int:pid>", methods=["POST"])
def create_device(pid):
    """Create a new device for a person with the given pid."""
    data = request.get_json()
    data['pid'] = pid  # Ensure the person ID is included
    session = db.session
    new_device = Device(**data)
    session.add(new_device)
    session.commit()
    return jsonify({"message": "Device created", "did": new_device.did}), 201

@device_bp.route("/<int:pid>", methods=["GET"])
def get_devices(pid):
    """Retrieve all devices associated with a specific person ID (pid)."""
    session = db.session
    devices = session.query(Device).filter_by(pid=pid).all()
    if not devices:
        return jsonify({"message": "No devices found for the provided person ID"}), 404
    
    result = [
        {
            "did": device.did,
            "pid": device.pid,
            "device_type": device.device_type
        }
        for device in devices
    ]
    
    return jsonify(result), 200

@device_bp.route("/<int:pid>/<int:did>", methods=["PUT"])
def update_device(pid, did):
    """Update a specific device by its device ID (did) and person ID (pid)."""
    session = db.session
    device = session.query(Device).filter_by(pid=pid, did=did).first()
    if not device:
        return jsonify({"message": "Device not found"}), 404
    
    data = request.get_json()
    for key, value in data.items():
        setattr(device, key, value)
    
    session.commit()
    return jsonify({"message": "Device updated"})


@device_bp.route("/<int:pid>/<int:did>", methods=["DELETE"])
def delete_device(pid, did):
    """Delete a specific device by its device ID (did) and person ID (pid)."""
    session = db.session
    device = session.query(Device).filter_by(pid=pid, did=did).first()
    if not device:
        return jsonify({"message": "Device not found"}), 404
    
    session.delete(device)
    session.commit()
    return jsonify({"message": "Device deleted"})


@device_bp.route("/<int:pid>", methods=["DELETE"])
def delete_all_devices(pid):
    """Delete all devices associated with a specific person ID (pid)."""
    session = db.session
    devices = session.query(Device).filter_by(pid=pid).all()
    if not devices:
        return jsonify({"message": "No devices found for the provided person ID"}), 404
    
    for device in devices:
        session.delete(device)
    
    session.commit()
    return jsonify({"message": "All devices for the person were deleted"})