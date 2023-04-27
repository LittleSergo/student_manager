from db import get_session
from models import StudentModel, GroupModel, CourseModel
from students import queries


def test_find_groups_with_less_or_equals_students_count(app):
    session = get_session()
    assert len(queries.find_groups_with_less_or_equals_students_count(
        session, 30)) == 10


def test_find_students_by_course(app):
    session = get_session()
    test_data = queries.find_students_by_course(session, 'math')
    query = session.query(CourseModel).filter_by(
        name='math').first()
    assert test_data == [{'student': f'{student.first_name} '
                                     f'{student.last_name}'}
                         for student in query.students]


def test_add_new_student(app):
    session = get_session()
    queries.add_new_student(session, 2, 'Jim', 'Bear')
    query = session.query(StudentModel).filter_by(
        first_name='Jim').first()
    assert query.last_name == 'Bear'


def test_delete_student(app):
    session = get_session()
    queries.delete_student(session, 5)
    assert session.query(StudentModel).filter_by(id=5).first() is None


def test_add_student_to_course(app):
    session = get_session()
    queries.add_student_to_course(session, 10, 'math')
    query = session.query(StudentModel).filter_by(id=10).first()
    assert 'math' in [course.name for course in query.courses]


def test_delete_student_from_course(app):
    session = get_session()
    query = session.query(StudentModel).filter_by(id=10).first()
    course = [course.name for course in query.courses].pop()
    queries.delete_student_from_course(session, 10, course)
    query = session.query(StudentModel).filter_by(id=10).first()
    assert course not in [course.name for course in query.courses]


def test_api_find_groups_with_less_or_equals_students_count(client):
    response = client.get('api/v1/group/?count=29')
    assert response.status_code == 200
    assert len(response.json['data']['groups']) == 10


def test_api_find_students_by_course(client):
    session = get_session()
    response = client.get('api/v1/course/math/')
    assert response.status_code == 200
    test_data = response.json['data']
    query = session.query(CourseModel).filter_by(
        name='math').first()
    assert test_data == [{'student': f'{student.first_name} '
                                     f'{student.last_name}'}
                         for student in query.students]


def test_api_add_new_student(client):
    response = client.post('api/v1/student/?group_id=2'
                           '&first_name=Faa&last_name=Fuu')
    assert response.status_code == 201
    session = get_session()
    query = session.query(StudentModel).filter_by(first_name='Faa').first()
    assert query.last_name == 'Fuu'


def test_api_delete_student(client):
    session = get_session()
    response = client.delete('api/v1/student/?student_id=5')
    assert session.query(StudentModel).filter_by(id=5).first() is None
    assert response.status_code == 200
    assert response.data == b'{"data": {"info": ' \
                            b'"Student successfully deleted."}}'


def test_api_add_student_to_course(client):
    session = get_session()
    response = client.put('api/v1/course/?student_id=5&course_name=math')
    query = session.query(StudentModel).filter_by(id=5).first()
    assert 'math' in [course.name for course in query.courses]
    assert response.status_code == 200
    assert response.data == b'{"data": {"info": "Student ' \
                            b'5 successfully added to course math"}}'


def test_api_delete_student_from_course(client):
    session = get_session()
    query = session.query(StudentModel).filter_by(id=5).first()
    course = [course.name for course in query.courses].pop()
    response = client.delete(f'api/v1/course/?student_id=5'
                             f'&course_name={course}')
    query = session.query(StudentModel).filter_by(id=5).first()
    assert course not in [course.name for course in query.courses]
    assert response.status_code == 200
