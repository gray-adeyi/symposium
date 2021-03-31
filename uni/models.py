from django.db import models

# Create your models here.


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


class Department(models.Model):
    """
    Model for all the Departments
    the university has.
    """
    name = models.CharField(blank=True, max_length=100)
    about = models.TextField(blank=True)
    HOD = models.ForeignKey(Lecturer, on_delete=models.SET_NULL)
