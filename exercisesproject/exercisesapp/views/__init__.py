from .home import home
from .auth.logout import logout_user
from .instructors.list import instructor_list
from .instructors.details import instructor_details
from .instructors.form import instructor_edit_form

from .students.list import student_list
from .students.details import student_details
from .students.form import student_form
from .students.form import student_edit_form

from .exercises.list import exercise_list
from .exercises.details import exercise_details
from .exercises.details import delete_assignment
from .exercises.form import exercise_form
from .exercises.form import exercise_edit_form
from .exercises.form import assignment_form

from .cohorts.list import cohort_list
from .cohorts.details import cohort_details
from .cohorts.form import cohort_form
from .cohorts.form import cohort_edit_form