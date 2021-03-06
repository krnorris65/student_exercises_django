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

def get_students(request, exercise_id):
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
        JOIN exercisesapp_instructor i ON i.cohort_id = s.cohort_id
        WHERE i.id = ? AND s.id NOT IN (
            SELECT
                s.id
            FROM exercisesapp_student s
            LEFT JOIN exercisesapp_assignment a ON a.student_id = s.id
            WHERE a.exercise_id =?
        )
        ORDER BY s.last_name
        """, (request.user.instructor.id, exercise_id))

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
        students = get_students(request, exercise_id)
        template = 'exercises/assignment_form.html'
        context = {
            'all_students': students,
            'exercise': exercise
        }

        return render(request, template, context)