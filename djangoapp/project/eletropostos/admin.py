from django.contrib import admin
# Importa todos os modelos que você criou baseados no Workbench
from .models import Estado, Cidade, Bairro, Lougradouro, Eletroposto, Conector

# Registra cada um para aparecer no painel
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Lougradouro)
admin.site.register(Eletroposto)
admin.site.register(Conector)