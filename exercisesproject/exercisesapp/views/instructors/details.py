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


def instructor_details(request, instructor_id):
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
        JOIN exercisesapp_cohort c ON i.cohort_id = c.id
        WHERE i.id = ?
        """, (instructor_id,))

        instructor = db_cursor.fetchone()

        template = 'instructors/details.html'
        context = {
            'instructor': instructor
        }

        return render(request, template, context)