import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Cohort, Student, Exercise
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
    cohort.name = _row["cohort_name"]

    student.cohort = cohort

    student.exercises = []

    exercise = Exercise()
    exercise.id = _row["exercise_id"]
    exercise.name = _row["exercise_name"]
    exercise.language = _row["language"]


    return  (student, exercise)

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
            c.name cohort_name,
            e.id exercise_id,
            e.name exercise_name,
            e.language
        FROM exercisesapp_student s
        JOIN exercisesapp_cohort c ON c.id = s.cohort_id
        JOIN exercisesapp_assignment a ON a.student_id = s.id
        JOIN exercisesapp_exercise e ON e.id = a.exercise_id
        WHERE s.id = ?            
        """, (student_id,))

        student_assignments = db_cursor.fetchall() 

        this_student = None

        for (s, exercise) in student_assignments:
            if this_student is None:
                s.exercises.append(exercise)
                this_student = s
            else:
                this_student.exercises.append(exercise)
            
        
        return this_student


def student_details(request, student_id):
    if request.method == 'GET':
        student = get_student(student_id)

        template = 'students/details.html'

        context = {
            'student': student
        }

        return render(request, template, context)
    if request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute(""" 
                UPDATE exercisesapp_student
                SET first_name = ?,
                last_name = ?,
                slack_handle = ?,
                cohort_id = ?
                WHERE id = ?
                """,
                (form_data['first_name'], form_data['last_name'], form_data['slack_handle'], form_data['cohort'], student_id))
            
            return redirect('exercisesapp:student', student_id)
        
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM exercisesapp_student
                    WHERE id = ?
                """, (student_id,))

            return redirect(reverse('exercisesapp:students'))
