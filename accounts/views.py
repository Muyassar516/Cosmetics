from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator

from accounts.form import UserForm, LoginForm,ProfileForm
from accounts.models import Profile, CustomUser, RoleChoice
from django.db.models.signals import post_save
from django.dispatch import receiver
from .form import ProfileUpdateForm, UserUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from cosmetic.models import Cosmetic, Comment, Category
from django.utils import timezone
from django.urls import reverse

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)  # создаёт профиль только если его ещё нет
    else:
        # проверяем, есть ли профиль перед сохранением
        if hasattr(instance, 'profile'):
            instance.profile.save()
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def favorites_view(request):
    profile = request.user.profile  # <- обязательно через profile
    favorites = profile.favorites.all()
    return render(request, 'accounts/favorites.html', {'favorites': favorites})
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # пароль будет хеширован
            # сохраняем profile автоматически через сигнал
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.first_name = form.cleaned_data.get('first_name', '')
            profile.last_name = form.cleaned_data.get('last_name', '')
            profile.email = form.cleaned_data.get('email', '')
            profile.phone = form.cleaned_data.get('phone_number', '')
            profile.save()

            # Авторизация
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user:
                auth_login(request, user)
            return redirect('get')
    else:
        form = UserForm()

    return render(request, 'accounts/register.html', {'form': form})
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('get')
#             else:
#                 form.add_error(None, "Username yoki parol noto'g'ri")
#     else:
#         form = LoginForm()
#     return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user_profile = request.user.profile
    favorites = user_profile.favorites.all()

    context = {
        'profile': user_profile,
        'favorites': favorites,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})

# accounts/views.py

@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': request.user,
    }
    return render(request, 'accounts/update_profile.html', context)

@login_required
def detail_cosmetic(request, cosmetic_id):
    cosmetic = get_object_or_404(Cosmetic, id=cosmetic_id)

    # Обработка формы комментария
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Comment.objects.create(
                cosmetic=cosmetic,
                user=request.user,  # обязательно объект пользователя
                text=text,
                created_at=timezone.now()
            )
            return redirect('cosmetic_detail', cosmetic_id=cosmetic.id)

    # Проверяем, лайкнул ли пользователь
    has_liked = request.user.profile.favorites.filter(id=cosmetic.id).exists()

    context = {
        'cosmetic': cosmetic,
        'has_liked': has_liked,
        'comments': cosmetic.comments.all().order_by('-created_at'),  # новые сверху
    }
    return render(request, 'crud/detail.html', context)



# views.py
def home(request):
    # Ручной список паблишеров
    publishers = [
        {
            'username': 'muyassar',
            'nickname': 'Muyassar',
            'bio': 'Sotuvchi kosmetika bo‘yicha ekspert',
            'image': 'images/default-user.png',  # можно положить в static
        },
        {
            'username': 'kal',
            'nickname': 'Kal',
            'bio': 'Yangi mahsulotlar sotuvchisi',
            'image': 'images/default-user.png',
        },
        {
            'username': 'kali',
            'nickname': 'Kali',
            'bio': 'Parfyumeriya bo‘yicha mutaxassis',
            'image': 'images/default-user.png',
        },
        {
            'username': 'mir',
            'nickname': 'Mir',
            'bio': 'Kosmetika mahsulotlari bo‘yicha sotuvchi',
            'image': 'images/default-user.png',
        },
        {
            'username': 'la',
            'nickname': 'La',
            'bio': 'Yuqori sifatli kosmetika sotuvchisi',
            'image': 'images/default-user.png',
        },
        {
            'username': 'sorya',
            'nickname': 'Sorya',
            'bio': 'Tajriba va maslahatlar bilan sotuvchi',
            'image': 'images/default-user.png',
        },
    ]

    # Каталог косметики с пагинацией
    cosmetics_list = Cosmetic.objects.all()
    paginator = Paginator(cosmetics_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'get.html', {
        'publishers': publishers,
        'page_obj': page_obj,
        'categories': categories,
    })


# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .form import CustomLoginForm


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # logindan keyin qayerga o'tishi kerak
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})
