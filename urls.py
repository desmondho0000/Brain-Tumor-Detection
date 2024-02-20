from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from firstPage import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$',views.index,name='homepage'),
    re_path('predictImage',views.predictImage,name='predictImage'),
    re_path('login/', views.login,name='login'),
    re_path('signUp',views.signUp,name='signUp'),
    re_path('logOut',views.logOut,name='logOut'),
    re_path('userAcc/',views.userAcc,name='userAcc'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)