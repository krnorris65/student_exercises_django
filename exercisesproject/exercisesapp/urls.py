from django.urls import include, path
from .views import *

app_name = "exercisesapp"

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('instructors/', instructor_list, name="instructors"),
    path('instructors/<int:instructor_id>/edit/', instructor_edit_form, name="instructor_edit_form"),
    path('instructors/<int:instructor_id>/', instructor_details, name="instructor"),
    path('students/', student_list, name="students"),
    path('students/<int:student_id>/', student_details, name="student"),
    path('students/new/', student_form, name="student_form"),
    path('students/<int:student_id>/edit/', student_edit_form, name="student_edit_form"),
    path('exercises/', exercise_list, name="exercises"),
    path('exercises/<int:exercise_id>/', exercise_details, name="exercise"),
    path('exercises/new/', exercise_form, name="exercise_form"),
    path('exercises/<int:exercise_id>/edit/', exercise_edit_form, name="exercise_edit_form"),
    path('cohorts/', cohort_list, name="cohorts"),
    path('cohorts/<int:cohort_id>/', cohort_details, name="cohort"),
    path('cohorts/new/', cohort_form, name="cohort_form"),
    path('cohorts/<int:cohort_id>/edit/', cohort_edit_form, name="cohort_edit_form"),
    path('exercises/<int:exercise_id>/assign', assignment_form, name="assignment_form"),

]
