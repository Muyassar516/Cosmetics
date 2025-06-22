from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import logout  # Django'ning login funksiyasi
from django.contrib.auth import authenticate, login as auth_login

from accounts.form import UserForm, LoginForm
from accounts.models import Profile


def register(request):
    if request.method=='POST':

        form=UserForm(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form=UserForm()


    return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('get')
            else:
                form.add_error(None, "Username yoki parol noto'g'ri")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def edit_user_profile(request, user_id):
    user_profile = Profile.objects.get(id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("get", user_id=user_id)
    else:
        form = UserForm(instance=user_profile)

    return render(request, "profile_form.html", {"form": form})