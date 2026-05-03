from django.db import models

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nm_estado = models.CharField(max_length=45)
    cd_uf = models.CharField(max_length=2)

class Cidade(models.Model):
    id_cidade = models.AutoField(primary_key=True)
    nm_cidade = models.CharField(max_length=45)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Bairro(models.Model):
    id_bairro = models.AutoField(primary_key=True)
    nm_bairro = models.CharField(max_length=45)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)

class Lougradouro(models.Model):
    id_lougradouro = models.AutoField(primary_key=True)
    nm_lougradouro = models.CharField(max_length=100)
    cd_cep = models.CharField(max_length=10)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)

class Eletroposto(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    nm_eletroposto = models.CharField(max_length=255)
    nm_latitude = models.FloatField()
    nm_longitude = models.FloatField()
    cd_status = models.CharField(max_length=50, null=True)
    lougradouro = models.ForeignKey(Lougradouro, on_delete=models.CASCADE)
    dados_completos_json = models.JSONField() # Guarda o JSON original para consultas futuras

class Conector(models.Model):
    eletroposto = models.ForeignKey(Eletroposto, related_name='conectores', on_delete=models.CASCADE)
    nm_conector = models.CharField(max_length=100, null=True, blank=True)
    vl_potencia = models.CharField(max_length=50, null=True, blank=True)
    nm_tipo = models.CharField(max_length=45)
    vl_quantidade = models.CharField(max_length=50, null=True, blank=True)
