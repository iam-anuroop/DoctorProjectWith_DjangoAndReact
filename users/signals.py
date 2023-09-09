from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctors,Users


@receiver(post_save,sender=Users)
def DocCreate(sender,instance,created,*args,**kwargs):
    if created and instance.is_doctor:
        Doctors.objects.create(
            user = instance
        )

