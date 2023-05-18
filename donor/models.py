from datetime import datetime
from django.db import models
from institution.models import Question
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from institution.models import Institution


User = get_user_model()


class Status(models.Model):
    code = models.IntegerField(null=False, unique=True)
    value = models.CharField(max_length=30)
    dlm = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.value


class Profile(models.Model):
    GENDER = (
        ('Ч', 'Чоловіча'),
        ('Ж', 'Жіноча')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=17, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER)
    birth_date = models.DateField()
    home_addr = models.CharField(max_length=250, blank=True)
    work_addr = models.CharField(max_length=250, blank=True)
    dlm = models.DateTimeField(default=datetime.now)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, to_field='code', null=False, default=1, on_delete=models.CASCADE)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created and not User.is_superuser:
        Profile.objects.create(user=instance)
        instance.profile.save()


class Test(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    result = models.CharField(max_length=500, null=True)
    test_date = models.DateField(default='1900-01-01',null=False)
    status = models.ForeignKey(Status, to_field='code', null=False, default=11, on_delete=models.CASCADE)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.result


class TestDetail(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=250)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.answer


class History(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    donation_date = models.DateField(format('%d.%m.%Y'))
    donated_volume = models.IntegerField(null=True)
    comment = models.CharField(max_length=250)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.profile} donated {self.donated_volume} of blood in {self.donation_date}'


class BloodParameter(models.Model):
    Rh_FACTOR = [
        ('Rh+', 'Rh+'),
        ('Rh-', 'Rh-')
    ]
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, null=True)
    rh_factor = models.CharField(max_length=4, choices=Rh_FACTOR, null=True)
    common_info = models.CharField(max_length=500, null=True)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.profile}, {self.blood_type}, {self.rh_factor}'


class CurrentHealthParameter(models.Model):
    history = models.OneToOneField(History, on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=9, null=True)
    heart_rate = models.IntegerField(null=True)
    hemoglobin = models.IntegerField(null=True)
    common_info = models.CharField(max_length=500, null=True)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.history}, {self.blood_pressure}, {self.heart_rate}, {self.hemoglobin}'
