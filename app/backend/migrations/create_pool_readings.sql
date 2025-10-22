-- ============================================================
-- SMARTCEU - MONITORAMENTO DA PISCINA
-- Tabela para armazenar leituras dos sensores da piscina
-- ============================================================

CREATE TABLE IF NOT EXISTS pool_readings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Tipo do sensor
    sensor_type ENUM('water_temp', 'ambient_temp', 'water_quality') NOT NULL,
    
    -- Data e hora da leitura
    reading_date DATE NOT NULL,
    reading_time TIME NOT NULL,
    
    -- Valores (temperatura em Celsius)
    temperature DECIMAL(5,2) NULL COMMENT 'Temperatura em Celsius (20-40°C)',
    
    -- Qualidade da água (apenas para sensor water_quality)
    water_quality ENUM('Ótima', 'Boa', 'Regular', 'Imprópria') NULL,
    
    -- Metadados
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para otimizar consultas
    INDEX idx_date_time (reading_date, reading_time),
    INDEX idx_sensor_type (sensor_type),
    INDEX idx_created_at (created_at),
    INDEX idx_composite (sensor_type, reading_date, reading_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Leituras dos sensores de monitoramento da piscina';

-- ============================================================
-- Inserir dados de exemplo para teste
-- ============================================================

INSERT INTO pool_readings (sensor_type, reading_date, reading_time, temperature, water_quality) VALUES
-- Temperatura da Água
('water_temp', CURDATE(), '08:00:00', 24.5, NULL),
('water_temp', CURDATE(), '12:00:00', 27.8, NULL),
('water_temp', CURDATE(), '16:00:00', 29.2, NULL),

-- Temperatura Ambiente
('ambient_temp', CURDATE(), '08:00:00', 26.3, NULL),
('ambient_temp', CURDATE(), '12:00:00', 32.5, NULL),
('ambient_temp', CURDATE(), '16:00:00', 34.1, NULL),

-- Qualidade da Água
('water_quality', CURDATE(), '08:00:00', NULL, 'Ótima'),
('water_quality', CURDATE(), '12:00:00', NULL, 'Ótima'),
('water_quality', CURDATE(), '16:00:00', NULL, 'Boa');
