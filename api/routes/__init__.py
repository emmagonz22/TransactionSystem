from .device_routes import device_bp
from .people_routes import people_bp
from .promotion_routes import promotion_bp
from .transaction_routes import transaction_bp
from .transfer_routes import transfer_bp

def init_routes(app):
    app.register_blueprint(device_bp)
    app.register_blueprint(people_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(transfer_bp)
