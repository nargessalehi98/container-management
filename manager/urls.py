from django.urls import path

from manager.views import (
    CreateAppAPIView,
    RunAppAPIView,
    AppListAPIView,
    UpdateAppAPIView,
    RemoveApiView,
    GetAppAPIView
)

urlpatterns = [
    path('create/', CreateAppAPIView.as_view()),
    path('run/<str:name>/', RunAppAPIView.as_view()),
    path('appList/', AppListAPIView.as_view()),
    path('updateApp/<str:name>/', UpdateAppAPIView.as_view()),
    path('removeApp/<str:name>/', RemoveApiView.as_view()),
    path('getApp/<str:name>/', GetAppAPIView.as_view())
]
