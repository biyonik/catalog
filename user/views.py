from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request,messages.SUCCESS, 'Oturum açma işlemi başarılı')
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Böyle bir kullanıcı bulumamadı')
            return redirect('login')
    return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        # Kullanıcı kayıt
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'Bu kullanıcı adı daha önce alınmış')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(request, messages.ERROR, 'Bu e-posta adresi daha önce alınmış')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.add_message(request, messages.INFO, 'Kullanıcı kayıt işlemi başarılı')
                    return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Parola ile Parola Tekrar alanı birbiri ile uyuşmuyor')
            return redirect('register')
    else:
        return render(request, 'user/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.INFO, 'Oturum sonlandırma işlemi başarılı')
        return redirect('index')
    return redirect('index')
