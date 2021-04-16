from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Faculty)
admin.site.register(models.Department)
admin.site.register(models.Symposium)
admin.site.register(models.FAQ)
admin.site.register(models.Course)
admin.site.register(models.Assignment)
admin.site.register(models.OfferedCourse)
admin.site.register(models.Timetable)
admin.site.register(models.TimetableUnit)
