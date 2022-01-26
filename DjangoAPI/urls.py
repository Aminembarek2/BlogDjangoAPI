
from django.contrib import admin
from django.urls import path, include, re_path
from accounts.api.views import Register_Users, login_user, User_logout
urlpatterns = [
    path('admin/club/', admin.site.urls),
    path('accounts/',include('accounts.api.urls')),
    path('posts/',include('articles.api.urls')),
    re_path(r'^register/', Register_Users, name='register'),
    re_path(r'^login/', login_user, name='login'),
    re_path(r'^logout/', User_logout, name='logout'),
]
