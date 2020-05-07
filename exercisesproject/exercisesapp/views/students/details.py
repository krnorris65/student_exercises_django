import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Cohort, Student
from ..connection import Connection

def create_student(cursor, row):
    _row = sqlite3.Row(cursor, row)

    student = Student()
    student.id = _row["student_id"]
    student.first_name = _row["first_name"]
    student.last_name = _row["last_name"]
    student.slack_handle = _row["slack_handle"]

    cohort = Cohort()
    cohort.id = _row["cohort_id"]
    cohort.name = _row["name"]

    student.cohort = cohort

    return  student

def get_student(student_id):
    with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_student
            db_cursor = conn.cursor()

            db_cursor.execute(""" 
            SELECT
                s.id student_id,
                s.first_name,
                s.last_name,
                s.slack_handle,
                s.cohort_id,
                c.name
            FROM exercisesapp_student s
            JOIN exercisesapp_cohort c ON c.id = s.cohort_id
            WHERE s.id = ?            
            """, (student_id,))

            return db_cursor.fetchone() 

def student_details(request, student_id):
    if request.method == 'GET':
        student = get_student(student_id)

        template = 'students/details.html'

        context = {
            'student': student
        }

        return render(request, template, context)
