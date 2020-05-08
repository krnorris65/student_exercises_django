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

            grouped_exercises = {}

            for exercise in all_exercises:
                if exercise.language not in grouped_exercises:

                    grouped_exercises[exercise.language] = {
                        "language": exercise.language,
                        "exercise_list": [exercise]
                    }
                else:
                    grouped_exercises[exercise.language]["exercise_list"].append(exercise)

            template_name = 'exercises/list.html'

            context = {
                'all_exercises': grouped_exercises.values()
            }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO exercisesapp_exercise
            (
                name, language
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['language']))

        return redirect(reverse('exercisesapp:exercises'))