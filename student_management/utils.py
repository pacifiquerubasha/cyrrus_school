from app.models import *

def general_notifications(request):
    notifications = GeneralNotification.objects.filter(motive='Staff_Notification', sender__admin__id = request.user.id ).order_by('-created_at')
    count = notifications.count()    
    
    return notifications, count

def student_notifications(request):
    student_notifications = GeneralNotification.objects.filter(motive='Grade Notifications')
    student_notifications_count = student_notifications.count()

    return student_notifications, student_notifications_count


def hod_notifications(request):
    hod_notifications = GeneralNotification.objects.filter(motive='Feedback')
    hod_notifications_count = hod_notifications.count()   

    return hod_notifications, hod_notifications_count