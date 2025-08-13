from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile_view, signup_view


urlpatterns = [
    path('profile/<str:username>/', profile_view, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/signup/', signup_view, name='signup'),
]

