from django.dispatch import receiver
from .models import Users,Doctors
from django.db.models.signals import post_save

@receiver(post_save,sender=Users)
def creating_doctor_instance(sender,instance,created,*args,**kwargs):
    if created and instance.is_doctor:
        Doctors.objects.create(user=instance)