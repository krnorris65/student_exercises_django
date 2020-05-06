from django.urls import include, path
from .views import *

app_name = "exercisesapp"

urlpatterns = [
    path('', home, name='home'),
    path('instructors/', instructor_list, name="instructors"),
    path('instructors/<int:instructor_id>/edit/', instructor_edit_form, name="instructor_edit_form"),
    path('instructors/<int:instructor_id>/', instructor_details, name="instructor")
]
