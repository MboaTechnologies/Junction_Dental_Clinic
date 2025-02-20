from django.urls import path
from .views import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication
    path('accounts/profile/update', views. profile_Update, name='user_profile_update'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('accounts/profile/view', views.user_profile_view, name='user_profile_view'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/includes/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/includes/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/includes/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/includes/password_reset_complete.html'
    ), name='password_reset_complete'),
]
