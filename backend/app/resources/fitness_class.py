from datetime import datetime
from flask_restful import Resource, reqparse, fields, marshal_with
from app import db
from app.models import FitnessClass

# Define response serialization structure
fitness_class_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "instructor": fields.String,
    "schedule": fields.String,  # Ensure schedule is serialized as a string
}

class FitnessClassResource(Resource):
    # Define request parser for validation
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str, help="Class name cannot be blank")
    parser.add_argument("description", required=True, type=str, help="Description cannot be blank")
    parser.add_argument("instructor", required=True, type=str, help="Instructor cannot be blank")
    parser.add_argument("schedule", required=True, type=str, help="Schedule must be in ISO 8601 format")

    @marshal_with(fitness_class_fields)
    def get(self, class_id=None):
        if class_id:
            fitness_class = FitnessClass.query.get(class_id)
            if not fitness_class:
                return {"message": "Fitness class not found"}, 404
            return fitness_class, 200

        classes = FitnessClass.query.all()
        return classes, 200

    def post(self):
        args = self.parser.parse_args()

        # Validate schedule format
        try:
            schedule = datetime.fromisoformat(args["schedule"])
        except ValueError:
            return {"message": "Invalid schedule format. Use ISO 8601 format."}, 400

        new_class = FitnessClass(
            name=args["name"],
            description=args["description"],
            instructor=args["instructor"],
            schedule=schedule
        )

        db.session.add(new_class)
        db.session.commit()

        return {"message": "Fitness class created", "id": new_class.id}, 201

    def put(self, class_id):
        fitness_class = FitnessClass.query.get(class_id)
        if not fitness_class:
            return {"message": "Fitness class not found"}, 404

        args = self.parser.parse_args()

        # Update fields if provided
        fitness_class.name = args["name"]
        fitness_class.description = args["description"]
        fitness_class.instructor = args["instructor"]
        
        try:
            fitness_class.schedule = datetime.fromisoformat(args["schedule"])
        except ValueError:
            return {"message": "Invalid schedule format. Use ISO 8601 format."}, 400

        db.session.commit()
        return {"message": "Fitness class updated", "id": fitness_class.id}, 200

    def delete(self, class_id):
        fitness_class = FitnessClass.query.get(class_id)
        if not fitness_class:
            return {"message": "Fitness class not found"}, 404

        db.session.delete(fitness_class)
        db.session.commit()
        return {"message": "Fitness class deleted"}, 200

# Separate class list resource if needed
class FitnessClassListResource(Resource):
    @marshal_with(fitness_class_fields)
    def get(self):
        classes = FitnessClass.query.all()
        return classes, 200