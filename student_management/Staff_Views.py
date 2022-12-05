from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import csv
from .utils import general_notifications


def staff_user_check(user):
    return user.user_type == '2'


@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def STAF_HOME(request):
    notifications, count = general_notifications(request)    
    return render(request, 'Staff/staff_home.html', {'notifications':notifications, 'count':count})

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)

    notifications, count = general_notifications(request)
    notifications.delete()

    for staff in staff:      
        
        staff_notifications = Staff_Notification.objects.filter(staff = staff.id)

        context = {'staff_notifications':staff_notifications}            

        return render(request, 'Staff/notifications.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def MARK_AS_DONE(request, status):

    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def LEAVE_APLICATION(request):  
    notifications, count = general_notifications(request)
    for staff in Staff.objects.filter(admin=request.user.id):     

        applications = Leave_Application.objects.filter(staff_id = staff.id)

        context = {'leaves':applications, 'notifications':notifications, 'count': count}         

    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')        
        staff = Staff.objects.get(admin=request.user.id)

        leave_application = Leave_Application(
            staff = staff,
            leave_date = leave_date,
            leave_message = leave_message
        )

        leave_application.save()
        messages.success(request, 'Your leave application was successfully sent')
        return redirect('leave_application')
               

    return render(request, 'Staff/leave_application.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def FEEDBACK(request):
    notifications, count = general_notifications(request)
    for staff in Staff.objects.filter(admin=request.user.id):     

        feedbacks = Feedback.objects.filter(staff_id = staff.id)

        context = {'feedbacks':feedbacks, 'notifications':notifications, 'count': count} 

    if request.method == 'POST':

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        staff = Staff.objects.get(admin = request.user.id)

        feedback = Feedback(
            subject = subject,
            message = message,
            staff=staff
        )

        feedback.save()
        message = f'{staff.admin.first_name} {staff.admin.last_name} sent a feedback'
        notification = GeneralNotification(
            sender = staff,
            message = message,
            motive='Feedback'
        )

        notification.save()

        messages.success(request, 'Your feedback has been successfully sent')        
        return redirect('send_feedback')

    return render(request, 'Staff/feedback.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def RECORD_ATTENDANCE(request):
    students = Student.objects.all()
    notifications, count = general_notifications(request)
    context = {'students':students, 'notifications':notifications, 'count': count}
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        attendance = request.POST.get('attendance')  
               
        if student_id == 'Select Student':
            messages.error(request, 'Cannot record attendance for an inexisting student')
            return redirect('record_attendance')
        
        elif attendance == 'Select Attendance':
            messages.error(request, 'Cannot record invalid attendance status')
            return redirect('record_attendance')
        
        else:
            student = Student.objects.get(id=student_id)
            attendance_record = Attendance(
                student = student,
                attendance = attendance
            )

            attendance_record.save()
            messages.success(request, f'Attendance for {student.admin.first_name} recorded')
            return redirect('record_attendance')

    return render(request, 'Staff/record_attendance.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def VIEW_ATTENDANCE(request):
    notifications, count = general_notifications(request)
    attendances = Attendance.objects.all()
    context = {'attendances':attendances, 'notifications':notifications, 'count': count}

    return render(request, 'Staff/view_attendance_list.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def UPDATE_ATTENDANCE(request):
    if request.method == 'POST':
        attendance_status = request.POST.get('attendance')
        attendance_id = request.POST.get('attendance_id')

        if attendance_status == 'Select Attendance':
            messages.error(request, 'Cannot record invalid attendance status')
            return render('view_attendance_list')

        else:
            attendance_record = Attendance.objects.get(id=attendance_id)
            attendance_record.attendance = attendance_status
            attendance_record.save()
            
            messages.success(
                request, 
                f'Attendance for {attendance_record.student.admin.first_name} {attendance_record.student.admin.last_name} on {attendance_record.created_at} updated'
            )
            return redirect('view_attendance_list')

    return render(request, 'Staff/view_attendance_list.html')

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def RECORD_GRADE(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    notifications, count = general_notifications(request)
    context = {
        'students':students, 
        'courses':courses, 
        'subjects':subjects,
        'notifications':notifications,
        'count': count

    }

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        subject_id = request.POST.get('subject_id')
        grade = request.POST.get('grade')
        possible_marks = request.POST.get('possible_marks')

        if student_id == 'Select Student' or course_id == 'Select Course'  or subject_id == 'Select Subject':
            messages.error(request, 'Make sure you select a valid student, course and subject')
            return redirect('record_grade')

        else:
            subject = Subject.objects.get(id=subject_id)
            
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)

            grade = Grade(
                subject = subject,
                student = student,
                course = course,
                grade = grade,
                possible_marks = possible_marks
            )

            if int(grade.grade) > int(grade.possible_marks) :
                messages.error(request, f'The grade {grade.grade} typed is higher than the possible marks {grade.possible_marks}')
                return redirect('record_grade')
            else:
                grade.save()          

                target_staff = Staff.objects.get(admin=request.user.id)
               
                notification = GeneralNotification(
                    sender = target_staff,
                    message = f'Your grade for {grade.subject} has been released!',
                    motive='Grade Notifications'
                )

                notification.save()

                messages.success(request, f'Grade {grade.grade} out of {grade.possible_marks} for {grade.student.admin.first_name} in {grade.course.name} recorded successfully')
                return redirect('record_grade')

    return render(request, 'Staff/record_grade.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def VIEW_GRADES(request):
    notifications, count = general_notifications(request)
    grades = Grade.objects.all()
    context = {'grades':grades, 'notifications':notifications, 'count': count}

    return render(request, 'Staff/view_grades_list.html', context)

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def DELETE_GRADE(request, id):
    grade = Grade.objects.get(id=id)  
    grade.delete()

    messages.success(request, 'Grade successfully deleted')
    return redirect('view_grade_list')

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def UPDATE_GRADE(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        possible_marks = request.POST.get('possible_marks')
        grade_id = request.POST.get('grade_id')

        updated_grade = Grade.objects.get(id = grade_id)
        updated_grade.grade = grade
        updated_grade.possible_marks = possible_marks
        updated_grade.save()
        messages.success(request, 'Grade updated successfully')
        return redirect('view_grade_list')

@login_required(login_url='/')
@user_passes_test(staff_user_check, login_url='/')
def DOWNLOAD_GRADES(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename=Grades' + \
                                        str(date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Course', 'Subject', 'Grade', 'Possible Marks', 'Date'])

    grades = Grade.objects.all()

    for grade in grades:
        writer.writerow([grade.student, grade.course, grade.subject, grade.grade, grade.possible_marks, grade.created_at])
    
    return response
