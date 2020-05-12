import sqlite3
from django.shortcuts import render, redirect, reverse
from exercisesapp.models import Cohort, model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def cohort_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Cohort)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                c.id,
                c.name
            FROM exercisesapp_cohort c
            ORDER BY c.name
            """)

            all_cohorts = db_cursor.fetchall()

            template_name = 'cohorts/list.html'

            context = {
                'all_cohorts': all_cohorts
            }
        return render(request, template_name, context)
    # elif request.method == 'POST':
    #     form_data = request.POST

    #     with sqlite3.connect(Connection.db_path) as conn:
    #         db_cursor = conn.cursor()

    #         db_cursor.execute("""
    #         INSERT INTO exercisesapp_exercise
    #         (
    #             name, language
    #         )
    #         VALUES (?, ?)
    #         """,
    #         (form_data['name'], form_data['language']))

    #     return redirect(reverse('exercisesapp:exercises'))