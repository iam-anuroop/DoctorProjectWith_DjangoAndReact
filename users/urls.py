from django.urls import path
from .views import RegisrationView,LoginView,ProfileManageView

urlpatterns = [
    path('', RegisrationView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('profile/', ProfileManageView.as_view(),name='profile'),
]
