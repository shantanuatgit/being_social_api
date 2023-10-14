from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
    path('signup/', views.UserCreateApiView.as_view()),
    path('<str:email>/', views.UserProfileFullUpdate.as_view()),
    path('follow/<int:pk>/', views.FollowerFollowingCreateDestroyApiView.as_view()),
    path('remove-follower/<int:pk>/', views.FollowerDestroyApiView.as_view()),
    path('follower/<str:email>/', views.FollowerListApiView.as_view()),
    path('following/<str:email>/', views.FollowingListApiView.as_view()),
]