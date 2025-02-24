import connexion
import six
from swagger_server.models.student import Student
from swagger_server.service.student_service_mongo import *
from swagger_server import util
from flask import json, jsonify

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

from flask import jsonify, request
from bson.objectid import ObjectId

def get_student_by_id(student_id):
    """Gets student
    Returns a single student
    :param student_id: the uid
    :type student_id: (str, dict, object)
    :rtype: Student
    """
    try:
        # Convert student_id to string if it's an object
        if isinstance(student_id, dict):  
            return jsonify({"error": "Invalid student_id: received an object"}), 400
        elif not isinstance(student_id, str):  
            student_id = str(student_id)  # Convert non-string types (like int) to string

        print("student_id = ", student_id)

        student, status = get_by_id(student_id)  # get_by_id returns (student, status_code)
        
        if status == 404:
            return jsonify({"error": "Student not found"}), 404
        elif status == 400:
            return jsonify({"error": student}), 400  # Error message from get_by_id

        print("Student found:", student)

        return jsonify(student), 200

    except Exception as e:
        print(f"Error: {e}")
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