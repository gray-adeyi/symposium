from django.db import models
from django.contrib.auth import get_user_model
import secrets
import datetime as dt

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

    class Meta:
        verbose_name_plural = "Faculties"


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
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE,
                                related_name='departments')
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    HOD = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True,
                            blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL,
                                related_name='courses', blank=True)
    department = models.ForeignKey(Department, null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='courses', blank=True)
    code = models.CharField(max_length=10, help_text="e.g MAT-101 \
    (all capital letters)")
    name = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    poster_image = models.ImageField(blank=True)

    def __str__(self):
        return self.code


class Symposium(models.Model):
    """
    Ignore it's unusual name. This
    models is models the Class in which
    all students belong to.

    Notice: The class name `Symposium`
    might be deprecated when a better name
    comes along.
    """
    LEVEL_OPTIONS = (
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
        ('500', '500 Level'),
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='classes')
    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=3, choices=LEVEL_OPTIONS)
    about = models.TextField(blank=True)
    poster_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class OfferedCourse(models.Model):
    symposium = models.ForeignKey(Symposium, on_delete=models.CASCADE,
                                  related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.symposium} => {self.course}"


class AssignmentManager(models.Manager):
    def current_and_future(self):
        """
        Archives `Assignment` with
        `submission_date` older than current date and
        filters `Assignment` to return
        those with dates matching the current
        date and future dates.
        """
        old_assigments = self.filter(submission_date__lt=dt.datetime.now())
        for assignment in old_assigments:
            assignment.archive = True
            assignment.save()
        return self.filter(submission_date__gte=dt.datetime.now())


class Assignment(models.Model):
    objects = AssignmentManager()

    symposium = models.ForeignKey(Symposium, on_delete=models.CASCADE,
                                  related_name='assignments')
    course = models.ForeignKey(OfferedCourse, on_delete=models.CASCADE,
                               related_name='assignments')
    questions = models.TextField()
    submission_date = models.DateTimeField()
    archive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.course)


class Timetable(models.Model):
    symposium = models.OneToOneField(Symposium, on_delete=models.CASCADE,
                                     related_name='timetable')

    def __str__(self):
        return str(self.symposium)


class TimetableUnitManager(models.Manager):
    def current_and_future(self):
        """
        Archives `TimetableUnit` with
        date older than current date and
        filters `TimetableUnit` to return
        those with dates matching the current
        date and future dates.
        """
        old_timetable_unit = self.filter(date_time__lt=dt.datetime.now())
        for unit in old_timetable_unit:
            unit.archive = True
            unit.save()
        return self.filter(date_time__gte=dt.datetime.now())


class TimetableUnit(models.Model):
    objects = TimetableUnitManager()
    TYPE_OPTIONS = (
        ('L', 'Lecture'),
        ('T', 'Tutorial'),
        ('E', 'Exam'),
        ('P', 'Practical'),
    )
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE,
                                  related_name='units')
    course = models.ForeignKey(OfferedCourse, on_delete=models.CASCADE,
                               related_name='timetable')
    unit_type = models.CharField(max_length=1, choices=TYPE_OPTIONS)
    date_time = models.DateTimeField()
    duration = models.DurationField(blank=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.timetable)


class FAQ(models.Model):
    symposium = models.ForeignKey(Symposium, on_delete=models.CASCADE,
                                  related_name='faqs')
    question = models.CharField(max_length=100)
    answer = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_on']


class Student(models.Model):
    """
    `Student` model represents each university student member
    and holds their data.
    """
    GENDER_OPTIONS = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('r', 'Rather not say'),
    )

    RELIGION_OPTIONS = (
        ('c', 'Christianity'),
        ('i', 'Islam'),
        ('r', 'Rather not say')
    )

    STATE_OPTIONS = (
        ('abia', 'Abia'),
        ('adamawa', 'Adamawa'),
        ('akwa ibom', 'Akwa Ibom'),
        ('anambra', 'Anambra'),
        ('bauchi', 'Bauchi'),
        ('bayelsa', 'Bayelsa'),
        ('benue', 'Benue'),
        ('borno', 'Borno'),
        ('cross river', 'Cross River'),
        ('delta', 'Delta'),
        ('ebonyi', 'Ebonyi'),
        ('edo', 'Edo'),
        ('ekiti', 'Ekiti'),
        ('enugu', 'Enugu'),
        ('gombe', 'Gombe'),
        ('imo', 'Imo'),
        ('jigawa', 'Jigawa'),
        ('kaduna', 'Kaduna'),
        ('kano', 'Kano'),
        ('katsina', 'Katsina'),
        ('kebbi', 'Kebbi'),
        ('kogi', 'Kogi'),
        ('kwara', 'Kwara'),
        ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'),
        ('niger', 'Niger'),
        ('ogun', 'Ogun'),
        ('ondo', 'Ondo'),
        ('osun', 'Osun'),
        ('oyo', 'Oyo'),
        ('plateau', 'Plateau'),
        ('rivers', 'Rivers'),
        ('sokoto', 'Sokoto'),
        ('taraba', 'Taraba'),
        ('yobe', 'Yobe'),
        ('zamfara', 'Zamfara'),
    )

    member_of = models.ForeignKey(Symposium, on_delete=models.SET_NULL,
                                  null=True, blank=True)
    basic_data = models.OneToOneField(USER, on_delete=models.CASCADE,
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
    link = models.SlugField(blank=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS, blank=True)
    religion = models.CharField(max_length=1, choices=RELIGION_OPTIONS,
                                blank=True)
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    passport_photograph = models.ImageField(blank=True)
    profile_picture = models.ImageField(blank=True)
    signature = models.ImageField(blank=True)
    state_of_origin = models.CharField(max_length=20,
                                       choices=STATE_OPTIONS, blank=True)

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='numbers')
    number = models.CharField(max_length=14,)

    def __str__(self):
        return self.student
