from django.db import models
from .cohort import Cohort

class Student(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slack_handle = models.CharField(max_length=50)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Student")
        verbose_name_plural = ("Students")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})
