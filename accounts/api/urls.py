from django.urls import path, include,re_path
from accounts.api.views import (
    UserListAPIView,
    #UserLoginAPIView,
    UserUpdateAPIView,
    deleteUser,
)


app_name = "accounts"

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    #path('login/', UserLoginAPIView.as_view(),name='Login'),
    re_path(r'^update/(?P<slug>[\w-]+)/$', UserUpdateAPIView.as_view(), name='update'),
    re_path(r'^delete/(?P<slug>[\w-]+)/$', deleteUser, name='delete'),
]