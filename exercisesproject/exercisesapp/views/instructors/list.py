import sqlite3
from django.shortcuts import render, redirect, reverse
from exercisesapp.models import Instructor, model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def instructor_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Instructor)
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                i.id,
                i.slack_handle,
                i.specialty,
                i.cohort_id,
                i.user_id,
                u.first_name,
                u.last_name
            FROM exercisesapp_instructor i 
            JOIN auth_user u ON i.user_id = u.id
            ORDER BY u.last_name 
            """)

            all_instructors = db_cursor.fetchall()

            template_name = 'instructors/list.html'

            context = {
                'all_instructors': all_instructors
            }
        return render(request, template_name, context)