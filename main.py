#### Implement JOINs, Lazy Loading, and Eager Loading
### Create main.py

### This file contains separate functions for each concept.
### The examples share the same database models and sample data
 
from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

from database import SessionLocal

from models import (
    Department,
    Employee,
    Course,
    employee_courses,
)


# =====================================================
# 1. DISPLAY ALL EMPLOYEES
# =====================================================

def get_all_employees():

    print("\n--- ALL EMPLOYEES ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all()

        for employee in employees:
            print(
                employee.employee_id,
                employee.employee_name,
                employee.email,
            )


# =====================================================
# 2. ONE-TO-MANY RELATIONSHIP
# =====================================================

def get_employees_by_department():

    print("\n--- EMPLOYEES BY DEPARTMENT ---")

    with SessionLocal() as session:

        statement = (
            select(Department)
            .where(
                Department.department_name == "Python"
            )
        )

        department = session.scalar(statement)

        if department is None:
            print("Department not found.")
            return

        print("Department:", department.department_name)

        # Lazy loading may execute a query here.
        for employee in department.employees:  ### One more selecct statement is issued by SQLAlchemy
            print("-", employee.employee_name)
'''
By default, the collection is lazily loaded.

    If the collection has not already been loaded, SQLAlchemy issues another SELECT to retrieve the employees.

    This demonstrates the difference between retrieving a department and retrieving its related employees.
'''

# =====================================================
# 3. INNER JOIN
# =====================================================

def inner_join_employees_departments():

    print("\n--- INNER JOIN ---")

    with SessionLocal() as session:

        statement = (
            select(
                Employee.employee_name,
                Department.department_name,
            )
            .join(Employee.department)
            .order_by(Employee.employee_id)
        )

        rows = session.execute(statement).all()

        


# =====================================================
# 4. LEFT OUTER JOIN
# =====================================================

def left_join_departments_employees():

    print("\n--- LEFT OUTER JOIN ---")

    with SessionLocal() as session:

        #### LEFT JOIN
        # statement = (
        #     select(
        #         Department.department_name,
        #         Employee.employee_name,
        #     )
        #     .outerjoin(Department.employees)
        #     .order_by(
        #         Department.department_id,
        #         Employee.employee_id,
        #     )
        # )

        ##### RIGHT JOIN
        statement = (
            select(
            Department.department_name,
            Employee.employee_name,
            )
            .select_from(Employee)
            .outerjoin(Department, Employee.department_id == Department.department_id)
            .order_by(Employee.employee_id)
            )

        rows = session.execute(statement).all()

        for department_name, employee_name in rows:

            # print(
            #     department_name,
            #     "->",
            #     employee_name,
            # )
            print(
                 employee_name,
                 "->",
                 department_name,
             )



'''
RIGHT OUTER JOIN
------------------
NOTE: SQLAlchemy provides outerjoin() for LEFT OUTER JOINs by default, because outerjoin() uses isouter=True internally. For a RIGHT OUTER JOIN, you can reverse the table order and use a LEFT OUTER JOIN.

statement = (
    select(
        Department.department_name,
        Employee.employee_name,
    )
    .select_from(Employee)
    .outerjoin(Department, Employee.department_id == Department.department_id)
    .order_by(Employee.employee_id)
)

'''

# =====================================================
# 5. FILTER EMPLOYEES USING JOIN
# =====================================================

def get_python_department_employees():

    print("\n--- PYTHON DEPARTMENT EMPLOYEES ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .join(Employee.department)
            .where(
                Department.department_name == "Python"
            )
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all()

        for employee in employees:
            print(employee.employee_name)


# =====================================================
# 6. MANY-TO-MANY RELATIONSHIP   --- Eager loading using selectinload()
# =====================================================

def get_employee_courses():

    print("\n--- EMPLOYEE COURSES ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .where(
                Employee.employee_name == "Arun"
            )
            .options(  ### It tells SQLAlchemy to eagerly load the courses associated with the selected employee using a separate SELECT query.
                selectinload(Employee.courses) 
            )
        )

        employee = session.scalar(statement)

        if employee is None:
            print("Employee not found.")
            return

        print("Employee:", employee.employee_name)

        for course in employee.courses:
            print("-", course.course_name)

'''
For example:
---------------
Conceptually, the queries are similar to:
-- Query 1: Retrieve Arun
SELECT *
FROM employees
WHERE employee_name = 'Arun';  ## employee_id =1

-- Query 2: Retrieve Arun's associated courses
SELECT *
FROM courses
JOIN employee_courses
    ON courses.course_id = employee_courses.course_id
WHERE employee_courses.employee_id IN (1);


'''

# =====================================================
# 7. FIND EMPLOYEES ENROLLED IN A COURSE  -- employee_courses [Association Table]
# =====================================================

def get_employees_by_course():

    print("\n--- EMPLOYEES IN SQLALCHEMY ORM ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .join(Employee.courses)   ### Single SQL INNER JOIN Query is provided by SQLAlchemy for Association Table
            .where(
                Course.course_name ==  "SQLAlchemy ORM"  # "Python Fundamentals"     # 
            )
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all()

        for employee in employees:
            print(employee.employee_name)


# =====================================================
# 8. LAZY LOADING
# =====================================================

def demonstrate_lazy_loading():

    print("\n--- LAZY LOADING ---")

    with SessionLocal() as session:

        # Query 1: Load the employee.
        employee = session.scalar(
            select(Employee)
            .where(
                Employee.employee_name == "Arun"
            )
        )

        if employee is None:
            print("Employee not found.")
            return

        print("Employee:", employee.employee_name)

        # Accessing the unloaded relationship may
        # execute another SELECT.
        print(
            "Department:",
            employee.department.department_name,  # Accessing the unloaded relationship may execute another SELECT
        )


# =====================================================
# 9. EAGER LOADING USING JOINEDLOAD   --- [specifies LEFT OUTER JOIN]
# =====================================================

def demonstrate_joinedload():

    print("\n--- JOINEDLOAD ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .options(
                joinedload(Employee.department)   ###LEFT OUTER JOIN
            )
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all()

        for employee in employees:

            print(
                employee.employee_name,
                "->",
                employee.department.department_name,
            )


# =====================================================
# 10. EAGER LOADING USING SELECTINLOAD  --- All employees courses
# =====================================================

def demonstrate_selectinload():

    print("\n--- SELECTINLOAD ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .options(
                selectinload(Employee.courses)
            )
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all()

        for employee in employees:

            print("\nEmployee:", employee.employee_name)

            for course in employee.courses:
                print("-", course.course_name)


# =====================================================
# 11. SOLVE THE N+1 QUERY PROBLEM
# =====================================================

def demonstrate_n_plus_one_solution():

    print("\n--- N+1 SOLUTION ---")

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .options(
                joinedload(Employee.department),  # Loads each employee's department using a SQL LEFT OUTER JOIN
                selectinload(Employee.courses), # Loads employee courses using a separate SELECT query
                # Why a separate query?   Because an employee can have multiple courses.
            )
            .order_by(Employee.employee_id)
        )

        employees = session.scalars(statement).all() # Retrieves all employee objects from the query

        for employee in employees:

            print(
                employee.employee_name,
                "| Department:",
                employee.department.department_name,  # Accesses the employee's department name,  using single SELECT by joinedload(), otherwise needs extra SELECT.... So N + 1 query problem occurs
            )
# NOTE : With joinedload(), SQLAlchemy retrieves the department data as part of the original query.
            print(
                "Courses:",
                [
                    course.course_name   # This is a list comprehension.
                    for course in employee.courses # Accesses the employee's related courses
                ],
            )


# =====================================================
# 12. FILTERING AND PAGINATION
# =====================================================

def get_employees_paginated():

    print("\n--- PAGINATION ---")

    page = 1
    page_size = 2

    offset_value = (page - 1) * page_size

    with SessionLocal() as session:

        statement = (
            select(Employee)
            .order_by(Employee.employee_id)
            .offset(offset_value)
            .limit(page_size)
        )

        employees = session.scalars(statement).all()

        for employee in employees:
            print(
                employee.employee_id,
                employee.employee_name,
            )


# =====================================================
# 13. COUNT EMPLOYEES BY DEPARTMENT
# =====================================================

def count_employees_by_department():

    print("\n--- EMPLOYEE COUNT BY DEPARTMENT ---")

    with SessionLocal() as session:

        statement = (
            select(
                Department.department_name,
                func.count(Employee.employee_id),
            )
            .outerjoin(Department.employees)
            .group_by(
                Department.department_id,
                Department.department_name,
            )
            .order_by(Department.department_id)
        )

        rows = session.execute(statement).all()

        for department_name, employee_count in rows:

            print(
                department_name,
                "->",
                employee_count,
            )


# =====================================================
# 14. RETRIEVE ONLY REQUIRED COLUMNS
# =====================================================

def get_employee_summary():

    print("\n--- EMPLOYEE SUMMARY ---")

    with SessionLocal() as session:

        statement = (
            select(
                Employee.employee_id,
                Employee.employee_name,
            )
            .order_by(Employee.employee_id)
        )

        rows = session.execute(statement).all()

        for employee_id, employee_name in rows:

            print(employee_id, employee_name)


# =====================================================
# MAIN MENU
# =====================================================

def main():

    operations = {
        "1": get_all_employees,
        "2": get_employees_by_department,
        "3": inner_join_employees_departments,
        "4": left_join_departments_employees,
        "5": get_python_department_employees,
        "6": get_employee_courses,
        "7": get_employees_by_course,
        "8": demonstrate_lazy_loading,
        "9": demonstrate_joinedload,
        "10": demonstrate_selectinload,
        "11": demonstrate_n_plus_one_solution,
        "12": get_employees_paginated,
        "13": count_employees_by_department,
        "14": get_employee_summary,
    }

    while True:

        print(
            """
=========================================
SQLALCHEMY RELATIONSHIP TRAINING
=========================================

1. Display all employees
2. One-to-many relationship
3. INNER JOIN
4. LEFT OUTER JOIN
5. Filter employees by department
6. Many-to-many relationship
7. Find employees by course
8. Lazy loading
9. Eager loading using joinedload
10. Eager loading using selectinload
11. N+1 query solution
12. Pagination
13. Count employees by department
14. Retrieve selected columns
0. Exit
"""
        )

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Training completed.")
            break

        operation = operations.get(choice)

        if operation is None:
            print("Invalid choice. Try again.")
            continue

        try:
            operation()

        except Exception as exc:
            print("Operation failed:", exc)
            print(
                "Check the database connection, "
                "table schema, and SQL logs."
            )


if __name__ == "__main__":
    main()




'''

N + 1 problem
===================

What is selectinload()? Why do we use it?
---------------------------------------------

selectinload() is a SQLAlchemy eager-loading strategy.

It loads related objects using a separate SQL query that retrieves related records for the selected parent objects.

For example:

select(Employee).options(
    selectinload(Employee.courses)
)

This tells SQLAlchemy:

Retrieve the employee.
Retrieve the employee's courses in a separate query.
Populate the employee.courses relationship with the retrieved objects.
What happens without selectinload()?

Consider:

statement = (
    select(Employee)
    .where(Employee.employee_name == "Arun")
)

employee = session.scalar(statement)

for course in employee.courses:
    print(course.course_name)

If Employee.courses uses the default lazy-loading behavior, accessing employee.courses may trigger an additional SQL query.

For one employee, that might be perfectly acceptable.

However, imagine retrieving 100 employees and accessing the courses for each one. SQLAlchemy might execute:

One query to retrieve the employees.
Up to 100 additional queries to retrieve their courses.

This is a common form of the N+1 query problem.

Using selectinload() can reduce this to approximately two queries for a simple relationship: one for the employees and another for their courses.

The actual number of queries depends on factors such as the number of parent objects and batching.



'''