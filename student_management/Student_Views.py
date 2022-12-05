import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import student_notifications

def student_user_check(user):
    return user.user_type == '3'


@login_required(login_url='/')
@user_passes_test(student_user_check, login_url='/')
def HOME(request):
    notifications, count = student_notifications(request)
    return render(request, 'Student/student_home.html', {'notifications':notifications, 'count':count})

@login_required(login_url='/')
@user_passes_test(student_user_check, login_url='/')
def STUDENT_LEAVE_APPLICATION(request):
    notifications, count = student_notifications(request)
    for student in Student.objects.filter(admin=request.user.id):     

        applications = Student_Leave.objects.filter(student_id = student.id)

        context = {'leaves':applications, 'notifications':notifications, 'count':count}         

    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')        
        student = Student.objects.get(admin=request.user.id)

        leave_application = Student_Leave(
            student = student,
            leave_date = leave_date,
            leave_message = leave_message
        )

        leave_application.save()
        messages.success(request, 'Your leave application was successfully sent')
        return redirect('student_leave_application')
               

    return render(request, 'Student/student_leave.html', context)

@login_required(login_url='/')
@user_passes_test(student_user_check, login_url='/')
def STUDENT_GRADE_VIEW(request):
    grades = Grade.objects.filter(student__admin__id=request.user.id)
    notifications, count = student_notifications(request)
    notifications.delete()

    return render(request, 'Student/grades.html', {'grades':grades, 'notifications':notifications, 'count':count })

@login_required(login_url='/')
@user_passes_test(student_user_check, login_url='/')
def DOWNLOAD_GRADES(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename=GradeBook' + f'_{request.user.first_name}_{request.user.last_name}_'+ \
                                        str(date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Course', 'Subject', 'Grade', 'Possible Marks', 'Date'])

    grades = Grade.objects.filter(student__admin__id=request.user.id)

    for grade in grades:
        writer.writerow([grade.student, grade.course, grade.subject, grade.grade, grade.possible_marks, grade.created_at])
    
    return response