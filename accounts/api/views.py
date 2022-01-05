from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from .serializers import RegisterSerializer, UpdateUserSerializer, User, UserLoginSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import (
    authenticate,
    login,
    logout,

    )

# @permission_classes([AllowAny])
# class UserLoginAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserLoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
@permission_classes([IsAdminUser])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@permission_classes([IsOwnerOrReadOnly])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        

@api_view(['DELETE',])    
@permission_classes([IsOwnerOrReadOnly])
def deleteUser(request,slug):
    data={}
    try:
        user=User.objects.get(username=slug)
        user.delete()
        data["succes"] = "delete succesful"
    except User.DoesNotExist:
        data["failure"] = "delete failed"
        return Response(data,status=status.HTTP_404_NOT_FOUND)

    return Response(data=data)

# LOGIN / REGISTER / LOGOUT

@api_view(['POST'])
@permission_classes([AllowAny])
def Register_Users(request):
    try:
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user registered successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = token

        else:
            data = serializer.errors
        return Response(data)
    except IntegrityError as e:
        account=User.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})

#Login

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
        data = {}
        serializer =  UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            Account = User.objects.get(username=serializer.data["username"])
            token = serializer.data["token"]
            if Account:
                if Account.is_active:
                    print(request.user)
                    login(request, Account)
                    data["message"] = "user logged in"
                    data["username"] = Account.username

                    Res = {"data": data, "token": token}

                    return Response(Res)

                else:
                    raise ValidationError({"400": f'Account not active'})
        else:
            return Response(serializer.errors)
#LogOut
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def User_logout(request):
    Account = User.objects.get(username=request.user)
    Token.objects.get(user=Account).delete()
    logout(request)
    return Response('User Logged out successfully')