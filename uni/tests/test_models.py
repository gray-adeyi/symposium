from django.test import TestCase
from django.contrib.auth import get_user_model
import datetime as dt
from django.utils.timezone import make_aware
from uni import models
from uni import fixtures
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
IMAGE_CONTENT = open(fixtures.IMAGE, 'rb').read()
USER_DATA = {
    'email': 'coyotedevmail@gmail.com',
    'username': 'coyote',
    'first_name': 'John',
    'last_name': 'Doe',
    'password': '1cleanCode!',
    'confirm_password': '1cleanCode!',
}


def set_up_test_data():
    faculty = models.Faculty.objects.create(name='engineering',
                                            about='lorem ipsum')
    basic_data = get_user_model().objects.create(username=USER_DATA[
                                                    'username'],
                                                 first_name=USER_DATA[
                                                    'first_name'],
                                                 last_name=USER_DATA[
                                                    'last_name'],
                                                 email=USER_DATA[
                                                    'email'],
                                                 password=USER_DATA[
                                                    'password'])
    hod = models.Lecturer.objects.create(basic_data=basic_data)
    department = models.Department.objects.create(faculty=faculty,
                                                  name='electrical \
                                                  engineering',
                                                  about='department of \
                                                  elect/elect',
                                                  HOD=hod)
    course = models.Course.objects.create(faculty=faculty,
                                          department=department,
                                          code="MAT-101",
                                          name="Algebraic mathematics",
                                          poster_image=SimpleUploadedFile(
                                                    name='test_image.jpg',
                                                    content=IMAGE_CONTENT,
                                                    content_type='image/jpeg')
                                          )
    symposium = models.Symposium.objects.create(department=department,
                                                name='Test Class Group',
                                                level='100',
                                                about="An awesome test class \
                                                    group.",
                                                poster_image=SimpleUploadedFile(
                                                          name='test_image.jpg',
                                                          content=IMAGE_CONTENT,
                                                          content_type='image/jpeg')
                                                )
    symposium_broadcast = models.SymposiumBroadcast.objects.create(
                                                        symposium=symposium,
                                                        message='hello ami!',
                                                        message_from='G'
                                                        )

    offered_course = models.OfferedCourse.objects.create(
                                                         symposium=symposium,
                                                         course=course,
                                                         unit=3
                                                         )

    assignment = models.Assignment.objects.create(
            symposium=symposium,
            course=offered_course,
            questions="What do you love?",
            submission_date=make_aware(dt.datetime.now() + dt.timedelta(days=1))

    )
    time_table = models.Timetable.objects.create(
        symposium=symposium
    )
    time_table_unit = models.TimetableUnit.objects.create(
        timetable=time_table,
        course=offered_course,
        unit_type='L',
        date_time=make_aware(dt.datetime.now() + dt.timedelta(days=1)),
        duration=dt.timedelta(hours=2)
    )

    faq = models.FAQ.objects.create(
        symposium=symposium,
        question="What is worth while?",
        answer="Giving back"
    )

    student = models.Student.objects.create(
        member_of=symposium,
        basic_data=basic_data
    )

    student_phone_number = models.StudentPhoneNumber.objects.create(
        student=student,
        number='09059438568'
    )

    return {
        'faculty': faculty,
        'user': basic_data,
        'lecturer': hod,
        'department': department,
        'course': course,
        'symposium': symposium,
        'symposium_broadcast': symposium_broadcast,
        'offered_course': offered_course,
        'assignment': assignment,
        'time_table': time_table,
        'time_table_unit': time_table_unit,
        'faq': faq,
        'student': student,
        'student_phone_number': student_phone_number,

    }


class ModelTestMixin:
    def _test_label(self, model, field, expected_label):
        model_instance = model.objects.get(id=1)
        field_label = model_instance._meta.get_field(field).verbose_name
        self.assertEqual(field_label, expected_label)


