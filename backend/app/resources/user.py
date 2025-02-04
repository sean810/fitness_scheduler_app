import re
from flask_restful import Resource, reqparse, abort
from app import db
from app.models import User

# Email validation function (moved outside for better reusability)
def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(email_regex, email))

class UserResource(Resource):
    def get(self, user_id=None):
        """Fetch all users or a specific user by ID."""
        if user_id:
            # Ensure the user_id is an integer
            try:
                user_id = int(user_id)
            except ValueError:
                abort(400, message="Invalid user ID. It must be a number.")
                
            user = User.query.get_or_404(user_id)
            return user.serialize(), 200  # Return a single user

        users = User.query.all()
        return [user.serialize() for user in users], 200  # Return all users

    def post(self):
        """Create a new user."""
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name cannot be blank")
        parser.add_argument("email", required=True, help="Email cannot be blank")
        args = parser.parse_args()

        # Validate email format
        if not is_valid_email(args["email"]):
            abort(400, message="Invalid email format")

        # Check if email already exists
        if User.query.filter_by(email=args["email"]).first():
            abort(400, message="Email already in use")

        # Create and save the new user
        new_user = User(name=args["name"], email=args["email"])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created", "id": new_user.id}, 201

    def put(self, user_id):
        """Update an existing user."""
        # Ensure the user_id is an integer
        try:
            user_id = int(user_id)
        except ValueError:
            abort(400, message="Invalid user ID. It must be a number.")

        user = User.query.get_or_404(user_id)

        parser = reqparse.RequestParser()
        parser.add_argument("name", required=False)
        parser.add_argument("email", required=False)
        args = parser.parse_args()

        # Validate email format if provided
        if args["email"] and not is_valid_email(args["email"]):
            abort(400, message="Invalid email format")

        # Check if email already exists when updating
        if args["email"] and User.query.filter_by(email=args["email"]).first():
            abort(400, message="Email already in use")

        # Update user fields if provided
        if args["name"]:
            user.name = args["name"]
        if args["email"]:
            user.email = args["email"]

        db.session.commit()
        return {"message": "User updated", "id": user.id}, 200

    def delete(self, user_id):
        """Delete a user by ID."""
        # Ensure the user_id is an integer
        try:
            user_id = int(user_id)
        except ValueError:
            abort(400, message="Invalid user ID. It must be a number.")

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200