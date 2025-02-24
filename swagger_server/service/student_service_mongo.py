from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from flask import jsonify

# print("MONGO_URI = " + os.getenv("MONGO_URI"))

# Check if MONGO_URI is set, otherwise default to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/student_db")

print("mongo_uri = " + os.getenv("MONGO_URI"))

# Connect to MongoDB using the URI
client = MongoClient(mongo_uri)

# Set up MongoDB connection
db = client["student_db"]
students_collection = db["students"]
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB (modify as needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]
students_collection = db["students"]


def add(student):
    print("Adding student to MongoDB")

    # Ensure student dict has _id if provided
    student_data = student.to_dict()

    if "_id" in student_data:
        try:
            student_data["_id"] = ObjectId(student_data["_id"])  # Convert to ObjectId if provided
        except:
            return "Invalid _id format", 400

        # Check if student with this _id exists
        existing_student = students_collection.find_one({"_id": student_data["_id"]})
        if existing_student:
            return 'already exists', 409

    # Insert student and return the generated ID
    result = students_collection.insert_one(student_data)

    return str(result.inserted_id), 200

def get_by_id(student_id):
    try:
        obj_id = ObjectId(student_id)  # Ensure valid ObjectId
        student = students_collection.find_one({"_id": obj_id})

        if not student:
            return 'not found', 404

        student["_id"] = str(student["_id"])  # Convert ObjectId to string
        return student, 200

    except Exception as e:
        return str(e), 400


def delete(student_id):
    try:
        result = students_collection.delete_one({"student_id": student_id})
        
        if result.deleted_count == 0:
            return 'not found', 404
        
        return student_id
    
    except Exception as e:
        return str(e), 400
