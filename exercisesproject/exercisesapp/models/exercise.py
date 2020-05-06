from django.db import models

class Exercise(models.Model):

    name = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    

    class Meta:
        verbose_name = ("exercise")
        verbose_name_plural = ("exercises")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exercise_detail", kwargs={"pk": self.pk})
