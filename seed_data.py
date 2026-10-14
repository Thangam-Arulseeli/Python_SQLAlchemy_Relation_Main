### Create the Tables and Insert Sample Data

# This script creates the tables and inserts sample records.

# Training environment note: Base.metadata.create_all() creates missing tables but does not update existing table definitions. If you change a model later, use migrations or reset a disposable training database as appropriate.

from sqlalchemy import select

from database import Base, engine, SessionLocal

from models import (
    Department,
    Employee,
    Course,
)


# =====================================================
# 1. CREATE TABLES
# =====================================================

Base.metadata.create_all(engine)
## Base.metadata - Contains information about the database tables defined by those models.
# Base.metadata knows what tables to create, and engine tells SQLAlchemy which database to connect to.

## create_all() uses that information to create the missing tables.

print("Tables created successfully.")


# =====================================================
# 2. INSERT SAMPLE DATA
# =====================================================

with SessionLocal() as session:

    try:

        # Prevent duplicate sample records on reruns.
        existing_employee = session.scalar(
            select(Employee).where(
                Employee.email == "arun@example.com"
            )
        )

        if existing_employee:
            print(
                "Sample data already exists. "
                "Skipping insertion."
            )

        else:

            # Create departments.
            python_department = Department(
                department_name="Python",
            )

            java_department = Department(
                department_name="Java",
            )

            testing_department = Department(
                department_name="Testing",
            )


            # Create courses.
            python_course = Course(
                course_name="Python Fundamentals",
            )

            sqlalchemy_course = Course(
                course_name="SQLAlchemy ORM",
            )

            fastapi_course = Course(
                course_name="FastAPI",
            )

            # Create employees.
            arun = Employee(
                employee_name="Arun",
                email="arun@example.com",
                department=python_department,
                courses=[
                    python_course,
                    sqlalchemy_course,
                ],
            )

            priya = Employee(
                employee_name="Priya",
                email="priya@example.com",
                department=python_department,
                courses=[
                    python_course,
                    fastapi_course,
                ],
            )

            karthik = Employee(
                employee_name="Karthik",
                email="karthik@example.com",
                department=java_department,
                courses=[
                    sqlalchemy_course,
                ],
            )

            divya = Employee(
                employee_name="Divya",
                email="divya@example.com",
                department=testing_department,
                courses=[],
            )

            session.add_all(
                [arun, priya, karthik, divya]
            )

            session.commit()

            print("Sample data inserted successfully.")

    except Exception:
        session.rollback()
        raise


print("Database initialization completed.")


'''
Why is the code structured this way?

We create the objects and associate them using Python relationships.

For example:

arun = Employee(
    employee_name="Arun",
    email="arun@example.com",
    department=python_department,
    courses=[
        python_course,
        sqlalchemy_course,
    ],
)

This establishes:

Arun belongs to the Python department.
Arun attends Python Fundamentals.
Arun attends SQLAlchemy ORM.

SQLAlchemy manages the foreign keys and association rows when the session flushes.

We do not have to manually insert each employee-course association row.


Execute the script
    > python seed_data.py

Expected output:

Tables created successfully.
Sample data inserted successfully.
Database initialization completed.

On subsequent runs, the sample insertion is skipped if Arun's email already exists.

NOTE: 
This is a simple rerun safeguard, not a complete database seeding framework. If you need to reset all sample data, use a dedicated disposable sample/testing database rather than deleting production records.

IMPORTANT NOTE: Alembic --> Manages version-controlled changes to an existing database schema

'''