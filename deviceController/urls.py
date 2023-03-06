from django.urls import path

from . import views

urlpatterns = [
    # ------------ Web pages ----------------- #
    path('', views.index, name='index'),
    path('light_control', views.light_control, name="light_control"),
    # ------------ Handling actions and buttons----------------- #
    path('skip_step/<str:step_name>/', views.skip_step, name="skip_step"),
    path('reset_game', views.reset_game, name="reset_game"),
    path('update_lights', views.update_lights, name="update_lights"),
    path("liberar_grillete/<int:grillete>",
         views.liberar_grillete, name="liberar_grillete"),
    path("abrir_cajon/<str:cajon>", views.abrir_cajon, name="abrir_cajon"),
    path("iniciar_sala", views.iniciar_sala, name="iniciar_sala"),
    path("radio_vol_up", views.radio_vol_up, name="radio_vol_up"),
    path("radio_vol_down", views.radio_vol_down, name="radio_vol_down"),
    path("sistema_audio_vol_up", views.sistema_audio_vol_up,
         name="sistema_audio_vol_up"),
    path("sistema_audio_vol_down", views.sistema_audio_vol_down,
         name="sistema_audio_vol_down"),
]
