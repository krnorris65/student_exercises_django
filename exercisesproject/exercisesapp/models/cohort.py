from django.db import models

class Cohort(models.Model):

    name = models.CharField(max_length=50)
    

    class Meta:
        verbose_name = ("cohort")
        verbose_name_plural = ("cohorts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cohort_detail", kwargs={"pk": self.pk})
