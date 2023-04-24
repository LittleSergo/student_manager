# План роботи
1. Створити базу даних
2. Написати моделі таблиць БД, створити таблиці:
 

    class Base(DeclarativeBase):
        pass


    association_table = Table(
        "association_table",
        Base.metadata,
        Column("student_id", ForeignKey("student.id")),
        Column("course_id", ForeignKey("course.id")),
    )


    class GroupModel(Base):
        __tablename__ = 'group'

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))

        students: Mapped[List['StudentModel']] = relationship(back_populates="group")


    class StudentModel(Base):
        __tablename__ = 'student'

        id: Mapped[int] = mapped_column(primary_key=True)
        group_id = mapped_column(ForeignKey('group.id'))
        first_name: Mapped[str] = mapped_column(String(30))
        last_name: Mapped[str] = mapped_column(String(30))

        group: Mapped['GroupModel'] = relationship(back_populates="students")
        courses: Mapped[List["CourseModel"]] = relationship(
            'CourseModel',
            secondary=association_table,
            back_populates="students")


    class CourseModel(Base):
        __tablename__ = 'course'

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        description: Mapped[str]

        students: Mapped[List["StudentModel"]] = relationship(
            'StudentModel',
            secondary=association_table,
            back_populates="courses")


    Base.metadata.create_all(engine)
    

3. Внести сгенеровані дані в таблиці:


    from faker import Faker, providers
    import random

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
        return [students.pop() for _ in range(random.randint(15, 30)) if students]
   
   
    def insert_data(engine):
        Session = sessionmaker(bind=engine)
        session = Session()
        groups = [random_group() for _ in range(10)]

        group_models = [GroupModel(name=group) for group in groups]
        for group in groups_models:
            session.add(group)
        session.commit()

        course_models = {name: CourseModel(name=name, description=name)
                     for name in courses}
        query = session.query(GroupModel)
        for group in query:
            for name in generate_group():
                first_name, last_name = name.split(maxsplit=1)
                student = StudentModel(group_id=group.id,
                                       first_name=first_name,
                                       last_name=last_name)
                for course in generate_courses():
                    student.courses.append(course_models[course])
                session.add(student)
                group.students.append(student)
            session.add(group)

        session.commit()


4. Написати функції-запити:
   1) знаходження груп з меньшою або рівною кількістю студентів
 

    def find_groups_with_less_or_equals_students_count(session, count: int):
        query = session.query(GroupModel) \
            .join(StudentModel) \
            .having(func.count(GroupModel.students) >= count) \
            .group_by(GroupModel.id)
        return [group.name for group in query]


   2) знайти всіх студентів які відносяться до заданого курсу:


    def find_students_by_course(session, course: str):
        query = session.query(CourseModel).filter_by(name=course).first()
        return [f'{student.first_name} {student.last_name}'
                for student in query.students]


   3) додати нового студента:


    def add_new_student(session, group_id: int, 
                        first_name: str, last_name: str):
        student = StudentModel(group_id=group_id,
                               first_name=first_name,
                               last_name=last_name)
        session.add(student)
        session.commit()


   4) видалити студента за його ID:


    def delete_student(session, student_id: int):
        student = session.query(StudentModel).filter_by(id=student_id).first()
        session.delete(student)
        session.commit()


   5) додати студента на курс:


    def add_student_to_course(session, student_id: int, course_name: str):
        student = session.query(StudentModel).filter_by(id=student_id).first()
        course = session.query(CourseModel).filter_by(name=course).first()
        student.courses.append(course)
        session.commit()


   6) видалити студента з курсу:


    def delete_student_from_course(session, student_id: int, course_name: str):
        student = session.query(StudentModel).filter_by(id=student_id).first()
        for course in student.courses:
            if course.name == course_name:
                student.courses.remove(course)
        session.commit()


5. Написати фласк додаток
