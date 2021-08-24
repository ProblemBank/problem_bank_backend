from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name = 'Account'

urlpatterns = [
    path('create/', CreateUserAPI.as_view(), name='create_user'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordAPI.as_view(), name='reset_password'),
]
