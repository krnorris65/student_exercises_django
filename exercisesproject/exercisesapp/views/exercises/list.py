import sqlite3
from django.shortcuts import render, redirect, reverse
from exercisesapp.models import Exercise, model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

def exercise_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Exercise)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                e.id,
                e.name,
                e.language
            FROM exercisesapp_exercise e
            ORDER BY e.language, e.name
            """)

            all_exercises = db_cursor.fetchall()

            template_name = 'exercises/list.html'

            context = {
                'all_exercises': all_exercises
            }
        return render(request, template_name, context)