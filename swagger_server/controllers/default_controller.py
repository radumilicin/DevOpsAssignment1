import connexion
import six
from swagger_server.models.student import Student
from swagger_server.service.student_service_mongo import *
from swagger_server import util
from flask import json, jsonify, request
from bson.objectid import ObjectId

def add_student(body=None):
    """Add a new student
    Adds an item to the system
    :param body: Student item to add
    :type body: dict | bytes
    :rtype: float
    """
    print("in add_student")
    if connexion.request.content_type == 'application/json': 
        try:
            print("in try")
            # Get JSON directly from the request body
            student = Student.from_dict(body)
            print("student = " + str(body))
            result, status_code = add(student)  # Unpack tuple correctly
            
            if status_code != 200:
                return jsonify({"message": "Failed to add student"}), status_code
            
            return jsonify({"message": "Added student"}), 200
        
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Error parsing or adding student"}), 500
    
    return jsonify({"error": "Invalid content type"}), 400

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

        # Handle the [object Object] case
        if student_id == "[object Object]":
            # For test cases, we need to get the student using a valid ObjectId
            # You might need to adjust this based on your test data
            student, status = get_by_id(student_id)
            if status != 200:
                return jsonify({"error": "Student not found"}), status
        else:
            # Normal case - try to get student with the provided ID
            student, status = get_by_id(student_id)
            if status != 200:
                return jsonify({"error": "Student not found"}), status

        # Transform MongoDB document into expected response format
        grade_records = []
        if "grades" in student:
            # Convert grades dict to array format expected by tests
            for subject, grade in student["grades"].items():
                grade_records.append({
                    "subject_name": subject,
                    "grade": grade
                })

        response = {
            "student_id": student.get("_id", student_id),  # Use MongoDB _id or passed id
            "first_name": student.get("first_name", ""),
            "last_name": student.get("last_name", ""),
            "grade_records": grade_records
        }

        print("Sending response:", response)  # Debug print
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