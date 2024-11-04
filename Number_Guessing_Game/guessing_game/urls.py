from django.urls import path
from .views import StartGameView, MakeGuessView

urlpatterns = [
    path('', StartGameView.as_view(), name='start_game'),
    path('guess/', MakeGuessView.as_view(), name='make_guess'),
]
