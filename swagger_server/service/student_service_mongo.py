from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# print("MONGO_URI = " + os.getenv("MONGO_URI"))

# Check if MONGO_URI is set, otherwise default to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/student_db")

# Connect to MongoDB using the URI
client = MongoClient(mongo_uri)

# Set up MongoDB connection
db = client["student_db"]
students_collection = db["students"]

def add(student):
    print("Adding student to MongoDB")

    # Check if student already exists
    existing_student = students_collection.find_one({
        "student_id": student.student_id
    })

    print("existing student: " + str(existing_student))
    
    if existing_student:
        return 'already exists', 409

    # Insert student and return the generated ID
    result = students_collection.insert_one(student.to_dict())
    print("result = " + str(result))
    # student.student_id = str(result.inserted_id)
    
    return student.student_id, 200

def get_by_id(student_id):
    try:
        student = students_collection.find_one({"student_id": student_id})
        if not student:
            return 'not found', 404
        
        student["_id"] = str(student["_id"])     
        return student

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
