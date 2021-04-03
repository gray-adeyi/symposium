from django.db import models
from django.contrib.auth import get_user_model
import secrets

# Create your models here.
USER = get_user_model()


class Faculty(models.Model):
    """
    Holds Informations about
    facluties present in the
    university.
    """
    name = models.CharField(max_length=50,)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    """
    `Lecturer` models represents a
    university's Lecturer.
    """
    basic_data = models.ForeignKey(USER, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.basic_data.first_name or "Unidentified Lecturer"


class Department(models.Model):
    """
    Model for all the Departments
    the university has.
    """
    name = models.CharField(blank=True, max_length=100)
    about = models.TextField(blank=True)
    HOD = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    `Student` model represents each university student member
    and holds their data.
    """
    basic_data = models.ForeignKey(USER, on_delete=models.CASCADE,
                                   related_name='student_data')
    matric_no = models.CharField(blank=True, max_length=10)
    reg_no = models.CharField(blank=True, max_length=10)
    is_governor = models.BooleanField(default=False,
                                      help_text='Flag to indicate that \
                                      the student is a class governor')
    is_deputy = models.BooleanField(default=False,
                                    help_text='Flag to indicate that \
                                    the student is a class deputy')
    school_email = models.EmailField(blank=True)
    is_activated = models.BooleanField(default=False)
    link = models.SlugField(blank = True)

    def __str__(self):
        return self.basic_data.first_name

    def save(self, *args, **kwargs):
        if self.link is not None:
            self.link = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)


class StudentPhoneNumber(models.Model):
    """
    Holds student phone numbers
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    number = models.CharField(max_length=14,)

    def __str__(self):
        return self.student
