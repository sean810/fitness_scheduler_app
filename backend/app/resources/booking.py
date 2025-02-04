from flask_restful import Resource, reqparse, fields, marshal_with
from app import db
from app.models import Booking, User, FitnessClass

# Define response serialization structure
booking_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "fitness_class_id": fields.Integer,
    "status": fields.String,
}

class BookingResource(Resource):
    # Define request parser for validation
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", required=True, type=int, help="User ID cannot be blank")
    parser.add_argument("fitness_class_id", required=True, type=int, help="Fitness class ID cannot be blank")
    parser.add_argument("status", required=False, default="confirmed", type=str, help="Booking status")

    @marshal_with(booking_fields)
    def get(self, booking_id=None):
        if booking_id:
            booking = Booking.query.get(booking_id)
            if not booking:
                return {"message": "Booking not found"}, 404
            return booking, 200

        bookings = Booking.query.all()
        return bookings, 200

    def post(self):
        args = self.parser.parse_args()

        # Validate user and fitness class existence
        if not User.query.get(args["user_id"]):
            return {"message": "User not found"}, 404
        if not FitnessClass.query.get(args["fitness_class_id"]):
            return {"message": "Fitness class not found"}, 404

        # Create new booking
        new_booking = Booking(
            user_id=args["user_id"], 
            fitness_class_id=args["fitness_class_id"], 
            status=args["status"]
        )
        
        db.session.add(new_booking)
        db.session.commit()

        return {"message": "Booking created", "id": new_booking.id}, 201

    def put(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        args = self.parser.parse_args()

        # Update fields if provided
        if args["user_id"] and User.query.get(args["user_id"]):
            booking.user_id = args["user_id"]
        if args["fitness_class_id"] and FitnessClass.query.get(args["fitness_class_id"]):
            booking.fitness_class_id = args["fitness_class_id"]
        if args["status"]:
            booking.status = args["status"]

        db.session.commit()
        return {"message": "Booking updated", "id": booking.id}, 200

    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        db.session.delete(booking)
        db.session.commit()
        return {"message": "Booking deleted"}, 200