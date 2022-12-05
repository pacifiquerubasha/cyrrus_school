from django.shortcuts import render, redirect
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser


def BASE(request):    
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                        username = request.POST.get('email'),
                                        password=request.POST.get('password'))

        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type =='1':
                return redirect('hod_home')

            elif user_type =='2':
                return redirect('staff_home')
            
            elif user_type =='3':
                return redirect('student_home')
            
            else:
                messages.error(request, 'Email and password are invalid !')
                return redirect('login')

        else:
            messages.error(request, 'Email and password are invalid !')
            return redirect('login')

    return None

def doLogout(request):
    logout(request)

    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    
    context={
        "user":user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method=="POST":
        profile_pic = request.FILES.get('profile_picture')
        first_name = request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name

            if password != None and password != "":
                custom_user.set_password(password)

            if profile_pic != None and profile_pic != "":
                custom_user.profile_pic = profile_pic
            
            custom_user.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
            
        except:
            messages.error(request, "Failed to update your profile!")

    return render(request, 'profile.html')