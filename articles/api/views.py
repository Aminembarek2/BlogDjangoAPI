#from django.db.models import Q
from articles.api.serilizers import PostDetailSerializer, PostListSerializer, PostCreateUpdateSerializer
from articles.models import Post
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    )


@permission_classes([IsAuthenticated])
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

@permission_classes([IsOwnerOrReadOnly])
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'

@permission_classes([IsOwnerOrReadOnly])
class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

@permission_classes([AllowAny])
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

