from django.urls import path
from . import views


urlpatterns = [
    path('checks/', views.CheckView.as_view(), name='check-list'),

]