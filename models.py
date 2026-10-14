### Create the ORM Models and Relationships
###  models.py

'''
It defines:

The Department model.
The Employee model.
The Course model.
The association table.
All ORM relationships.

'''

from sqlalchemy import (
    String,
    ForeignKey,
    Table,
    Column,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database import Base


# =====================================================
# 1. MANY-TO-MANY ASSOCIATION TABLE
# =====================================================

employee_courses = Table(
    "employee_courses",   # The composite primary key prevents duplicate employee-course pairs
    Base.metadata,

    Column(
        "employee_id",
        ForeignKey("employees.employee_id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "course_id",
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# =====================================================
# 2. DEPARTMENT MODEL
# =====================================================

class Department(Base):

    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

   # One department has many employees.
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department",   # This attribute represents the two directions of the relationship
    ) 

    def __repr__(self):   # __repr__() provides a readable string representation of an object, mainly for debugging and development.    print(repr(department))  -- __repr__() makes SQLAlchemy objects easier to inspect and debug.
        return (
            f"Department("
            f"id={self.department_id}, "  
            f"name={self.department_name!r})"  # Displays the string with quotation marks.
        )


# =====================================================
# 3. EMPLOYEE MODEL
# =====================================================

class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    employee_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),  # Setting the foreign key in child table
        nullable=False,
        index=True,
    )

    # Many employees belong to one department.
    department: Mapped["Department"] = relationship(
        back_populates="employees",  # This attribute represents the two directions of the relationship
    )

    # Many employees can attend many courses.
    courses: Mapped[list["Course"]] = relationship(
        secondary=employee_courses,   # The secondary parameter identifies the association table.
        back_populates="employees",
    )

    def __repr__(self):
        return (
            f"Employee("
            f"id={self.employee_id}, "
            f"name={self.employee_name!r})"
        )


# =====================================================
# 4. COURSE MODEL
# =====================================================

class Course(Base):

    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    course_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    # A course can have many employees.
    employees: Mapped[list["Employee"]] = relationship(  
        secondary=employee_courses,    # The secondary parameter identifies the association table
        back_populates="courses",
    ) # The composite primary key prevents duplicate employee-course pairs


    def __repr__(self):
        return (
            f"Course("
            f"id={self.course_id}, "
            f"name={self.course_name!r})"
        )


'''
Important: Understand the relationships
--------------------------------------------
A. One-to-many
````````````````
Inside Department:

employees: Mapped[list["Employee"]] = relationship(
    back_populates="department",
)

Inside Employee:

department: Mapped["Department"] = relationship(
    back_populates="employees",
)

These attributes represent the two directions of the relationship.

The foreign key is on the employee table:

department_id: Mapped[int] = mapped_column(
    ForeignKey("departments.department_id"),
    nullable=False,
    index=True,
)

The database ensures that every employee references an existing department.



B. Many-to-many
`````````````````
The association table connects employees and courses:

employee_courses = Table(
    "employee_courses",
    Base.metadata,
    ...
)


The relationship uses:

courses: Mapped[list["Course"]] = relationship(
    secondary=employee_courses,
    back_populates="employees",
)

The secondary parameter identifies the association table.

NOTE: The composite primary key prevents duplicate employee-course pairs.



C. Why use back_populates?
--------------------------------

It connects the ORM relationship attributes.


For example:

employee.department  --> retrieves an employee's department, while:

department.employees -->  retrieves the employees belonging to that department.


Likewise:

employee.courses  and   course.employees

        navigate the many-to-many relationship in opposite directions.

'''
