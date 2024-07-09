from django.urls import path

from meetings import views

urlpatterns = [
    path('<str:meeting_id>/events/', views.MeetingEventList.as_view()),
    path('<str:meeting_id>/events/<int:pk>', views.MeetingEventDetail.as_view()),
    path('<str:meeting_id>/reviews/', views.MeetingReviewList.as_view()),
    path('<str:meeting_id>/reviews/<int:pk>', views.MeetingReviewDetail.as_view()),
    path('', views.MeetingList.as_view()),
    path('<str:pk>/', views.MeetingDetail.as_view()),
]
