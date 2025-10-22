"""
Teste rápido de conexão com o banco
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv('backend/.env')

passwords_to_try = [
    os.getenv('DB_PASSWORD'),
    'password',
    '',
    'root',
    'CeuTresPontes2025!',
]

user = os.getenv('DB_USER', 'ceu_tres_pontes')
database = os.getenv('DB_NAME', 'ceu_tres_pontes_db')

print(f"🔍 Testando conexões para: {user}@localhost/{database}\n")

for i, pwd in enumerate(passwords_to_try, 1):
    try:
        print(f"{i}. Testando senha: {'(vazio)' if not pwd else '****' + pwd[-2:] if len(pwd) > 2 else '**'}... ", end='')
        conn = pymysql.connect(
            host='localhost',
            user=user,
            password=pwd,
            database=database,
            charset='utf8mb4'
        )
        print("✅ SUCESSO!")
        print(f"\n✨ Senha correta encontrada!")
        print(f"📝 Atualize seu .env com: DB_PASSWORD={pwd}")
        conn.close()
        break
    except pymysql.err.OperationalError as e:
        if '1045' in str(e):
            print("❌ Senha incorreta")
        else:
            print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
else:
    print("\n❌ Nenhuma senha funcionou!")
    print("\n💡 Dica: Verifique qual senha você usou ao criar o usuário MySQL")
