
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    #LOGIN
    path('', views.LOGIN, name='login'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('logout', views.doLogout, name='logout'),

    #PROFILE
    path('profile/', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

    #HOD
    path('Hod/Home', Hod_Views.HOME, name='hod_home'),
    path('Hod/Student/Add', Hod_Views.ADD_STUDENT, name='add_student'),
    path('Hod/Student/View', Hod_Views.VIEW_STUDENTS, name='view_students'),
    path('Hod/Student/View/<str:pk>/', Hod_Views.VIEW_SINGLE_STUDENT, name='view_single_student'),
    path('Hod/Student/Edit/<str:pk>/', Hod_Views.EDIT_STUDENT, name='edit_student'),
    path('Hod/Student/Update', Hod_Views.UPDATE_STUDENT, name='update_student'),
    path('Hod/Student/Delete/<str:admin>/', Hod_Views.DELETE_STUDENT, name='delete_student'),
    path('Hod/Student/View/Download', Hod_Views.DOWNLOAD_STUDENTS, name='download_students' ),
    path('Hod/Student_Leaves', Hod_Views.VIEW_STUDENT_LEAVE_APPLICATIONS, name='student_leaves'),
    path('Hod/Student_Leaves/Approve/<str:status>', Hod_Views.APPROVE_STUDENT_LEAVE, name="approve_student_leave"),
    path('Hod/Student_Leaves/Decline/<str:status>', Hod_Views.DECLINE_STUDENT_LEAVE, name="decline_student_leave"),


    path('Hod/Staff/Add', Hod_Views.ADD_STAFF, name='add_staff'),
    path('Hod/Staff/View', Hod_Views.VIEW_STAFF, name='view_staff'),
    path('Hod/Staff/View/<str:pk>/', Hod_Views.VIEW_SINGLE_STAFF, name='view_single_staff'),
    path('Hod/Staff/Edit/<str:pk>/', Hod_Views.EDIT_STAFF, name='edit_staff'),
    path('Hod/Staff/Update', Hod_Views.UPDATE_STAFF, name='update_staff'),
    path('Hod/Staff/Delete/<str:admin>/', Hod_Views.DELETE_STAFF, name='delete_staff'),
    path('Hod/Staff/View/Download', Hod_Views.DOWNLOAD_STAFF, name = 'download_staff'),


    path('Hod/Course/Add', Hod_Views.ADD_COURSE, name='add_course'),
    path('Hod/Course/View', Hod_Views.VIEW_COURSE, name='view_courses'),
    path('Hod/Course/Edit/<str:id>/', Hod_Views.EDIT_COURSE, name="edit_course"),
    path('Hod/Course/Update', Hod_Views.UPDATE_COURSE, name="update_course"),
    path('Hod/Course/Delete/<str:id>/', Hod_Views.DELETE_COURSE, name='delete_course'),

    path('Hod/Subject/Add', Hod_Views.ADD_SUBJECT, name='add_subject'),
    path('Hod/Subject/View', Hod_Views.VIEW_SUBJECT, name='view_subjects'),
    path('Hod/Subject/Edit/<str:id>/', Hod_Views.EDIT_SUBJECT, name="edit_subject"),
    path('Hod/Subject/Update', Hod_Views.UPDATE_SUBJECT, name="update_subject"),
    path('Hod/Subject/Delete/<str:id>/', Hod_Views.DELETE_SUBJECT, name='delete_subject'),

    path('Hod/Session/Add', Hod_Views.ADD_SESSION, name='add_session'),
    path('Hod/Session/View', Hod_Views.VIEW_SESSIONS, name='view_sessions'),
    path('Hod/Session/Edit/<str:id>/', Hod_Views.EDIT_SESSION, name="edit_session"),
    path('Hod/Session/Update', Hod_Views.UPDATE_SESSION, name="update_session"),
    path('Hod/Session/Delete/<str:id>/', Hod_Views.DELETE_SESSION, name='delete_session'),

    path('Hod/Staff/Notification', Hod_Views.STAFF_NOTIFICATION, name='staff_notification'),
    path('Hod/Staff/Notification/Save', Hod_Views.SAVE_NOTIFICATION, name='save_notification'),
    path('Hod/Leaves', Hod_Views.STAFF_LEAVE_APPLICATIONS, name='staff_leaves'),
    path('Hod/Leave/Approve/<str:status>', Hod_Views.APPROVE_LEAVE, name="approve_leave"),
    path('Hod/Leave/Decline/<str:status>', Hod_Views.DECLINE_LEAVE, name="decline_leave"),

    path('Hod/Feedbacks', Hod_Views.FEEDBACKS, name='feedbacks'),
    path('Hod/Feedback/Reply/<str:feedback>', Hod_Views.FEEDBACK_REPLY, name='send_feedback_reply'),

    path('Hod/Level/Add', Hod_Views.ADD_LEVEL, name='add_level'),
    path('Hod/Level/View', Hod_Views.VIEW_LEVELS, name='view_levels'),
    path('Hod/Level/Delete/<str:id>/', Hod_Views.DELETE_LEVEL, name='delete_level'),


    #STAFF
    path('Staff/Home', Staff_Views.STAF_HOME, name='staff_home' ),
    path('Staff/Notifications', Staff_Views.NOTIFICATIONS, name='notifications'),
    path('Staff/MarkDone/<str:status>', Staff_Views.MARK_AS_DONE, name= 'mark_done'),
    path('Staff/ApplyLeave', Staff_Views.LEAVE_APLICATION, name='leave_application'),
    path('Staff/Feedback', Staff_Views.FEEDBACK, name='send_feedback'),

    path('Staff/Record_Attendance', Staff_Views.RECORD_ATTENDANCE, name='record_attendance'),
    path('Staff/View_Attendance', Staff_Views.VIEW_ATTENDANCE, name='view_attendance_list'),
    path('Staff/Update_Attendance', Staff_Views.UPDATE_ATTENDANCE, name='update_attendance'),

    path('Staff/Grade/Record', Staff_Views.RECORD_GRADE, name='record_grade'),
    path('Staff/Grade/View', Staff_Views.VIEW_GRADES, name='view_grade_list'),
    path('Staff/Grade/Delete/<str:id>/', Staff_Views.DELETE_GRADE, name='delete_grade'),
    path('Staff/Grade/Update', Staff_Views.UPDATE_GRADE, name='update_grade'),
    path('Staff/Grade/Downloads', Staff_Views.DOWNLOAD_GRADES, name='download_grades'),

    #STUDENTS
    path('Student/Home', Student_Views.HOME, name='student_home'),
    path('Student/Leave', Student_Views.STUDENT_LEAVE_APPLICATION, name='student_leave_application'),
    path('Student/Grades', Student_Views.STUDENT_GRADE_VIEW, name='student_grades'),
    path('Student/Grades/Download', Student_Views.DOWNLOAD_GRADES, name='student_download_grades'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

