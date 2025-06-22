
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cosmetic.form import CosmeticForm
from cosmetic.models import Cosmetic, Like


def index(request):
    return render(request,'index.html')

def get_cosmetic(request):
    query = request.GET.get('q')
    cosmetics = Cosmetic.objects.all()

    if query:
        cosmetics = cosmetics.filter(title__icontains=query)

    paginator = Paginator(cosmetics, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'crud/get.html', {
        'page_obj': page_obj,
        'query': query,
    })
@login_required
def create_cosmetic(request):
    if request.method=='POST':
        form=CosmeticForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('get')
        else:
            return render(request, 'crud/create.html', {'form': form})
    else:
        form=CosmeticForm()
        return render(request,'crud/create.html',{'form':form})

@login_required
def update_cosmetic(request):
    pass

@login_required

def detail_cosmetic(request, cosmetic_id):
    cosmetic = get_object_or_404(Cosmetic, id=cosmetic_id)
    user = request.user.username
    has_liked = cosmetic.likes.filter(user=user).exists()

    return render(request, 'crud/detail.html', {
        'cosmetic': cosmetic,
        'has_liked': has_liked
    })


def delete_cosmetic(request,pk):
    cos=get_object_or_404(Cosmetic,pk=pk)
    if request.method=="POST":
        cos.delete()
        messages.success(request,"O'chirildi")
        return redirect('get')
    return render(request,'crud/delete',{'cos':cos})


def toggle_like(request, cosmetic_id):
    if request.method == 'POST':
        user = request.POST.get('user')
        cosmetic = get_object_or_404(Cosmetic, id=cosmetic_id)
        existing_like = Like.objects.filter(cosmetic=cosmetic, user=user).first()
        if existing_like:
            existing_like.delete()
        else:
            Like.objects.create(cosmetic=cosmetic, user=user)

        return redirect('cosmetic_detail', cosmetic_id=cosmetic.id)
