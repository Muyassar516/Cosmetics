from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cosmetic.views import  get_cosmetic, create_cosmetic, delete_cosmetic, update_cosmetic, detail_cosmetic, \
    toggle_like, user_products, location_view

urlpatterns=[
    path('location/', location_view, name='location'),
    path('my-products/',user_products,name='user_products'),
    path('get/',get_cosmetic,name='home'),
    path('',get_cosmetic,name='get'),
    path('create/',create_cosmetic,name='create'),
    path('delete/<int:pk>',delete_cosmetic,name='delete'),
    path('update/<int:pk>',update_cosmetic,name='update'),
    path('detail/<int:cosmetic_id>/', detail_cosmetic, name='cosmetic_detail'),
    path('like/<int:cosmetic_id>',toggle_like,name='toggle_like'),

     ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)