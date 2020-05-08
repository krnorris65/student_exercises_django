import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Instructor, Student, Exercise
from ..connection import Connection

def create_exercise(cursor, row):
    _row = sqlite3.Row(cursor, row)

    exercise = Exercise()
    exercise.id = _row["exercise_id"]
    exercise.name = _row["exercise_name"]
    exercise.language = _row["language"]

    exercise.assignments = []

    assignment = None
    if _row["student_id"] is not None:
        student = Student()
        student.id = _row["student_id"]
        student.first_name = _row["s_first"]
        student.last_name = _row["s_last"]
        student.slack_handle = _row["s_slack"]
        student.cohort_id = _row["s_cohort"]

        instructor = Instructor()
        instructor.id = _row["instructor_id"]
        instructor.first_name = _row["i_first"]
        instructor.last_name = _row["i_last"]
        instructor.slack_handle = _row["i_slack"]
        instructor.specialty = _row["specialty"]
        instructor.cohort_id = _row["i_cohort"]


        assignment = (student, instructor)

    return (exercise, assignment)

def get_exercise(exercise_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_exercise
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            e.id exercise_id,
            e.name exercise_name,
            e.language,
            s.id student_id,
            s.first_name s_first,
            s.last_name s_last,
            s.slack_handle s_slack,
            s.cohort_id s_cohort,
            i.id instructor_id,
            i.slack_handle i_slack,
            i.specialty,
            i.cohort_id i_cohort,
            u.first_name i_first,
            u.last_name i_last
        FROM exercisesapp_exercise e
        LEFT JOIN exercisesapp_assignment a ON a.exercise_id = e.id
        LEFT JOIN exercisesapp_student s ON a.student_id = s.id
        LEFT JOIN exercisesapp_instructor i ON a.instructor_id = i.id
        LEFT JOIN auth_user u ON i.user_id = u.id
        WHERE e.id = ?            
        """, (exercise_id,))

        exercise_assignments = db_cursor.fetchall() 

        this_exercise = None
        for (exercise, assignment) in exercise_assignments:
            if this_exercise is None:
                if assignment is not None:
                    exercise.assignments.append(assignment)
                this_exercise = exercise
            else:
                this_exercise.assignments.append(assignment)
            
        
        return this_exercise

def exercise_details(request, exercise_id):
    if request.method == 'GET':
        exercise = get_exercise(exercise_id)

        template = 'exercises/details.html'

        context = {
            'exercise': exercise
        }

        return render(request, template, context)