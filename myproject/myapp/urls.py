from django.urls import path

from . import views

urlpatterns = [
    path('', views.prehome, name='prehome'),
    path('create_problem/', views.create_problem, name='create_problem'),
    path('home/', views.problem_list, name='problem_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.profile_view, name='profile'),
]