from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('skip_step/<str:step_name>/', views.skip_step,
         name="skip_step"),
    path('reset_game', views.reset_game, name="reset_game"),
    path('update_lights', views.update_lights, name="update_lights")
]
