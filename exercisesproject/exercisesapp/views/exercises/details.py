import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exercisesapp.models import Instructor, Student, Exercise, Assignment
from ..connection import Connection

def create_exercise(cursor, row):
    _row = sqlite3.Row(cursor, row)

    exercise = Exercise()
    exercise.id = _row["exercise_id"]
    exercise.name = _row["exercise_name"]
    exercise.language = _row["language"]

    exercise.assignments = []

    assignment = None
    if _row["assignment_id"] is not None:
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

        assignment = Assignment()
        assignment.id = _row["assignment_id"]
        assignment.instructor = instructor
        assignment.student = student
        assignment.exercise = exercise


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
            u.last_name i_last,
            a.id assignment_id
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

@login_required
def exercise_details(request, exercise_id):
    if request.method == 'GET':
        exercise = get_exercise(exercise_id)

        template = 'exercises/details.html'

        context = {
            'exercise': exercise
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        # updates exercise
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute(""" 
                UPDATE exercisesapp_exercise
                SET name = ?,
                language = ?
                WHERE id = ?
                """,
                (form_data['name'], form_data['language'], exercise_id))
            
            return redirect('exercisesapp:exercise', exercise_id)
        # deletes exercise
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM exercisesapp_exercise
                    WHERE id = ?
                """, (exercise_id,))

            return redirect(reverse('exercisesapp:exercises'))

        # creates assignment
        if (
            "actual_resource" in form_data
            and form_data["actual_resource"] == "assignment"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO exercisesapp_assignment
                (
                    exercise_id, student_id, instructor_id
                )
                VALUES (?, ?, ?)
                """,
                (exercise_id, form_data['student'], request.user.instructor.id))

            return redirect('exercisesapp:exercise', exercise_id)

def delete_assignment(request, assignment_id, exercise_id):
    if request.method == 'POST':
        form_data = request.POST
        if (
            "actual_resource" in form_data
            and form_data["actual_resource"] == "assignment"
            and "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            # exercise_id is actually the assignment_id
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM exercisesapp_assignment
                    WHERE id = ?
                """, (assignment_id,))
            return redirect('exercisesapp:exercise', exercise_id)