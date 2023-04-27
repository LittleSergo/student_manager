from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    relationship
from sqlalchemy import Table, Column, String, ForeignKey
from typing import List


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
