#!/usr/bin/env python3
"""
Script para limpar leituras existentes e repopular com timezone correto
"""

from app import create_app, db
from app.models.reading import Reading
from app.models.pool_reading import PoolReading

def clear_and_repopulate():
    """Limpa todas as leituras do banco de dados"""
    
    app = create_app()
    with app.app_context():
        print('='*70)
        print('Limpando leituras existentes do banco de dados')
        print('='*70)
        print()
        
        # Contar leituras existentes
        sensor_readings_count = Reading.query.count()
        pool_readings_count = PoolReading.query.count()
        
        print(f'📊 Leituras encontradas:')
        print(f'   Sensores: {sensor_readings_count}')
        print(f'   Piscina:  {pool_readings_count}')
        print()
        
        if sensor_readings_count == 0 and pool_readings_count == 0:
            print('✅ Nenhuma leitura para limpar!')
            return
        
        # Confirmar
        response = input('❓ Deseja limpar TODAS as leituras? (s/N): ')
        if response.lower() != 's':
            print('Operação cancelada.')
            return
        
        print()
        print('🗑️  Limpando leituras...')
        
        # Limpar readings
        if sensor_readings_count > 0:
            Reading.query.delete()
            print(f'   ✅ {sensor_readings_count} leituras de sensores removidas')
        
        # Limpar pool_readings
        if pool_readings_count > 0:
            PoolReading.query.delete()
            print(f'   ✅ {pool_readings_count} leituras de piscina removidas')
        
        # Commit
        db.session.commit()
        
        print()
        print('='*70)
        print('✅ Banco de dados limpo com sucesso!')
        print('='*70)
        print()
        print('📝 Próximos passos:')
        print('   1. Execute: python3 populate_readings.py')
        print('   2. Execute: python3 populate_pool_readings.py')
        print()

if __name__ == '__main__':
    clear_and_repopulate()
