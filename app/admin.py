from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Leave_Application)
admin.site.register(Feedback)
admin.site.register(Level)
admin.site.register(Attendance)
admin.site.register(Grade)
admin.site.register(GeneralNotification)
admin.site.register(Student_Leave)