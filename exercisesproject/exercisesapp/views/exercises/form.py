import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from exercisesapp.models import Exercise, model_factory

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