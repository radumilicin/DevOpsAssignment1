import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query


db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(os.curdir, "students.json")
student_db = TinyDB(db_file_path)


def add(student=None):
    print("in add w db_file_path = " + db_file_path)
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    print("before if with res = " + str(res))
    if res:
        return 'already exists', 409
    print("adding student")
    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id 


def get_by_id(student_id=None, subject=None):
    table = student_db.table('_default')
    
    # Search for student with matching student_id
    student = table.get(lambda x: x.get('student_id') == student_id)
    if not student:
        return 'not found', 404
    return student

def delete(student_id=None):
    # Get all records from the default table
    table = student_db.table('_default')
    
    # Search for student with matching student_id
    student = table.get(lambda x: x.get('student_id') == student_id)
    
    if not student:
        return 'not found', 404
        
    # Get the doc_id of the matching record
    doc_id = table.get(lambda x: x.get('student_id') == student_id).doc_id
    
    # Remove the record using doc_id
    student_db.remove(doc_ids=[doc_id])
    
    return student_id