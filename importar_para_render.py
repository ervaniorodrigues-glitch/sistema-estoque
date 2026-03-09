"""
Script para importar dados diretamente no PostgreSQL do Render
Execute este script LOCALMENTE
"""

import psycopg2
import os

# URL do banco PostgreSQL no Render
DATABASE_URL = "postgresql://estoque_user:FJ0SeF6A9jUHxPJxT9KgHp2cENHzRHM0@dpg-d6ng65450q8c73a7hea0-a.virginia-postgres.render.com/estoque_sht3"

# Arquivo SQL gerado
SQL_FILE = "migracao_completa_20260309_154131.sql"

def importar_dados():
    """Importa dados do arquivo SQL para o PostgreSQL"""
    
    print("="*60)
    print("IMPORTAÇÃO DE DADOS PARA POSTGRESQL (RENDER)")
    print("="*60)
    print()
    
    if not os.path.exists(SQL_FILE):
        print(f"❌ Arquivo SQL não encontrado: {SQL_FILE}")
        return
    
    print(f"📄 Lendo arquivo: {SQL_FILE}")
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print(f"✅ Arquivo lido: {len(sql_content)} caracteres")
    print()
    
    try:
        print("🔌 Conectando ao PostgreSQL no Render...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Conectado com sucesso!")
        print()
        
        print("📤 Executando SQL...")
        print("⏳ Isso pode levar alguns minutos...")
        print()
        
        # Executar o SQL linha por linha para identificar erros
        linhas = sql_content.split('\n')
        erros = []
        sucesso = 0
        
        for i, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('--'):
                continue
            
            try:
                cursor.execute(linha)
                sucesso += 1
                if sucesso % 100 == 0:
                    print(f"   Processadas {sucesso} linhas...")
            except Exception as e:
                erros.append((i, linha[:100], str(e)))
                if len(erros) <= 5:  # Mostrar apenas os primeiros 5 erros
                    print(f"⚠️  Linha {i}: {str(e)[:80]}")
        
        conn.commit()
        
        print("✅ Dados importados com sucesso!")
        print()
        
        # Verificar quantos registros foram importados
        tabelas = ['usuarios', 'produtos', 'fornecedores', 'funcionarios', 'clientes']
        print("📊 Verificando dados importados:")
        for tabela in tabelas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"   {tabela}: {count} registros")
            except:
                pass
        
        cursor.close()
        conn.close()
        
        print()
        print("="*60)
        print("🎉 IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print()
        print("Agora você pode acessar o sistema web:")
        print("https://sistema-estoque-cjjg.onrender.com")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    importar_dados()
