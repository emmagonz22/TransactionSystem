from flask import Flask
from routes import init_routes
from config import Config
from db import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.debug = True
    # Initialize database
    db.init_app(app)
    
    # Initialize routes
    init_routes(app)
    print(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
