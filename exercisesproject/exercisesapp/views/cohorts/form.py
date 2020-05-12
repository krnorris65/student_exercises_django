import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from exercisesapp.models import Cohort, model_factory

def get_cohort(cohort_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Cohort)
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            c.id,
            c.name
        FROM exercisesapp_cohort c
        WHERE c.id = ?            
        """, (cohort_id,))

        return db_cursor.fetchone() 

@login_required
def cohort_form(request):
    if request.method == 'GET':

        template = 'cohorts/form.html'
        context = {}

        return render(request, template, context)

@login_required
def cohort_edit_form(request, cohort_id):
    if request.method == 'GET':
        cohort = get_cohort(cohort_id)

        template = 'cohorts/form.html'
        context = {
            'cohort': cohort
        }

        return render(request, template, context)