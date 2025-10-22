import os

# Ler app.py
with open('app.py', 'r') as f:
    lines = f.readlines()

# Encontrar e modificar a linha com port=5000
new_lines = []
for line in lines:
    if 'port=5000' in line:
        line = line.replace('port=5000', 'port=int(os.getenv("API_PORT", 5001))')
    new_lines.append(line)

# Salvar
with open('app.py', 'w') as f:
    f.writelines(new_lines)

print('Corrigido!')
