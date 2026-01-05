from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cosmetic, Comment, Category
from .form import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cosmetic.form import CosmeticForm
from cosmetic.models import Cosmetic, Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cosmetic, Like


def index(request):
    products = Cosmetic.objects.all()
    return render(request,'index.html',{'products': products})
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cosmetic


def get_cosmetic(request):
    query = request.GET.get('q', '')
    cosmetics = Cosmetic.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        cosmetics = cosmetics.filter(category_id=category_id)

    if query:
        cosmetics = cosmetics.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(cosmetics, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    latest_products = Cosmetic.objects.order_by('-id')[:4]

    # Передаем категории в контекст render
    return render(request, 'crud/get.html', {
        'page_obj': page_obj,
        'query': query,
        'latest_products': latest_products,
        'categories': categories,
    })


@login_required
def create_cosmetic(request):
    if request.method == 'POST':
        form = CosmeticForm(request.POST, request.FILES)
        if form.is_valid():
            cosmetic = form.save(commit=False)
            cosmetic.created_by = request.user
            cosmetic.save()
            return redirect('get')
        return render(request, 'crud/create.html', {'form': form})

    form = CosmeticForm()
    return render(request, 'crud/create.html', {'form': form})

@login_required
def update_cosmetic(request, pk):
    cosmetic = get_object_or_404(Cosmetic, pk=pk)

    if cosmetic.created_by != request.user:
        messages.error(request, "❌ У вас нет прав редактировать этот товар!")
        return redirect('get')  # или куда нужно

    if request.method == "POST":
        form = CosmeticForm(request.POST, request.FILES, instance=cosmetic)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменено успешно! ✅")
            return redirect('cosmetic_detail', cosmetic_id=cosmetic.id)
    else:
        form = CosmeticForm(instance=cosmetic)

    return render(request, 'crud/update.html', {'form': form, 'cosmetic': cosmetic})


@login_required
def delete_cosmetic(request, pk):
    cosmetic = get_object_or_404(Cosmetic, pk=pk)

    if cosmetic.created_by != request.user:
        messages.error(request, "❌ У вас нет прав удалить этот товар!")
        return redirect('get')  # или куда нужно

    if request.method == "POST":
        cosmetic.delete()
        messages.success(request, "Удалено! ✅")
        return redirect('get')

    return render(request, 'crud/delete.html', {'cosmetic': cosmetic})

@login_required
def toggle_like(request, cosmetic_id):
    cosmetic = get_object_or_404(Cosmetic, id=cosmetic_id)
    profile = request.user.profile

    if cosmetic in profile.favorites.all():
        profile.favorites.remove(cosmetic)
        liked = False
    else:
        profile.favorites.add(cosmetic)
        liked = True

    return JsonResponse({
        'liked': liked,
        'count': cosmetic.favorited_by.count()
    })

@login_required
def detail_cosmetic(request, cosmetic_id):
    cosmetic = get_object_or_404(Cosmetic, id=cosmetic_id)
    comments = cosmetic.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.cosmetic = cosmetic
            new_comment.user = request.user
            new_comment.save()
            return redirect('cosmetic_detail', cosmetic_id=cosmetic.id)
    else:
        form = CommentForm()

    has_liked = cosmetic in request.user.profile.favorites.all()

    context = {
        'cosmetic': cosmetic,
        'comments': comments,
        'form': form,
        'has_liked': has_liked
    }
    return render(request, 'crud/detail.html', context)


from django.contrib.auth.decorators import login_required

@login_required
def user_products(request):
    my_products = Cosmetic.objects.filter(created_by=request.user)

    return render(request, 'accounts/user_products.html', {
        'my_products': my_products
    })

def location_view(request):
    return render(request, 'crud/location.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import CustomUser


def home(request):
    publishers = CustomUser.objects.filter(role='publisher')
    return render(request, "get.html", {"publishers": publishers})

