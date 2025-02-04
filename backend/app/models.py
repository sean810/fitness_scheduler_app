from datetime import datetime
from app import db
import re

# User Model (One-to-Many with Bookings)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationship with Bookings (Cascade delete ensures dependent bookings are removed)
    bookings = db.relationship("Booking", backref="user", lazy="joined", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def is_valid_email(email):
        """Validates email format using a regex."""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return bool(re.match(email_regex, email))


# Fitness Class Model (One-to-Many with Bookings)
class FitnessClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)

    # Relationship with Bookings
    bookings = db.relationship("Booking", backref="fitness_class", lazy="joined", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FitnessClass {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instructor": self.instructor,
            "schedule": self.schedule.isoformat(),  # Returns ISO format
            "readable_schedule": self.schedule.strftime("%Y-%m-%d %H:%M:%S")  # Readable date format
        }


# Booking Model (Many-to-Many with additional attributes)
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default="confirmed")  # Booking status (e.g., "confirmed", "cancelled")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    fitness_class_id = db.Column(db.Integer, db.ForeignKey("fitness_class.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set to the current time

    def __repr__(self):
        return f"<Booking {self.user_id} for {self.fitness_class_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "user_id": self.user_id,
            "fitness_class_id": self.fitness_class_id,
            "created_at": self.created_at.isoformat(),  # Returns ISO format
            "readable_created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Readable date format
        }