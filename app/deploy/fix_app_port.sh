#!/bin/bash

# Corrigir app.py para usar porta do .env

cd /var/www/smartceu/app/backend

# Backup
cp app.py app.py.backup_port

# Usar Python para fazer a correção
python3 << 'PYEOF'
import re

# Ler arquivo
with open('app.py', 'r') as f:
    content = f.read()

# Encontrar e substituir o bloco if __name__
pattern = r"if __name__ == '__main__':\s+app\.run\(\s+host='0\.0\.0\.0',\s+port=\d+,\s+debug=True\s+\)"

replacement = """if __name__ == '__main__':
    import os
    port = int(os.getenv('API_PORT', 5001))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )"""

# Substituir
content_new = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Salvar
with open('app.py', 'w') as f:
    f.write(content_new)

print("✅ app.py corrigido para usar porta do .env (API_PORT=5001)")
PYEOF

# Mostrar resultado
echo ""
echo "=== Últimas linhas do app.py corrigido ==="
tail -n 12 app.py

# Alterar dono
chown www-data:www-data app.py

echo ""
echo "✅ Correção aplicada!"
