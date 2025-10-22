"""
Script para aplicar refatoração da aplicação
Substitui as rotas antigas pelas refatoradas
"""

import os
import shutil
from datetime import datetime

# Diretório base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend', 'app')
ROUTES_DIR = os.path.join(BACKEND_DIR, 'routes')
BACKUP_DIR = os.path.join(BASE_DIR, 'backup_pre_refactoring')

def create_backup():
    """Criar backup dos arquivos antes da refatoração"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{BACKUP_DIR}_{timestamp}"
    
    print(f"📦 Criando backup em: {backup_path}")
    
    # Copiar estrutura atual
    shutil.copytree(
        BACKEND_DIR,
        backup_path,
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo')
    )
    
    print(f"✅ Backup criado com sucesso!")
    return backup_path

def apply_refactoring():
    """Aplicar refatoração"""
    print("\n🔄 Aplicando refatoração...")
    
    # Substituir auth.py
    old_auth = os.path.join(ROUTES_DIR, 'auth.py')
    new_auth = os.path.join(ROUTES_DIR, 'auth_refactored.py')
    
    if os.path.exists(new_auth):
        # Backup do arquivo antigo
        shutil.copy(old_auth, old_auth + '.old')
        
        # Substituir
        shutil.copy(new_auth, old_auth)
        print("✅ auth.py refatorado")
    
    print("\n✨ Refatoração concluída!")

def show_summary():
    """Mostrar resumo das mudanças"""
    print("\n" + "="*60)
    print("📊 RESUMO DA REFATORAÇÃO")
    print("="*60)
    print("\n✅ Novos Componentes Adicionados:")
    print("   📁 app/schemas/ - Validação com Marshmallow")
    print("   📁 app/services/ - Camada de lógica de negócio")
    print("   📁 app/utils/ - Utilitários e helpers")
    print("\n✅ Melhorias Implementadas:")
    print("   • Validação automática de requisições")
    print("   • Tratamento de erros padronizado")
    print("   • Separação de responsabilidades (SRP)")
    print("   • Código mais limpo e testável")
    print("   • Documentação aprimorada")
    print("\n✅ Rotas Refatoradas:")
    print("   • /api/v1/auth/* - Autenticação completa")
    print("\n📝 Próximos Passos:")
    print("   1. Refatorar rotas de sensores")
    print("   2. Refatorar rotas de leituras")
    print("   3. Refatorar rotas de estatísticas")
    print("   4. Adicionar testes unitários")
    print("="*60)

def main():
    print("="*60)
    print("🚀 REFATORAÇÃO DA APLICAÇÃO")
    print("="*60)
    
    # Criar backup automaticamente
    backup_path = create_backup()
    print(f"\n💾 Backup salvo em: {backup_path}")
    
    # Aplicar refatoração
    apply_refactoring()
    show_summary()
    
    print("\n✅ Refatoração aplicada com sucesso!")
    print("\n💡 Dica: Reinicie o servidor Flask para aplicar as mudanças")

if __name__ == "__main__":
    main()
