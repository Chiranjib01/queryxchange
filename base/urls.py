from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('',views.home,name='home'),
    path('question/<str:pk>/',views.question,name='question'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('create-question/',views.createQuestion,name='create-question'),
    path('update-question/<str:pk>/',views.updateQuestion,name='update-question'),
    path('delete-question/<str:pk>/',views.deleteQuestion,name='delete-question'),
    path('delete-answer/<str:pk>/',views.deleteAnswer,name='delete-answer'),
    path('update-user/',views.updateUser,name='update-user'),
    path('topics/',views.topicsPage,name='topics'),
    path('activity/',views.activityPage,name='activity'),
    path('question/<str:pk>/answer',views.answer,name='answer'),
]