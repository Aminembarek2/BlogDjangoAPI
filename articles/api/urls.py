from django.urls import path, re_path

from articles.api.views import PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostUpdateAPIView, PostCreateAPIView


urlpatterns = [
    re_path(r'^$',PostListAPIView.as_view(), name='list'),
    re_path(r'^create/$',PostCreateAPIView.as_view(), name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$',PostDetailAPIView.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$',PostDeleteAPIView.as_view(), name='Delete'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$',PostUpdateAPIView.as_view(), name='update'),

]