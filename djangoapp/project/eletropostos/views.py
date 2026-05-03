from django.shortcuts import render
from .models import Eletroposto, Estado, Cidade

def mapa_eletropostos(request):
    postos = Eletroposto.objects.all().select_related('lougradouro__bairro__cidade__estado')
    estados = Estado.objects.all().order_by('nm_estado')
    # O distinct garante que Campinas apareça apenas uma vez
    cidades = Cidade.objects.all().order_by('nm_cidade').distinct()
    
    return render(request, 'eletropostos/mapa.html', {
        'postos': postos,
        'estados': estados,
        'cidades': cidades
    })