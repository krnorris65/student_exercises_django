import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from exercisesapp.models import Cohort, Instructor, model_factory

def get_instructor(instructor_id):
    with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Instructor)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                i.id,
                i.slack_handle,
                i.specialty,
                i.cohort_id,
                u.first_name,
                u.last_name
                FROM exercisesapp_instructor i 
            JOIN auth_user u ON i.user_id = u.id
            WHERE i.id = ?
            """, (instructor_id,))

            return db_cursor.fetchone()

def get_cohorts():
    with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Cohort)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                c.id,
                c.name
            FROM exercisesapp_cohort c 
            """)

            return db_cursor.fetchall()

def instructor_edit_form(request, instructor_id):

    if request.method == 'GET':
        instructor = get_instructor(instructor_id)
        cohorts = get_cohorts()

        template = 'instructors/form.html'
        context = {
            'instructor': instructor,
            'all_cohorts': cohorts
        }

        return render(request, template, context)