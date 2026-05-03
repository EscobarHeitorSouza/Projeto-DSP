from django.urls import path
from . import views # Aqui o '.' aponta corretamente para eletropostos/views.py

urlpatterns = [
    # Define a rota para a tela de teste
    path('mapa/', views.mapa_eletropostos, name='mapa_eletropostos'),
]