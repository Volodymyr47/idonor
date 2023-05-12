from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from donor.models import Status
from institution.models import Institution
from datetime import datetime


class Profile(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=17, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER)
    birth_date= models.DateField()
    home_addr = models.CharField(max_length=250, blank=True)
    work_addr = models.CharField(max_length=250, blank=True)
    dlm = models.DateTimeField(default=datetime.now)
    inst = models.ForeignKey(Institution, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, to_field='code', null=False, default=2, on_delete=models.CASCADE)

    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created and not User.is_superuser:
        Profile.objects.create(user=instance)
        instance.profile.save()
