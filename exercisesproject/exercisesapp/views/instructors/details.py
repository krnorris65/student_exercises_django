import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Cohort, Instructor
from ..connection import Connection

def create_instructor(cursor, row):
    _row = sqlite3.Row(cursor, row)

    instructor = Instructor()
    instructor.id = _row["instructor_id"]
    instructor.first_name = _row["first_name"]
    instructor.last_name = _row["last_name"]
    instructor.slack_handle = _row["slack_handle"]
    instructor.specialty = _row["specialty"]

    cohort = Cohort()
    cohort.id = _row["cohort_id"]
    cohort.name = _row["name"]

    instructor.cohort = cohort

    return instructor

def get_instructor(instructor_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_instructor
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            i.id instructor_id,
            i.slack_handle,
            i.specialty,
            i.cohort_id,
            u.first_name,
            u.last_name,
            c.name
        FROM exercisesapp_instructor i 
        JOIN auth_user u ON i.user_id = u.id
        LEFT JOIN exercisesapp_cohort c ON i.cohort_id = c.id
        WHERE i.id = ?
        """, (instructor_id,))

        return db_cursor.fetchone()

def instructor_details(request, instructor_id):
    if request.method == 'GET':
        instructor = get_instructor(instructor_id)

        template = 'instructors/details.html'
        context = {
            'instructor': instructor
        }

        return render(request, template, context)
    if request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                cohort = form_data['cohort']
                slack = form_data['slack_handle']
                specialty = form_data['specialty']


                # if these fields are empty save them as NULL values in database, not EMPTY values
                if cohort == "":
                    cohort = None
                if slack == "":
                    slack = None
                if specialty == "":
                    specialty = None

                db_cursor.execute("""
                UPDATE exercisesapp_instructor
                SET cohort_id = ?,
                    slack_handle = ?,
                    specialty = ?
                WHERE id = ?
                """,
                (cohort, slack, specialty, instructor_id,))

                db_cursor.execute("""
                UPDATE auth_user
                SET first_name = ?,
                    last_name = ?
                WHERE id = (SELECT user_id 
                    FROM exercisesapp_instructor 
                    WHERE id = ?)
                """,
                (
                    form_data['first_name'], form_data['last_name'], instructor_id,
                ))

            return redirect('exercisesapp:instructor', instructor_id)