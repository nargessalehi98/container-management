from django.urls import path

from manager.views import CreateAppAPIView, RunAppAPIView

urlpatterns = [
    path('create/', CreateAppAPIView.as_view()),
    path('run/<str:name>/', RunAppAPIView.as_view())
]
