from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.serializers import UserSerializer, UserLoginSerializer
from authentication.token import BearerTokenAuthentication


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = []

    # login
    @action(methods=['post'], detail=False, url_path='login', url_name='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'token': token.key,
                    'user': UserSerializer(user).data
                }
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid credentials'
            }, status=400)

    # logout
    @action(methods=['post'], detail=False, url_path='logout', url_name='logout')
    def logout(self, request):
        request.auth.delete()
        return Response({
            'status': 'success',
            'message': 'Logout successful'
        })

    # register
    @action(methods=['post'], detail=False, url_path='register', url_name='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'User registered',
                'data': serializer.data
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid data',
                'data': serializer.errors
            }, status=400)


    # TODO: Password Reset and Change Password








class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]



    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'User details',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)

        return Response({
            'status': 'success',
            'message': 'User details',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': 'success',
            'message': 'User details updated',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'User deleted',
        })


    # profile
    @action(methods=['get', 'put','patch'], detail=False, url_path='profile', url_name='profile')
    def profile(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.user.pk)
            serializer = UserSerializer(user)

            if request.method in ['PUT', 'PATCH']:
                serializer = UserSerializer(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({
                "status": "success",
                "message": "User profile retrieved successfully",
                "data": serializer.data
            })
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)






