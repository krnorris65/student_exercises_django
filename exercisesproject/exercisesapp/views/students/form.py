import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from exercisesapp.models import Cohort, Student, model_factory

def get_student(student_id):
    with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Student)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                s.id,
                s.first_name,
                s.last_name,
                s.slack_handle,
                s.cohort_id
            FROM exercisesapp_student s
            WHERE s.id = ?            
            """, (student_id,))

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

def student_form(request):
    if request.method == 'GET':
        cohorts = get_cohorts()

        template = 'students/form.html'
        context = {
            'all_cohorts': cohorts
        }

        return render(request, template, context)

def student_edit_form(request, student_id):
    if request.method == 'GET':
        student = get_student(student_id)
        cohorts = get_cohorts()

        template = 'students/form.html'
        context = {
            'student': student,
            'all_cohorts': cohorts
        }

        return render(request, template, context)