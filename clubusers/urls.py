from django.urls import path

from clubusers import views

urlpatterns = [
    path('', views.UserProfileList.as_view()),
    path('<int:pk>/', views.UserProfileDetail.as_view()),
    path('login/', views.login),
    path('leaders/', views.LeaderProfileList.as_view()),
    path('leaders/<str:pk>/', views.LeaderProfileDetail.as_view()),
    path('followers/', views.FollowerProfileList.as_view()),
    path('followers/<str:pk>/', views.FollowerProfileDetail.as_view()),
    path('availabilities/', views.AvailabilityList.as_view()),
    path('availabilities/<str:pk>/', views.AvailabilityDetail.as_view()),
]
