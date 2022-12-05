from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Course(models.Model):
    name=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Level(models.Model):
    level_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.level_name


class Session_Year(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

    def __str__(self):
        return self.session_start + " to " + self.session_end

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address= models.TextField()
    gender = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    level_id = models.ForeignKey(Level, on_delete=models.DO_NOTHING)
    session_year = models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address= models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name

class Subject(models.Model):
    name=models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Staff_Notification(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.staff.admin.first_name

class Leave_Application(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=100)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.staff.admin.first_name + " " + self.staff.admin.last_name

class Student_Leave(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=100)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.student.admin.first_name + " " + self.student.admin.last_name


class Feedback(models.Model):
    staff=models.ForeignKey(Staff, on_delete=models.CASCADE)
    subject = models.TextField()
    message = models.TextField()
    reply = models.TextField(default='No reply yet')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff.admin.first_name + " " + self.staff.admin.last_name

class Attendance(models.Model):    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.admin.first_name + " " + self.student.admin.last_name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, default=0)
    possible_marks = models.IntegerField(null=True, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.admin.first_name + " " + self.student.admin.last_name

class GeneralNotification(models.Model):
    sender = models.ForeignKey(Staff, on_delete=models.CASCADE)    
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    motive = models.CharField(max_length=100, default='Feedback')
    status = models.CharField(max_length=100, default='Unvisited')

    def __str__(self):
        return self.sender.admin.first_name + " " + self.sender.admin.last_name + " - " + self.motive







