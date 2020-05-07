import sqlite3
from django.shortcuts import render, redirect, reverse
from exercisesapp.models import Student, model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

def student_list(request):
    if request.method == 'GET':
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

            all_students = db_cursor.fetchall()

            template_name = 'students/list.html'

            context = {
                'all_students': all_students
            }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO exercisesapp_student
            (
                first_name, last_name, slack_handle,
                cohort_id
            )
            VALUES (?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'],
                form_data['slack_handle'], form_data['cohort']))

        return redirect(reverse('exercisesapp:students'))