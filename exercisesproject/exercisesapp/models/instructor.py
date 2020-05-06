from django.db import models
from .cohort import Cohort
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Instructor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slack_handle = models.CharField(max_length=50, null=True)
    specialty = models.CharField(max_length=50, null=True)
    cohort = models.ForeignKey(Cohort, null=True, blank=True,on_delete=models.CASCADE)


    @receiver(post_save, sender=User)
    def create_instructor(sender, instance, created, **kwargs):
        if created:
            Instructor.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_instructor(sender, instance, **kwargs):
        instance.instructor.save()
