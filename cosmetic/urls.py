from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cosmetic.views import index, get_cosmetic, create_cosmetic, delete_cosmetic, update_cosmetic, detail_cosmetic, \
    toggle_like

urlpatterns=[
    path('get/',index,name='home'),
    path('',get_cosmetic,name='get'),
    path('create/',create_cosmetic,name='create'),
    path('delete/<int:pk>',delete_cosmetic,name='delete'),
    path('update/<int:pk>',update_cosmetic,name='update'),
    path('detail/<int:cosmetic_id>/', detail_cosmetic, name='cosmetic_detail'),
    path('like/<int:cosmetic_id>',toggle_like,name='toggle_like'),

     ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
