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

        # If we get "[object Object]", try to extract the actual ID from the request URL
        if student_id == "[object Object]":
            # Assuming you have access to the request object from Flask
            from flask import request
            # Get the actual URL path
            path = request.path
            # Try to extract the ID from the path
            try:
                # Split the path and get the last segment
                actual_id = path.split('/')[-1]
                if actual_id and actual_id != "[object Object]":
                    student_id = actual_id
                else:
                    return jsonify({"error": "Invalid student ID format"}), 400
            except:
                return jsonify({"error": "Could not parse student ID from request"}), 400

        # Clean and validate the ID
        try:
            # Remove any whitespace
            student_id = str(student_id).strip()
            
            # Basic validation
            if not student_id:
                return jsonify({"error": "Student ID cannot be empty"}), 400
                
            if len(student_id) > 50:  # Arbitrary max length
                return jsonify({"error": "Student ID too long"}), 400
                
            # If you expect numeric IDs, uncomment this:
            # if not student_id.isdigit():
            #     return jsonify({"error": "Student ID must be numeric"}), 400
                
            print(f"Processed student_id = {student_id}")
            
            # Get student data
            student, status = get_by_id(student_id)
            
            if status == 404:
                return jsonify({"error": "Student not found"}), 404
            elif status == 400:
                return jsonify({"error": student}), 400
                
            # Format response
            response = {
                "student_id": student_id,
                "first_name": student.get("first_name"),
                "last_name": student.get("last_name"),
                "grade_records": [
                    {
                        "subject_name": subject,
                        "grade": grade
                    } for subject, grade in student.get("grades", {}).items()
                ]
            }
            
            return jsonify(response), 200
            
        except ValueError as ve:
            return jsonify({"error": f"Invalid student ID format: {str(ve)}"}), 400
            
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