from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from .serializer import RegistrationSerializer,MyTokenSerializer,UsersSerializer,UpdateSerializer,UserAdminSerializer
from .models import Users,Doctors
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView





class RegisrationView(APIView):
    def post(self,request,format=None):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            is_doctor = serializer.validated_data.get('is_doctor')

            Users.objects.create_user(
                email = email,
                username = username,
                password = password,
                is_doctor=is_doctor
            )
            return Response(
                    {
                    'msg':'Registration successfull...',
                    'data':serializer.data
                    },
                    status=status.HTTP_201_CREATED
                    )
        
        return Response(
                {
                'msg':'serialization error',
                'data':serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenSerializer





@permission_classes([IsAuthenticated])
class ProfileManageView(APIView):
    def get(self,request):
        print(request.data)
        user = Users.objects.get(pk=request.user.id)
        serializer = UsersSerializer( user)
        return Response(
                {
                'msg':'user account',
                'data':serializer.data
                },
                status=status.HTTP_200_OK
                )
    
    def patch(self,request):
        print(request.data)
        serializer = UpdateSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                    'msg':'profile updated'
                    },
                    status=status.HTTP_200_OK
                    )
        return Response(
                {
                'msg':'update failed',
                'data':serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
    def delete(self,request):
        try:
            user = Users.objects.get(pk=request.user.id)
            user.delete()
            return Response(
                    {
                    'msg':'deleted...'
                    },
                    status=status.HTTP_200_OK
                    )
        except:
            return Response(
                {
                'msg':'something wrong'
                },
                status=status.HTTP_400_BAD_REQUEST
                )

        
@permission_classes([IsAdminUser])
class AdminPanelView(APIView):
    def get(self,request,pk=None):
        if pk is not None:
            print('pkkkkkk',pk)
            user = Users.objects.get(id=pk)
            serializer = UsersSerializer(user)
            return Response(
                    {
                    'msg':'user',
                    'data':serializer.data
                    },
                    status=status.HTTP_200_OK
                    )
        else:
            users = Users.objects.all()
            serializer = UsersSerializer(users,many=True)
            return Response(
                    {
                    'msg':'users',
                    'data':serializer.data
                    },
                    status=status.HTTP_200_OK
                    )
    
    def patch(self,request,pk=None):
        print(request.data)
        print(pk)
        print('hi')
        if pk is not None:
            print(request.data)
            user = Users.objects.get(pk=pk)
            serializer = UserAdminSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.validated_data['is_active']:
                    return Response(
                            {
                            "msg":"User Unblocked !!!"
                            },
                            status=status.HTTP_200_OK
                            )
                return Response(
                        {
                        "msg":"User Blocked !!!"
                        },
                        status=status.HTTP_200_OK
                        )
            return Response(serializer.errors)

@permission_classes([IsAuthenticated])
class UserDoctorView(APIView):
    def get(self,request):
        user = Users.objects.filter(is_doctor=True,doctors__is_verified=True,is_active=True)
        serializer = UserAdminSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



        
    
        




# Create your views here.
