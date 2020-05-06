from django.db import models
from .exercise import Exercise
from .instructor import Instructor
from .student import Student

class Assignment(models.Model):

    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    instructor = models.ForeignKey("Instructor", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("assignment")
        verbose_name_plural = ("assignments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("assignment_detail", kwargs={"pk": self.pk})
