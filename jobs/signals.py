from django.db.models.signals import pre_save, post_save

from .models import MALRequirement, MicroTask


def make_microtask_not_available_when_selected(sender, instance, created, *args, **kwargs):
    if created:
        microtask_id = instance.micro_task.id
        MicroTask.objects.filter(id=microtask_id).update(is_selected=True)


post_save.connect(make_microtask_not_available_when_selected, sender=MALRequirement)