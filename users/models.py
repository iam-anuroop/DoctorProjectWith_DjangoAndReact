from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, username, password=None,is_doctor=False,**extrafields):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          username=username,
          is_doctor = is_doctor,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, username, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          username=username,
      )
      user.is_admin = True
      user.is_active = True
      user.save(using=self._db)
      return user

#  Custom User Model
class Users(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  first_name = models.CharField(max_length=100,null=True,blank=True)
  last_name = models.CharField(max_length=100,null=True,blank=True)
  username = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_doctor = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      return self.is_admin

  

class Doctors(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE,related_name='doctors')
    department = models.CharField(max_length=155,null=True,blank=True)
    hospital = models.CharField(max_length=155,null=True,blank=True)

    is_verified = models.BooleanField(default=False)
