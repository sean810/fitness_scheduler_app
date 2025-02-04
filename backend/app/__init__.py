from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from .config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app():
    """Flask application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend-backend communication
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import models to avoid circular imports
    from app import models

    # Register API routes
    register_routes(api)

    return app

def register_routes(api):
    """Register Flask-RESTful API routes."""
    from app.resources.user import UserResource
    from app.resources.fitness_class import FitnessClassResource
    from app.resources.booking import BookingResource

    api.add_resource(UserResource, "/users", "/users/<int:user_id>")
    api.add_resource(FitnessClassResource, "/classes", "/classes/<int:class_id>")
    api.add_resource(BookingResource, "/bookings", "/bookings/<int:booking_id>")