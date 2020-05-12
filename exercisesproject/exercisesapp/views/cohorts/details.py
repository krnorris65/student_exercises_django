import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Instructor, Student, Cohort
from ..connection import Connection

def create_cohort(cursor, row):
    _row = sqlite3.Row(cursor, row)

    cohort = Cohort()
    cohort.id = _row["cohort_id"]
    cohort.name = _row["cohort_name"]

    cohort.students = []
    cohort.instructors = []

    student = None
    if _row["student_id"] is not None:
        student = Student()
        student.id = _row["student_id"]
        student.first_name = _row["s_first"]
        student.last_name = _row["s_last"]
        student.slack_handle = _row["s_slack"]
        student.cohort_id = _row["s_cohort"]

    instructor = None
    if _row["instructor_id"] is not None:
        instructor = Instructor()
        instructor.id = _row["instructor_id"]
        instructor.first_name = _row["i_first"]
        instructor.last_name = _row["i_last"]
        instructor.slack_handle = _row["i_slack"]
        instructor.specialty = _row["specialty"]
        instructor.cohort_id = _row["i_cohort"]

    return (cohort, student, instructor)

def get_cohort(cohort_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_cohort
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            c.id cohort_id,
            c.name cohort_name,
            s.id student_id,
            s.first_name s_first,
            s.last_name s_last,
            s.slack_handle s_slack,
            s.cohort_id s_cohort,
            i.id instructor_id,
            i.slack_handle i_slack,
            i.specialty,
            i.cohort_id i_cohort,
            u.first_name i_first,
            u.last_name i_last
        FROM exercisesapp_cohort c
        LEFT JOIN exercisesapp_student s ON s.cohort_id = c.id
        LEFT JOIN exercisesapp_instructor i ON i.cohort_id = c.id
        LEFT JOIN auth_user u ON i.user_id = u.id
        WHERE c.id = ?            
        """, (cohort_id,))

        cohort_details = db_cursor.fetchall() 

        this_cohort = None
        for (cohort, student, instructor) in cohort_details:
            if this_cohort is None:
                if student is not None:
                    cohort.students.append(student)
                if instructor is not None:
                    cohort.instructors.append(instructor)
                this_cohort = cohort
            else:
                if student is not None and student not in this_cohort.students:
                    this_cohort.students.append(student)
                if instructor is not None and instructor not in this_cohort.instructors:
                    this_cohort.instructors.append(instructor)
            
        
        return this_cohort

@login_required
def cohort_details(request, cohort_id):
    if request.method == 'GET':
        cohort = get_cohort(cohort_id)

        template = 'cohorts/details.html'

        context = {
            'cohort': cohort
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute(""" 
                UPDATE exercisesapp_cohort
                SET name = ?
                WHERE id = ?
                """,
                (form_data['name'], cohort_id))
            
            return redirect('exercisesapp:cohort', cohort_id)