class FacultyModelTest(ModelTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Faculty
        self._test_label(model, 'name', 'name')
        self._test_label(model, 'about', 'about')


class TestLecturerModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
                                                    username=USER_DATA[
                                                        'username'],
                                                    first_name=USER_DATA[
                                                        'first_name'],
                                                    last_name=USER_DATA[
                                                        'last_name'],
                                                    email=USER_DATA[
                                                        'email'],
                                                    password=USER_DATA[
                                                        'password'])
        models.Lecturer.objects.create(basic_data=user)

    def test_labels(self):
        model = models.Lecturer
        self._test_label(model, 'basic_data', 'basic data')


class TestDepartmentModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(self):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Department
        self._test_label(model, 'faculty', 'faculty')
        self._test_label(model, 'name', 'name')
        self._test_label(model, 'about', 'about')
        self._test_label(model, 'HOD', 'HOD')


class TestCourseModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(self):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Course
        self._test_label(model, 'faculty', 'faculty')
        self._test_label(model, 'department', 'department')
        self._test_label(model, 'code', 'code')
        self._test_label(model, 'name', 'name')
        self._test_label(model, 'about', 'about')
        self._test_label(model, 'poster_image', 'poster image')


class TestSymposiumModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Symposium
        self._test_label(model, 'department', 'department')
        self._test_label(model, 'name', 'name')
        self._test_label(model, 'level', 'level')
        self._test_label(model, 'about', 'about')
        self._test_label(model, 'poster_image', 'poster image')
        self._test_label(model, 'created_on', 'created on')
        self._test_label(model, 'updated_on', 'updated on')


class TestSymposiumBroadcastModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.SymposiumBroadcast
        self._test_label(model, 'symposium', 'symposium')
        self._test_label(model, 'message', 'message')
        self._test_label(model, 'message_from', 'message from')
        self._test_label(model, 'created_on', 'created on')
        self._test_label(model, 'archive', 'archive')


class TestOfferedCourseModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.OfferedCourse
        self._test_label(model, 'symposium', 'symposium')
        self._test_label(model, 'course', 'course')
        self._test_label(model, 'unit', 'unit')


class TestAssignmentModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Assignment
        self._test_label(model, 'symposium', 'symposium')
        self._test_label(model, 'course', 'course')
        self._test_label(model, 'questions', 'questions')
        self._test_label(model, 'submission_date', 'submission date')
        self._test_label(model, 'archive', 'archive')


class TestTimetableModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Timetable
        self._test_label(model, 'symposium', 'symposium')


class TestTimetableUnitModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.TimetableUnit
        self._test_label(model, 'timetable', 'timetable')
        self._test_label(model, 'course', 'course')
        self._test_label(model, 'unit_type', 'unit type')
        self._test_label(model, 'duration', 'duration')
        self._test_label(model, 'archive', 'archive')


class TestFAQModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.FAQ
        self._test_label(model, 'symposium', 'symposium')
        self._test_label(model, 'question', 'question')
        self._test_label(model, 'answer', 'answer')
        self._test_label(model, 'created_on', 'created on')
        self._test_label(model, 'updated_on', 'updated on')


class TestStudentModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.Student
        self._test_label(model, 'member_of', 'member of')
        self._test_label(model, 'basic_data', 'basic data')
        self._test_label(model, 'matric_no', 'matric no')
        self._test_label(model, 'reg_no', 'reg no')
        self._test_label(model, 'is_governor', 'is governor')
        self._test_label(model, 'is_deputy', 'is deputy')
        self._test_label(model, 'school_email', 'school email')
        self._test_label(model, 'is_activated', 'is activated')
        self._test_label(model, 'link', 'link')
        self._test_label(model, 'address', 'address')
        self._test_label(model, 'gender', 'gender')
        self._test_label(model, 'religion', 'religion')
        self._test_label(model, 'dob', 'dob')
        self._test_label(model, 'bio', 'bio')
        self._test_label(model, 'passport_photograph', 'passport photograph')
        self._test_label(model, 'profile_picture', 'profile picture')
        self._test_label(model, 'signature', 'signature')
        self._test_label(model, 'state_of_origin', 'state of origin')


class TestStudentPhoneNumberModel(ModelTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = set_up_test_data()

    def test_labels(self):
        model = models.StudentPhoneNumber
        self._test_label(model, 'student', 'student')
        self._test_label(model, 'number', 'number')
