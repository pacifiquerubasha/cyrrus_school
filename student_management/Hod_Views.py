import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import *
from django.contrib import messages

def hod_user_check(user):
    return user.user_type == '1'


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def HOME(request):
    total_students= Student.objects.all().count()
    total_staff= Staff.objects.all().count()
    total_courses= Course.objects.all().count()
    total_subjects= Subject.objects.all().count()

    total_boys = Student.objects.filter(gender='Male').count()
    total_girls = Student.objects.filter(gender='Female').count()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()    
    context = {
        'total_students':total_students,
        'total_staff':total_staff,
        'total_courses':total_courses,
        'total_subjects':total_subjects,
        'total_boys':total_boys,
        'total_girls':total_girls,
        'notifications':notifications,
        'count':notifications_count
    }

    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    levels = Level.objects.all()
    session_year = Session_Year.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        course_id = request.POST.get("course_id")
        level_id = request.POST.get('level_id')
        session_id = request.POST.get("session_id")
        password = request.POST.get("password")

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken' )
            return redirect('add_student')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists' )
            return redirect('add_student')

        else:
            
            if course_id == "Select Course":                
                messages.error(request, "Please select a course")
                return redirect("add_student")

            elif session_id == "Select Session": 
                messages.error(request, "Please select a session")
                return redirect("add_student")
            
            elif level_id == "Select Level": 
                messages.error(request, "Please select a level")
                return redirect("add_student")

            else:
                user = CustomUser(
                    first_name = first_name,
                    last_name=last_name,
                    profile_pic=profile_pic,
                    email=email,
                    username=username,
                    user_type=3
                )

                user.set_password(password)
                user.save()

                course = Course.objects.get(id=course_id)
                session_year = Session_Year.objects.get(id=session_id)
                level = Level.objects.get(id=level_id )

                student = Student(
                        admin = user,
                        address = address,
                        session_year = session_year,
                        course_id = course,
                        level_id = level,
                        gender = gender,
                )
                student.save()
                messages.success(request, user.first_name +" "+ user.last_name+" was successfully added !")

                return redirect("add_student")
            

    context = {
        "courses":course,
        "sessions":session_year,
        'levels':levels,
        'notifications':notifications,
        'count':notifications_count
    }

    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_STUDENTS(request):
    students = Student.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    
    context={
        "students":students,
        'notifications':notifications,
        'count':notifications_count
    }
    return render(request, 'Hod/view_student.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_SINGLE_STUDENT(request, pk):
    student = Student.objects.get(pk=pk)
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    
    context = {
        "student":student,
        'notifications':notifications,
        'count':notifications_count
    }

    return render(request, 'Hod/single_student.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def EDIT_STUDENT(request, pk):
    student = Student.objects.get(pk=pk)

    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        'student':student,
        'courses':course,
        'sessions':session_year,
        'notifications':notifications,
        'count':notifications_count
    }

    return render(request, 'Hod/edit_student.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def UPDATE_STUDENT(request):

    if request.method == "POST":
        
        student_id = request.POST.get('student_id')        
        
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        
        if course_id == "Select Course":                
            messages.error(request, "Couldn't update without a valid course")
            return redirect('view_students')

        elif session_id == "Select Session": 
            messages.error(request, "Couldn't update without a valid session")
            return redirect('view_students')

        else:
            user = CustomUser.objects.get(id = student_id)
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            # user.username = username

            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            student = Student.objects.get(admin = student_id)
            
            student.address = address
            student.gender = gender

            course = Course.objects.get(id = course_id)
            student.course_id = course

            session_year = Session_Year.objects.get(id = session_id)
            student.session_year_id = session_year

            student.save()
            messages.success(request,f'{student.admin.first_name} was successfully updated!')
            return redirect('view_students')
    

    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
   
    student.delete()
    messages.success(request, f"{student.first_name} deleted successfully!")

    return redirect('view_students')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DOWNLOAD_STUDENTS(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename=List_Of_Students' + \
                                        str(date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'FistName','Last Name', 'Email', 'Gender', 'Course', 'Address', 'Session Year', 'Date Inserted'])

    students = Student.objects.all()

    for student in students:
        writer.writerow([student.id, student.admin.first_name, student.admin.last_name, student.admin.email, student.gender, student.course_id, student.address, student.session_year, student.created_at])
    
    return response

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_STAFF(request):
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        gender = request.POST.get("gender")
        address = request.POST.get("address")        
        password = request.POST.get("password")

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken' )
            return redirect('add_staff')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists' )
            return redirect('add_staff')
                
        user = CustomUser(
            first_name = first_name,
            last_name=last_name,
            profile_pic=profile_pic,
            email=email,
            username=username,
            user_type=2
        )

        user.set_password(password)
        user.save()

        staff = Staff(
                admin = user,
                address = address,
                gender = gender,
        )
        staff.save()
        messages.success(request, user.first_name +" "+ user.last_name+" was successfully added !")

        return redirect("add_staff")            

    return render(request, 'Hod/add_staff.html', {'notifications':notifications, 'count':notifications_count})


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    
    context = {
        "staff":staff, 
        'notifications':notifications,
        'count':notifications_count
    }
    
    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_SINGLE_STAFF(request, pk):
    staff = Staff.objects.get(pk=pk)
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        "staff":staff,
        'notifications':notifications,
        'count':notifications_count
    }
    return render(request, 'Hod/single_staff.html', context)


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def EDIT_STAFF(request, pk):
    staff = Staff.objects.get(pk=pk)
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        'staff':staff, 
        'notifications':notifications,
        'count':notifications_count      
    }
    
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def UPDATE_STAFF(request):

    if request.method == "POST":
        
        staff_id = request.POST.get('staff_id')        
        
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        
        
        user = CustomUser.objects.get(id = staff_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        # user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin = staff_id)
        
        staff.address = address
        staff.gender = gender

        
        staff.save()
        messages.success(request,f'Staff member {staff.admin.first_name} was successfully updated!')
        return redirect('view_staff')
    
    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
   
    staff.delete()
    messages.success(request, f"Staff member {staff.first_name} deleted successfully!")
    
    return redirect('view_staff')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DOWNLOAD_STAFF(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename=List_Of_Staff' + \
                                        str(date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'FistName','Last Name', 'Email', 'Gender', 'Address', 'Date Inserted'])

    staff = Staff.objects.all()
    for staff in staff:
        writer.writerow([staff.id, staff.admin.first_name, staff.admin.last_name, staff.admin.email, staff.gender, staff.address, staff.created_at])
    
    return response

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_COURSE(request):
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    if request.method == "POST":
        course_name = request.POST.get('course_name')

        if Course.objects.filter(name=course_name).exists():
            messages.warning(request, 'Course with similar name is already saved' )
            return redirect('add_course')
        else:
            course = Course(
                name = course_name
            )
            course.save()

            messages.success(request, f"{course.name} saved successfully!")
            return redirect('add_course')

    return render(request, 'Hod/add_course.html', {'notifications': notifications, 'count':notifications_count})

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_COURSE(request):
    courses = Course.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        "courses":courses,
        'notifications': notifications, 
        'count':notifications_count
    }

    return render(request, 'Hod/view_course.html', context)


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def EDIT_COURSE(request, id):
    course = Course.objects.get(id=id)
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        'course':course,
        'notifications': notifications, 
        'count':notifications_count
    }

    return render(request, 'Hod/edit_course.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def UPDATE_COURSE(request):

    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.name = course_name
        course.save()

        messages.success(request, f"Course {course.name} updated successfully!")
        return redirect('view_courses')

    return render(request, 'Hod/edit_course.html')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_COURSE(request, id):
    course = Course.objects.get(id=id)
    course.delete()

    messages.success(request, f"Course {course.name} deleted successfully")
    return redirect('view_courses')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_SUBJECT(request):
    courses = Course.objects.all()
    staffs = Staff.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')


        if course_id == "Select Course":                
            messages.error(request, "Please select a course")
            return redirect('add_subject')

        elif staff_id == "Select Staff": 
            messages.error(request, "Please select a staff")            
            return redirect('add_subject')
        else:
            
            course = Course.objects.get(id=course_id)
            staff=Staff.objects.get(admin=staff_id)

            subject = Subject(
                name = subject_name,
                course_id = course,
                staff_id = staff
            )    
            subject.save()
            messages.success(request, f"Subject {subject.name} added successfully!")
            return redirect('add_subject')
        
        
    context = {
        "courses":courses,
        "staffs":staffs,
        'notifications': notifications, 
        'count':notifications_count
    }

    return render(request, 'Hod/add_subject.html', context)


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_SUBJECT(request):
    subjects = Subject.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {"subjects":subjects, 'notifications': notifications, 'count':notifications_count}
    return render(request, 'Hod/view_subjects.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    courses = Course.objects.all()
    staffs=Staff.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {
        'subject':subject,
        "courses":courses,
        "staffs":staffs,
        'notifications': notifications, 
        'count':notifications_count
    }

    return render(request, 'Hod/edit_subject.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def UPDATE_SUBJECT(request):

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        if course_id == "Select Course":                
            messages.error(request, "Cannot update without a valid course")
            
        elif staff_id == "Select Staff": 
            messages.error(request, "Cannot update without a valid a staff")            

        else:
            course = Course.objects.get(id=course_id)
            staff = Staff.objects.get(admin=staff_id)

            subject = Subject.objects.get(id=subject_id)
            
            subject.name = subject_name
            subject.course_id = course
            subject.staff_id = staff
            subject.save()

            messages.success(request, f"{subject.name} in {subject.course_id} updated successfully!")
        return redirect('view_subjects')

    return render(request, 'Hod/edit_subject.html')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, f"{subject.name} in {subject.course_id} deleted successfully! ")
    return redirect('view_subjects')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_SESSION(request):
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    if request.method == "POST":
        start = request.POST.get('session_start')
        end = request.POST.get('session_end')

        session = Session_Year(
            session_start = start,
            session_end = end
        )

        if Session_Year.objects.filter(session_start=start).exists():
            messages.warning(request, f'Session starting on {session.session_start} is already saved')
            return redirect('add_session')

        else:
            session.save()
            messages.success(request, f'Session {session.session_start} to {session.session_end} CREATED successfully')
            return redirect('add_session')

    return render(request, 'Hod/add_session.html', {'notifications':notifications, 'count':notifications_count})

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_SESSIONS(request):
    sessions = Session_Year.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {'sessions':sessions, 'notifications':notifications, 'count':notifications_count}
    return render(request, 'Hod/view_sessions.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def EDIT_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    context= {'session':session, 'notifications':notifications, 'count':notifications_count}

    return render(request, 'Hod/edit_session.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def UPDATE_SESSION(request):
    if request.method == 'POST':
        start = request.POST.get('session_start')
        end = request.POST.get('session_end')
        session_id = request.POST.get('session_id')

        session = Session_Year.objects.get(id=session_id)
        session.session_start = start
        session.session_end = end

        if Session_Year.objects.filter(session_start=start).exists():
            messages.warning(request, f'Session starting on {session.session_start} is already saved')
            return redirect('edit_session')
        else:
            session.save()
            messages.success(request, f'Session {session.session_start} to {session.session_end} UPDATED successfully')
            return redirect('view_sessions')

    return render(request, 'Hod/edit_session.html')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request, f'Session {session.session_start} to {session.session_end} DELETED successfully')
    return redirect('view_sessions')

#STAFF NOTIFICATIONS
@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def STAFF_NOTIFICATION(request):
    staff = Staff.objects.all()
    staff_notifications = Staff_Notification.objects.all().order_by('-created_at')

    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {'staff':staff, 'staff_notifications':staff_notifications, 'notifications':notifications, 'count':notifications_count}
    return render(request, 'Hod/staff_notification.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def SAVE_NOTIFICATION(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        staff_id = request.POST.get('staff_id')

        target_staff = Staff.objects.get(admin = staff_id)
        staff_notification = Staff_Notification(
            message = message,
            staff = target_staff
        )

        staff_notification.save()

        message = 'You have a new notification'
        notification = GeneralNotification(
            sender = target_staff,
            message = message,
            motive='Staff_Notification'
        )

        notification.save()

        messages.success(request, 'Notification saved successfully')
        return redirect('staff_notification')

#STAFF LEAVE APPLICATIONS
@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def STAFF_LEAVE_APPLICATIONS(request):
    all_leaves = Leave_Application.objects.all().order_by('-leave_date')

    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {'all_leaves':all_leaves, 'notifications':notifications, 'count':notifications_count}

    return render(request, 'Hod/staff_leave_applications.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def APPROVE_LEAVE(request, status):

    leave = Leave_Application.objects.get(id = status)    
    leave.status = 2
    leave.save()
    messages.success(request, 'Decision recorded successfully')
    return redirect('staff_leaves')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DECLINE_LEAVE(request, status):

    leave = Leave_Application.objects.get(id = status)    
    leave.status = 1
    leave.save()
    messages.success(request, 'Decision recorded successfully')
    return redirect('student_leaves')


#STUDENT LEAVE APPLICATIONS ===========================
@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_STUDENT_LEAVE_APPLICATIONS(request):
    all_leaves = Student_Leave.objects.all().order_by('-leave_date')
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    context = {'all_leaves':all_leaves, 'notifications':notifications, 'count':notifications_count}

    return render(request, 'Hod/student_leave_applications.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def APPROVE_STUDENT_LEAVE(request, status):

    leave = Student_Leave.objects.get(id = status)    
    leave.status = 2
    leave.save()
    messages.success(request, 'Decision recorded successfully')
    return redirect('student_leaves')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DECLINE_STUDENT_LEAVE(request, status):

    leave = Student_Leave.objects.get(id = status)    
    leave.status = 1
    leave.save()
    messages.success(request, 'Decision recorded successfully')
    return redirect('student_leaves')

#FEEDBACKS ===========================================
@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def FEEDBACKS(request):

    all_feedbacks = Feedback.objects.all()
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    general_notifications = GeneralNotification.objects.filter(motive='Feedback')
    general_notifications.delete()

    context = {'all_feedbacks':all_feedbacks, 'notifications':notifications, 'count':notifications_count}

    return render(request, 'Hod/all_feedbacks.html', context)

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def FEEDBACK_REPLY(request, feedback):
    if request.method == 'POST':
        reply = request.POST.get('reply')
        feedback = Feedback.objects.get(id = feedback )        

        feedback.reply= reply
        feedback.save()
        messages.success(request, 'Reply sent successfully')
        return redirect('feedbacks')

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def ADD_LEVEL(request):
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()

    if request.method == 'POST':
        level_name = request.POST.get('level_name')       
        level = Level(
            level_name = level_name,
        )

        level.save()
        messages.success(request, f'Level {level.level_name} added successfully')
        return redirect('add_level')

    return render(request, 'Hod/add_level.html', {'notifications':notifications, 'count':notifications_count})

@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def VIEW_LEVELS(request):
    levels = Level.objects.all()
    
    notifications = GeneralNotification.objects.filter(motive='Feedback')
    notifications_count = notifications.count()
    
    context = {'levels':levels, 'notifications':notifications, 'count':notifications_count}
    return render(request, 'Hod/view_levels.html', context)


@login_required(login_url='/')
@user_passes_test(hod_user_check, login_url='/')
def DELETE_LEVEL(request, id):
    level = Level.objects.get(id=id)
    level.delete()
    messages.success(request, f'Level {level.level_name} {level.course} deleted successfully')
    return redirect('view_levels')

