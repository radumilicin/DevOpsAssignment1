import connexion
import six
from swagger_server.models.student import Student
from swagger_server.service.student_service_mongo import *
from swagger_server import util
from flask import json, jsonify, request
from bson.objectid import ObjectId

# def add_student(body=None):
#     """Add a new student
#     Adds an item to the system
#     :param body: Student item to add
#     :type body: dict | bytes
#     :rtype: float
#     """
#     print("in add_student")
#     if connexion.request.content_type == 'application/json': 
#         try:
#             print("in try")
#             # Get JSON directly from the request body
#             student = Student.from_dict(body)
#             print("student = " + str(body))
#             result, status_code = add(student)  # Unpack tuple correctly
            
#             if status_code != 200:
#                 return jsonify({"message": "Failed to add student"}), status_code
            
#             return jsonify({"message": "Added student"}), 200
        
#         except Exception as e:
#             print(f"Error: {e}")
#             return jsonify({"error": "Error parsing or adding student"}), 500
    
#     return jsonify({"error": "Invalid content type"}), 400

def add(student):
    print("Adding student to MongoDB")
    # Convert the student object to the correct format for MongoDB
    student_data = student.to_dict()
    
    # Convert grade_records array to grades object
    grades = {}
    if 'grade_records' in student_data:
        for grade_record in student_data['grade_records']:
            grades[grade_record['subject_name']] = grade_record['grade']
    
    # Create the MongoDB document
    mongo_doc = {
        "first_name": student_data.get('first_name'),
        "last_name": student_data.get('last_name'),
        "grades": grades
    }
    
    try:
        # Insert and get the ID
        result = students_collection.insert_one(mongo_doc)
        # Store the ID for later retrieval
        inserted_id = str(result.inserted_id)
        return inserted_id, 200
    except Exception as e:
        return str(e), 400

def get_student_by_id(student_id):
    """Gets student by ID
    Returns a single student with their grade records
    :param student_id: the uid
    :type student_id: (str, dict, object)
    :rtype: Student
    """
    try:
        print(f"Raw student_id input type: {type(student_id)}")
        print(f"Raw student_id value: {student_id}")
        
        # Get student data
        student, status = get_by_id(student_id)
        
        if status != 200:
            return jsonify({"error": "Student not found"}), 404
            
        # Convert grades back to grade_records array
        grade_records = []
        if "grades" in student:
            for subject_name, grade in student["grades"].items():
                grade_records.append({
                    "subject_name": subject_name,
                    "grade": grade
                })
                
        response = {
            "student_id": student.get("_id"),
            "first_name": student.get("first_name"),
            "last_name": student.get("last_name"),
            "grade_records": grade_records
        }
        
        print("Sending response:", response)
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in get_student_by_id: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def delete_student(student_id):
    """Delete student
    Delete a student by ID
    :param student_id: the uid
    :type student_id: int
    :rtype: object
    """
    try:
        result = delete(student_id)
        if result == "not found":
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500