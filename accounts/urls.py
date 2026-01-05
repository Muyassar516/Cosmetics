from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from cosmetic.views import get_cosmetic

urlpatterns=[
    path('', get_cosmetic, name='get'),
    path('profile/',views.profile,name='profile'),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('update/',views.update_profile,name='update_profile'),
    path('favorites/', views.favorites_view, name='favorites'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)