import os
import sqlite3
import django
import json

# 1. Configura o Django para reconhecer os Models e o Postgres
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from eletropostos.services import processar_posto_json

def iniciar_migracao(caminho_sqlite):
    if not os.path.exists(caminho_sqlite):
        print(f"❌ Erro: O arquivo {caminho_sqlite} não foi encontrado.")
        return

    # 2. Conecta no banco antigo (SQLite)
    print(f"🔌 Conectando ao SQLite: {caminho_sqlite}")
    conn = sqlite3.connect(caminho_sqlite)
    cursor = conn.cursor()

    try:
        # 3. Busca a coluna JSON (ajuste o nome da tabela/coluna se necessário)
        cursor.execute("SELECT dados_completos_json FROM eletropostos")
        rows = cursor.fetchall()
        
        total = len(rows)
        print(f"📊 {total} registros encontrados. Iniciando processamento...")

        for i, row in enumerate(rows, 1):
            json_bruto = row[0]
            
            # Converte para dicionário se for string
            if isinstance(json_bruto, str):
                dados_dict = json.loads(json_bruto)
            else:
                dados_dict = json_bruto

            # 4. Usa a sua lógica de negócio para salvar no Postgres
            # Isso vai criar automaticamente o Estado, Cidade, Bairro e Posto
            processar_posto_json(dados_dict)
            
            if i % 10 == 0:
                print(f"✅ Processados {i}/{total}...")

        print("\n🏆 Migração concluída com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Certifique-se de que o nome do arquivo coincida com o seu .db
    iniciar_migracao('evcs_database.db')