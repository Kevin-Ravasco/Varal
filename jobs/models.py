from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MicroTask(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_selected = models.BooleanField(default=False)
    is_allocated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True) # the date the job was created

    def __str__(self):
        return self.name


class MALRequirement(models.Model):
    micro_task = models.ForeignKey(MicroTask, on_delete=models.CASCADE, limit_choices_to={'is_selected': False})

    def __str__(self):
        return self.micro_task.name


class AllocatedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    outsource_email = models.EmailField()
    time_allocated = models.DateTimeField(auto_now_add=True)
    time_completed = models.DateTimeField(blank=True, null=True)

