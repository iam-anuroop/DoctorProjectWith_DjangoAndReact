from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from .serializer import RegistrationSerializer,LoginSerializer,DoctorSerializer,UsersSerializer,UpdateSerializer
from .models import Users,Doctors
from django.shortcuts import get_object_or_404




class RegisrationView(APIView):

    def post(self,request,format=None):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            Users.objects.create_user(
                email = email,
                username = username,
                password = password
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



def token_generator(user):
    refresh = RefreshToken.for_user(user)

    return  {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
            }
            


class LoginView(APIView):
 
    def post(self,request,format=None):
        serialiser = LoginSerializer(data=request.data)
        if serialiser.is_valid():
            email = serialiser.validated_data.get('email')
            password = serialiser.validated_data.get('password')
         
            user = authenticate( email=email,password=password )
            if user is not None:
                token = token_generator(user)
                return Response(
                        {
                        'token':token,
                        'msg':'Login successfull...'
                        },
                        status=status.HTTP_200_OK
                        )
            return Response(
                    {
                    'msg':'user is none...'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(
                {
                'msg':'serialization error',
                'data':serialiser.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
                


@permission_classes([IsAuthenticated])
class ProfileManageView(APIView):
    def get(self,request):
        user = request.user
        try:
            if user.is_doctor == True:
                user = get_object_or_404(Doctors, user__id=user.id)
                serializer = DoctorSerializer(user)
                return Response(
                        {
                        'msg':'doctor account',
                        'data':serializer.data
                        },
                        status=status.HTTP_200_OK
                        )
            else:
                user = Users.objects.get(pk=user.id)
                serializer = UsersSerializer(user)
                return Response(
                        {
                        'msg':'user account',
                        'data':serializer.data
                        },
                        status=status.HTTP_200_OK
                        )
        except Exception as e:
                return Response(
                        {
                        'msg':'user not found',
                        'data': e
                        },
                        status=status.HTTP_404_NOT_FOUND
                        )
    def patch(self,request):
        serializer = UpdateSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                    'msg':'profile updated',
                    'data':serializer.data
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

        


        




# Create your views here.
