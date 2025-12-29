from django.urls import path , include
from home.views import LoginView, RegisterView , ProfileModelViewSet , FollowViewSet , PostModelViewSet
from rest_framework.routers import DefaultRouter

profile_router = DefaultRouter()
profile_router.register(r"myporfile",ProfileModelViewSet, basename = 'myprofile')
urlpatterns = profile_router.urls

post_router = DefaultRouter()
post_router.register(r"post",PostModelViewSet,basename = "post")

urlpatterns = post_router.urls 

urlpatterns = [
    path('post/',include(post_router.urls)),
    path('follow/',FollowViewSet.as_view()),
    path('myprofile/',include(profile_router.urls)),
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
]
