"""API application for student manager. It allows to find groups with
less or equals students count, find students on the course, add new
student, delete student, enroll student to the course, cross student
out the course.
"""
import json
from pathlib import Path

from flasgger import swag_from
from flask import request, make_response
from flask_restful import Resource
from simplexml import dumps

from students import queries
from db import get_session


class JsonMixin:
    def render_json(self, data: dict, status_code: int):
        """Convert dictionary to json, make and return response.
        :param status_code:
        :param data:
        :return Response:
        """
        json_data = json.dumps({'data': data})
        return make_response(json_data, status_code,
                             {'content-type': 'application/json'})


class XmlMixin:
    def render_xml(self, data: dict, status_code: int):
        """Convert dictionary to xml, make and return response.
        :param status_code:
        :param data:
        :return Response:
        """
        xml_data = dumps({'data': data})
        return make_response(xml_data, status_code,
                             {'content-type': 'application/xml'})


class ResponseMixin(JsonMixin, XmlMixin):
    def render(self, data: dict, format: str, status_code: int = 200):
        """Depends on query argument 'format' return response with
        json or with xml.
        :param status_code:
        :param format:
        :param data:
        :return Response:
        """
        return self.render_xml(data, status_code) if format == 'xml' \
            else self.render_json(data, status_code)


class ApiGetGroupsByStudentsCount(Resource, ResponseMixin):
    @swag_from(Path('../swagger_api_docs/'
                    'api_group_with_less_or_equals_students.yml'))
    def get(self):
        """Take request arguments and return API with information about
        groups with less or equals students count.
        Required argument 'count'"""
        session = get_session()
        count = int(request.args.get('count'))
        content = {
            'groups': queries.find_groups_with_less_or_equals_students_count(
                session, count)
        }
        return self.render(content, request.args.get('format'))


class ApiFindStudentsByCourse(Resource, ResponseMixin):
    @swag_from(Path('../swagger_api_docs/'
                    'api_find_students_by_course.yml'))
    def get(self, course):
        """Return API with information about students on defined course"""
        session = get_session()
        content = queries.find_students_by_course(session, course)
        return self.render(content, request.args.get('format'))


class ApiStudent(Resource, ResponseMixin):
    @swag_from(Path('../swagger_api_docs/api_add_new_student.yml'))
    def post(self):
        """Add student to the database.
        Required arguments 'group_id', 'first_name', 'last_name'."""
        session = get_session()
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_id = int(request.args.get('group_id'))
        queries.add_new_student(session, group_id, first_name, last_name)
        content = {'info': 'Student successfully added.'}
        return self.render(content, request.args.get('format'), 201)

    @swag_from(Path('../swagger_api_docs/api_delete_student.yml'))
    def delete(self):
        """Delete student from database by id.
        Required argument 'student_id'."""
        session = get_session()
        student_id = int(request.args.get('student_id'))
        queries.delete_student(session, student_id)
        content = {'info': 'Student successfully deleted.'}
        return self.render(content, request.args.get('format'))


class ApiCourse(Resource, ResponseMixin):
    @swag_from(Path('../swagger_api_docs/api_add_student_to_course.yml'))
    def put(self):
        """Add student to the defined course."""
        session = get_session()
        student_id = int(request.args.get('student_id'))
        course_name = request.args.get('course_name')
        queries.add_student_to_course(session, student_id, course_name)
        content = {'info': f'Student {student_id} successfully added to course '
                           f'{course_name}'}
        return self.render(content, request.args.get('format'))

    @swag_from(Path('../swagger_api_docs/'
                    'api_delete_student_from_course.yml'))
    def delete(self):
        """Delete student from course."""
        session = get_session()
        student_id = int(request.args.get('student_id'))
        course_name = request.args.get('course_name')
        queries.delete_student_from_course(session, student_id, course_name)
        content = {'info': f'Student {student_id} successfully deleted '
                           f'from course {course_name}'}
        return self.render(content, request.args.get('format'))
