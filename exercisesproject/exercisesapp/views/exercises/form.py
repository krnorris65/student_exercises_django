import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from exercisesapp.models import Exercise, Student, model_factory

def get_exercise(exercise_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Exercise)
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            e.id,
            e.name,
            e.language
        FROM exercisesapp_exercise e
        WHERE e.id = ?            
        """, (exercise_id,))

        return db_cursor.fetchone()

def get_students():
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
        ORDER BY s.last_name 
        """)

        return db_cursor.fetchall()

@login_required
def exercise_form(request):
    if request.method == 'GET':

        template = 'exercises/form.html'
        context = {}

        return render(request, template, context)

@login_required
def exercise_edit_form(request, exercise_id):
    if request.method == 'GET':
        exercise = get_exercise(exercise_id)

        template = 'exercises/form.html'
        context = {
            'exercise': exercise
        }

        return render(request, template, context)

@login_required
def assignment_form(request, exercise_id):
    if request.method == 'GET':
        exercise = get_exercise(exercise_id)
        students = get_students()
        template = 'exercises/assignment_form.html'
        context = {
            'all_students': students,
            'exercise': exercise
        }

        return render(request, template, context)