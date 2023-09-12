from django.urls import path
from .views import RegisrationView,MyTokenObtainPairView,ProfileManageView,AdminPanelView,UserDoctorView

urlpatterns = [
    path('', RegisrationView.as_view(),name='register'),
    path('login/', MyTokenObtainPairView.as_view(),name='login'),
    path('profile/', ProfileManageView.as_view(),name='profile'),
    path('adminpanel/', AdminPanelView.as_view(),name='adminpanel'),
    path('doc/', UserDoctorView.as_view(),name='doc'),
]
