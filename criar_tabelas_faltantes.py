import sys
sys.path.insert(0, 'estoque_web')

from app import app, db

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    # Verificar tabelas
    import sqlite3
    conn = sqlite3.connect('estoque_web/estoque_web.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    
    print("\nTabelas no banco:")
    for t in tabelas:
        print(f"  - {t[0]}")
    
    conn.close()
