"""
Script para criar tabelas diretamente com PyMySQL (sem SQLAlchemy)
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print("=== CRIAÇÃO MANUAL DE TABELAS ===\n")

# Conexão
connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'ceu_tres_pontes'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'ceu_tres_pontes_db'),
    charset='utf8mb4'
)

cursor = connection.cursor()

# SQL para criar tabelas
tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS sensors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        serial_number VARCHAR(100) NOT NULL UNIQUE,
        protocol VARCHAR(20) NOT NULL,
        location VARCHAR(255) NOT NULL,
        description TEXT,
        status ENUM('active', 'inactive', 'maintenance', 'error') DEFAULT 'active',
        battery_level SMALLINT,
        signal_strength SMALLINT,
        total_readings BIGINT DEFAULT 0,
        last_reading_at DATETIME,
        installed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_serial (serial_number),
        INDEX idx_protocol (protocol),
        INDEX idx_status (status),
        INDEX idx_location (location(100))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    """
    CREATE TABLE IF NOT EXISTS readings (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        sensor_id INT NOT NULL,
        activity SMALLINT NOT NULL,
        timestamp DATETIME NOT NULL,
        sensor_metadata JSON,
        message_id VARCHAR(100),
        gateway_id VARCHAR(50),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE,
        INDEX idx_sensor_timestamp (sensor_id, timestamp),
        INDEX idx_timestamp_activity (timestamp, activity),
        INDEX idx_sensor_activity (sensor_id, activity),
        INDEX idx_gateway_timestamp (gateway_id, timestamp),
        INDEX idx_timestamp (timestamp),
        INDEX idx_message_id (message_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) NOT NULL UNIQUE,
        email VARCHAR(120) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(80),
        last_name VARCHAR(80),
        role ENUM('admin', 'operator', 'viewer') DEFAULT 'viewer',
        is_active BOOLEAN DEFAULT TRUE,
        last_login_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_username (username),
        INDEX idx_email (email),
        INDEX idx_role (role)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    """
    CREATE TABLE IF NOT EXISTS alerts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sensor_id INT NOT NULL,
        alert_type VARCHAR(50) NOT NULL,
        severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
        message TEXT NOT NULL,
        is_resolved BOOLEAN DEFAULT FALSE,
        resolved_at DATETIME,
        resolved_by INT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE,
        FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL,
        INDEX idx_sensor (sensor_id),
        INDEX idx_type (alert_type),
        INDEX idx_severity (severity),
        INDEX idx_resolved (is_resolved),
        INDEX idx_created (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    """
    CREATE TABLE IF NOT EXISTS statistics (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        sensor_id INT,
        total_readings INT DEFAULT 0,
        total_detections INT DEFAULT 0,
        avg_signal_strength FLOAT,
        min_battery_level SMALLINT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE,
        UNIQUE KEY unique_date_sensor (date, sensor_id),
        INDEX idx_date (date),
        INDEX idx_sensor (sensor_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
]

# Criar tabelas
for i, sql in enumerate(tables_sql, 1):
    table_name = sql.split("IF NOT EXISTS ")[1].split(" (")[0]
    try:
        cursor.execute(sql)
        print(f"✅ Tabela {i}/5: {table_name}")
    except Exception as e:
        print(f"❌ Erro ao criar {table_name}: {e}")

# Commit
connection.commit()

# Verificar tabelas criadas
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print(f"\n✅ Total de tabelas criadas: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

cursor.close()
connection.close()

print("\n🎉 BANCO DE DADOS INICIALIZADO COM SUCESSO!")
