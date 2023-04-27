import click
import random
from faker import Faker, providers
from flask import current_app, g
from sqlalchemy.orm import sessionmaker

import models


def get_db():
    """Connect to db.
    :return:
    """
    if 'db' not in g:
        g.db = current_app.config['DATABASE']

    return g.db


def get_session():
    """Connect to db."""
    if 'session' not in g:
        engine = current_app.config['DATABASE']
        Session = sessionmaker(bind=engine)
        g.session = Session()

    return g.session


def close_session(e=None):
    """Close connection to db."""
    session = g.pop('session', None)

    if session is not None:
        session.close()


fake = Faker()
base = providers.BaseProvider(fake)
students = [fake.name() for _ in range(200)]
courses = ['math', 'biology', 'chemistry', 'english', 'physics',
           'history', 'literature', 'computer science', 'psychology',
           'art']


def random_group():
    rand_chars = ''.join(base.random_letters(2))
    rand_num = f'{base.random_digit()}{base.random_digit()}'
    return f'{rand_chars}-{rand_num}'


def generate_courses():
    return [random.choice(courses) for _ in range(random.randint(1, 3))]


def generate_group():
    return [students.pop() for _ in range(
        random.randint(15, 30)) if students]


def store_data():
    session = get_session()
    groups = [random_group() for _ in range(10)]

    group_models = [models.GroupModel(name=group) for group in groups]
    for group in group_models:
        session.add(group)
    session.commit()

    course_models = {name: models.CourseModel(name=name,
                                              description=name)
                     for name in courses}
    query = session.query(models.GroupModel)
    for group in query:
        for name in generate_group():
            first_name, last_name = name.split(maxsplit=1)
            student = models.StudentModel(group_id=group.id,
                                          first_name=first_name,
                                          last_name=last_name)
            for course in generate_courses():
                student.courses.append(course_models[course])
            session.add(student)
            group.students.append(student)
        session.add(group)

    session.commit()
    session.close()


def init_db():
    """Create tables and insert data."""
    engine = get_db()

    models.Base.metadata.create_all(engine)
    store_data()


@click.command('init-db')
def init_db_command():
    """Make cli command for db initialization."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register close_db and init_db_command in application."""
    app.teardown_appcontext(close_session)
    app.cli.add_command(init_db_command)
