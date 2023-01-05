from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.sign_me_up, name='sign-me-up'),
    path('login/', views.log_me_in, name='login'),
    path('logout/', views.log_me_out, name='logout'),
    path('login_logs/', views.ListUserLogsView.as_view(), name='login_logs'),
]
