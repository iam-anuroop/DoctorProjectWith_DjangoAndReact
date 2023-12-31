from rest_framework import serializers
from rest_framework.fields import empty
from .models import Users , Doctors
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.renderers import JSONRenderer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    is_doctor = serializers.BooleanField(default=False)
    class Meta:
        model = Users
        fields = ['username','email','password','password2','is_doctor']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        username = attrs.get('username')
        is_doctor = attrs.get('is_doctor')
        # print(username)

        if len(password)<=4:
          raise serializers.ValidationError("password must contain atleast 5 characters")
        if password != password2:
          raise serializers.ValidationError("Password and Confirm Password doesn't match")
        if len(username)<=4:
          raise serializers.ValidationError("name must contain atleast 5 characters")
    
        return attrs
    def create(self, validate_data):
        return Users.objects.create_user(**validate_data)
    

class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data =  UsersSerializer(user).data
        token['user'] = user_data
        if hasattr(user,'is_admin'):
            token['is_admin'] = user.is_admin
        return token


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

# for profile view 
class UsersSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer()

    class Meta:
        model = Users
        fields = ['id','first_name','last_name','username','email','is_active','doctors']


            

class UpdateSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer()
    class Meta:
      model = Users
      fields = ('id','first_name', 'last_name','username', 'email','doctors')

    
  
            

    
    def update(self, instance, validated_data):
       instance.first_name = validated_data.get('first_name',instance.first_name)
       instance.last_name = validated_data.get('last_name',instance.last_name)
       instance.email = validated_data.get('email',instance.email)
       instance.username = validated_data.get('username',instance.username)
      #  instance.is_doctor = validated_data.get('is_doctor',instance.is_doctor)
       print(instance.is_doctor)
       if instance.is_doctor:
          print(instance)
          doctor_data = validated_data.get('doctors')
          doctor = Doctors.objects.get(user=instance)
          doctor.department = doctor_data.get('department', doctor.department)
          doctor.hospital = doctor_data.get('hospital', doctor.hospital)
          if doctor.hospital is not  None and doctor.department is not None:
              doctor.is_verified = True
          doctor.save()
             
       instance.save()
       return instance
    

class UserAdminSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(read_only=True)   
    class Meta:
        model = Users
        fields = ('id','first_name', 'last_name','username', 'email','is_active','doctors')

 
    def update(self,instance,validated_data):
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance
    