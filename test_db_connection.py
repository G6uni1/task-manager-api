from app.core.config import settings
import psycopg2

try:
    conn = psycopg2.connect(settings.DATABASE_URL)
    print("✅ Conexão com PostgreSQL estabelecida com sucesso!")
    print(f"Banco conectado: {conn.info.dbname}")
    conn.close()
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")