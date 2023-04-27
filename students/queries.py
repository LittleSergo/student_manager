from sqlalchemy import func
import models


def find_groups_with_less_or_equals_students_count(
        session, count: int = 30):
    """Make query and find groups where students count less or equals
    to count variable.
    :param session:
    :param count:
    :return dict: dictionary with group names
    """
    query = session.query(models.GroupModel) \
        .join(models.StudentModel) \
        .having(func.count(models.GroupModel.students) <= count) \
        .group_by(models.GroupModel.id)
    return [{'group': group.name} for group in query]


def find_students_by_course(session, course_name: str):
    """Make query and find students which relates to defined course.
    :param session:
    :param course_name:
    :return dict: dictionary with students names
    """
    query = session.query(models.CourseModel).filter_by(
        name=course_name).first()
    return [{'student': f'{student.first_name} {student.last_name}'}
            for student in query.students]


def add_new_student(session, group_id: int,
                    first_name: str, last_name: str):
    """Add new student.
    :param session:
    :param group_id:
    :param first_name:
    :param last_name:
    :return:
    """
    student = models.StudentModel(group_id=group_id,
                                  first_name=first_name,
                                  last_name=last_name)
    session.add(student)
    session.commit()


def delete_student(session, student_id: int):
    """Delete student by id.
    :param session:
    :param student_id:
    :return:
    """
    student = session.query(models.StudentModel).filter_by(
        id=student_id).first()
    session.delete(student)
    session.commit()


def add_student_to_course(session, student_id: int, course_name: str):
    """Add student to the course
    :param session:
    :param student_id:
    :param course_name:
    :return:
    """
    student = session.query(models.StudentModel).filter_by(
        id=student_id).first()
    course = session.query(models.CourseModel).filter_by(
        name=course_name).first()
    student.courses.append(course)
    session.commit()


def delete_student_from_course(session, student_id: int,
                               course_name: str):
    """Delete student from the course.
    :param session:
    :param student_id:
    :param course_name:
    :return:
    """
    student = session.query(models.StudentModel).filter_by(
        id=student_id).first()
    for course in student.courses:
        if course.name == course_name:
            student.courses.remove(course)
    session.commit()
