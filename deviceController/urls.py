from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('skip_step/<str:step_name>/', views.skip_step,
         name="skip_step"),
]
