from django.urls import include, path
from .views import *

app_name = "exercisesapp"

urlpatterns = [
    path('', home, name='home'),
    path('instructors/', instructor_list, name="instructors")
]
