from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from institution.models import Question


class Status(models.Model):
    code = models.IntegerField(null=False, unique=True)
    value = models.CharField(max_length=30)
    dlm = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.value


class Answer(models.Model):
    question = models.ManyToManyField(Question)
    donor = models.ManyToManyField(User)
    answer = models.CharField(max_length=250)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.answer


class Test(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateField()
    result = models.CharField(max_length=250)
    result_date = models.DateField()
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.result


class History(models.Model):
    donor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_date = models.DateField()
    comment = models.CharField(max_length=250)
    dlm = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.donor_id} have donated in {self.donation_date}'


# class Profile(models.Model):
#     GENDER = (
#         ('male', 'male'),
#         ('female', 'female')
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=17, blank=True)
#     gender = models.CharField(max_length=6, choices=GENDER)
#     birth_date= models.DateField()
#     home_addr = models.CharField(max_length=250, blank=True)
#     work_addr = models.CharField(max_length=250, blank=True)
#     dlm = models.DateTimeField(default=datetime.now)
#     inst = models.ForeignKey(Institution, on_delete=models.CASCADE)
#     status = models.ForeignKey(Status, to_field='code', null=False, default=2, on_delete=models.CASCADE)
#
#     signup_confirmation = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.name
#
#
# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created and not User.is_superuser:
#         Profile.objects.create(user=instance)
#         instance.profile.save()
