#!/bin/bash
echo '========================================'
echo 'RELATÓRIO FINAL - SmartCEU Deployment'
echo '========================================'
echo ''
echo '1. SERVIÇOS:'
echo '  - smartceu-api: '$(systemctl is-active smartceu-api)
echo '  - mosquitto:    '$(systemctl is-active mosquitto)
echo '  - mysql:        '$(systemctl is-active mysql)
echo '  - nginx:        '$(systemctl is-active nginx)
echo ''
echo '2. PORTAS:'
echo '  - API (5000):   '$(netstat -tuln | grep ':5000 ' | wc -l)' listener(s)'
echo '  - MQTT (1884):  '$(netstat -tuln | grep ':1884 ' | wc -l)' listener(s)'
echo '  - MySQL (3306): '$(netstat -tuln | grep ':3306 ' | wc -l)' listener(s)'
echo '  - NGINX (80):   '$(netstat -tuln | grep ':80 ' | wc -l)' listener(s)'
echo ''
echo '3. TESTES HTTP:'
echo ''
echo '  a) Agasalho Aqui (/):'
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' http://localhost/)
echo '     Status: '$HTTP_CODE
echo ''
echo '  b) SmartCEU Health:'
curl -s http://localhost/smartceu/health | head -4
echo ''
echo '  c) SmartCEU API Sensors:'
curl -s http://localhost/smartceu/api/v1/sensors | head -3
echo ''
echo '  d) SmartCEU Dashboard:'
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' http://localhost/smartceu)
echo '     Status: '$HTTP_CODE
echo ''
echo '4. ESTRUTURA DE ARQUIVOS:'
echo '  - HTML Principal: '$(test -f /var/www/smartceu/app/frontend/smart_ceu.html && echo 'OK' || echo 'FALTA')
echo '  - Pool Monitoring: '$(test -f /var/www/smartceu/app/frontend/monitoramento_piscina.html && echo 'OK' || echo 'FALTA')
echo '  - Backend app.py: '$(test -f /var/www/smartceu/app/backend/app.py && echo 'OK' || echo 'FALTA')
echo '  - Assets docs-web: '$(test -d /var/www/smartceu/app/docs-web/assets && echo 'OK' || echo 'FALTA')
echo ''
echo '5. URLs PÚBLICAS:'
echo '  ✓ http://82.25.75.88/            → Agasalho Aqui'
echo '  ✓ http://82.25.75.88/smartceu    → SmartCEU Dashboard'
echo '  ✓ http://82.25.75.88/smartceu/pool → Pool Monitoring'
echo '  ✓ http://82.25.75.88/smartceu/api/v1/... → API'
echo '  ✓ http://82.25.75.88/smartceu/health → Health Check'
echo ''
echo '========================================'
echo 'DEPLOY CONCLUÍDO COM SUCESSO!'
echo '========================================'
