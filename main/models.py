from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AdvisorProfile(models.Model):
    instructor_name = models.CharField(max_length=255, default="")
    username = models.CharField(max_length=255)
    advisor_email = models.CharField(max_length=255)
    advisor_subject = models.CharField(max_length=255)

    def __str__(self):
        return self.instructor_name


class AllSubjects(models.Model):
    subject = models.CharField(max_length=100)
    descr = models.CharField(max_length=100)
    acad_groups = models.CharField(max_length=100)
    careers = models.CharField(max_length=100)
    campuses = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class SubjectClasses(models.Model):
    index = models.IntegerField(null=True)
    crse_id = models.IntegerField(null=True)
    strm = models.IntegerField(null=True)
    session_code = models.CharField(max_length=100, null=True)
    class_section = models.CharField(max_length=100, null=True)
    class_nbr = models.IntegerField(null=True)
    component = models.CharField(max_length=100, null=True)
    isLecture = models.BooleanField(default=True)
    subject = models.CharField(max_length=100, null=True)
    catalog_nbr = models.CharField(max_length=100, null=True)
    acad_group = models.CharField(max_length=100, null=True)
    class_capacity = models.IntegerField(null=True)
    enrollment_total = models.IntegerField(null=True)
    enrollment_available = models.IntegerField(null=True)
    descr = models.TextField(null=True)
    start_time = models.CharField(max_length=100, null=True)
    end_time = models.CharField(max_length=100, null=True)
    days = models.CharField(max_length=100, null=True)
    facility_id = models.CharField(max_length=100, null=True)
    instructor = models.CharField(max_length=100, null=True)
    instructor_email = models.CharField(max_length=100, null=True)
    page = models.IntegerField(null=True)

    def __str__(self):
        return self.descr


class Cart(models.Model):
    username = models.TextField()
    num_credits = models.IntegerField()
    num_classes = models.IntegerField()
    classes = models.ManyToManyField(SubjectClasses)

    def __str__(self):
        return self.username


class Schedule(models.Model):
    username = models.TextField()
    classes = models.ManyToManyField(SubjectClasses)
    is_approved = models.BooleanField(null=True, default=None)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    username = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255, null=True)
    user_major = models.CharField(max_length=255, default="N/C")
    advisor = models.ForeignKey(
        AdvisorProfile, null=True, related_name='advisor_users', on_delete=models.SET_NULL)
    schedules = models.ManyToManyField(Schedule)

    def __str__(self):
        return self.username
