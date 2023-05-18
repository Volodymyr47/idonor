from datetime import datetime
from django.db import models


class Status(models.Model):
    code = models.IntegerField(null=False, unique=True)
    value = models.CharField(max_length=30)
    dlm = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.value


class Institution(models.Model):
    full_name = models.CharField(max_length=250, null=False, default='InstitutionName')
    short_name = models.CharField(max_length=80, null=True)
    address = models.CharField(max_length=250, null=True)
    corporate_phone = models.CharField(max_length=20, null=True)
    status = models.ForeignKey(Status, to_field='code', null=False, default=2, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)
    status = models.ForeignKey(Status, to_field='code', null=False, default=2, on_delete=models.CASCADE)
    dlm = models.DateTimeField(default=datetime.today)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    dlm = models.DateTimeField(default=datetime.today)
    status = models.ForeignKey(Status, to_field='code', null=False, default=2, on_delete=models.CASCADE)

    def __str__(self):
        return self.text