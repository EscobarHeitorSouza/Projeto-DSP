import re
import json
from .models import Estado, Cidade, Bairro, Lougradouro, Eletroposto, Conector

def processar_posto_json(data):
    """
    Destrincha o JSON bruto e popula a hierarquia relacional.
    Garante a limpeza de strings para evitar erros nos filtros de BI.
    """
    
    # 1. DICIONÁRIO DE NORMALIZAÇÃO DE ESTADOS
    # Essencial para que 'São Paulo' e 'SP' não criem entradas duplicadas
    ESTADOS_MAP = {
        'São Paulo': 'SP', 'SP': 'SP', 'Rio de Janeiro': 'RJ', 'RJ': 'RJ',
        'Minas Gerais': 'MG', 'MG': 'MG', 'Paraná': 'PR', 'PR': 'PR'
    }

    # 2. EXTRAÇÃO E LIMPEZA DE ENDEREÇO (DESTINCHAMENTO)
    endereco_bruto = data.get('formattedAddress', '')
    partes = [p.strip() for p in endereco_bruto.split(',')]
    
    # Regex para localizar o padrão "Cidade - UF" (ex: Campinas - SP)
    # Isso evita que o número da casa ou o CEP sejam confundidos com a cidade
    nome_cidade = "Campinas"
    sigla_uf = "SP"
    
    for parte in partes:
        match = re.search(r'(.+)\s+-\s+([A-Z]{2})', parte)
        if match:
            # Pegamos o que está antes do hífen (Cidade) e o que está depois (UF)
            nome_cidade = match.group(1).split(' - ')[-1].strip()
            sigla_uf = match.group(2).strip().upper()
            break

    # 3. POPULANDO HIERARQUIA RELACIONAL
    # Estado (Sigla de 2 letras)
    sigla_uf = ESTADOS_MAP.get(sigla_uf, sigla_uf[:2])
    obj_estado, _ = Estado.objects.get_or_create(
        cd_uf=sigla_uf, 
        defaults={'nm_estado': 'São Paulo' if sigla_uf == 'SP' else sigla_uf}
    )

    # Cidade (Vinculada ao Estado)
    obj_cidade, _ = Cidade.objects.get_or_create(nm_cidade=nome_cidade, estado=obj_estado)

    # Bairro (Extraído da parte anterior à cidade no endereço)
    nome_bairro = "Centro"
    for i, p in enumerate(partes):
        if nome_cidade in p and i > 0:
            nome_bairro = partes[i-1].split(' - ')[-1].strip()
            break
    obj_bairro, _ = Bairro.objects.get_or_create(nm_bairro=nome_bairro, cidade=obj_cidade)

    # Logradouro e CEP
    match_cep = re.search(r'\d{5}-\d{3}', endereco_bruto)
    cep = match_cep.group(0) if match_cep else "00000-000"
    obj_logradouro, _ = Lougradouro.objects.get_or_create(
        cd_cep=cep,
        bairro=obj_bairro,
        defaults={'nm_lougradouro': partes[0]}
    )

    # 4. SALVANDO O ATIVO (ELETROPOSTO)
    # O place_id garante que o registro seja único e não duplique na migração
    posto, _ = Eletroposto.objects.update_or_create(
        place_id=data.get('id'),
        defaults={
            'nm_eletroposto': data['displayName']['text'],
            'nm_latitude': str(data['location']['latitude']),
            'nm_longitude': str(data['location']['longitude']),
            'cd_status': 'Ativo',
            'lougradouro': obj_logradouro,
            'dados_completos_json': data 
        }
    )

    # 5. DESTRINCHANDO CONECTORES (DADOS TÉCNICOS)
    # Limpa conectores antigos para evitar inconsistência de hardware
    Conector.objects.filter(eletroposto=posto).delete()
    
    agregacao = data.get('evChargeOptions', {}).get('connectorAggregation', [])
    for item in agregacao:
        # Limpeza do nome (Ex: 'EV_CONNECTOR_TYPE_TYPE_2' -> 'TYPE 2')
        nome_tec = item.get('type', 'TYPE_2').replace('EV_CONNECTOR_TYPE_', '').replace('_', ' ')
        
        Conector.objects.create(
            eletroposto=posto,
            nm_conector=nome_tec,
            vl_quantidade=item.get('count', 1),
            vl_potencia=str(round(item.get('maxChargeRateKw', 0), 1))
        )
    
    return posto