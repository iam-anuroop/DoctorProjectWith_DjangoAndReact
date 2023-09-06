from rest_framework import serializers
from .models import Users , Doctors
from rest_framework.exceptions import ValidationError



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Users
        fields = ['username','email','password','password2','is_doctor']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        username = attrs.get('username')
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
    

class LoginSerializer(serializers.ModelSerializer):
   email = serializers.EmailField()
   class Meta:
        model = Users
        fields = ['email','password']


class DoctorSerializer(serializers.ModelSerializer):
   class Meta:
        model = Doctors
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
   user = DoctorSerializer()
   class Meta:
    model = Users
    fields = '__all__'

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
      model = Users
      fields = ('id','first_name', 'last_name','username', 'email')

    
    def update(self, instance, validated_data):
       instance.first_name = validated_data.get('first_name',instance.first_name)
       instance.last_name = validated_data.get('last_name',instance.last_name)
       instance.email = validated_data.get('email',instance.email)
       instance.username = validated_data.get('username',instance.username)


       if instance.is_doctor:
          print(instance.is_doctor,'lllllllllllllllllllllllllllllllllllllllllll')
          doctor_data = validated_data.get('doctor', {})
          print(doctor_data)
          doctor = Doctors.objects.get(user=instance)
          doctor.department = doctor_data.get('department', doctor.department)
          doctor.hospital = doctor_data.get('hospital', doctor.hospital)
          doctor.save()
             
            
       instance.save()
       return instance
    