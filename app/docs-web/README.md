# IoT Gateway - Documentação Arquitetônica Web

## 📚 Visão Geral

Aplicação web moderna para documentação completa do Sistema IoT do CEU Três Pontes. Interface interativa com documentação técnica detalhada da solução completa: 6 sensores ativos, Gateway MQTT, API REST com 29 endpoints, banco de dados MySQL com 6.000+ leituras e autenticação JWT.

## ✨ Características

- **Interface Moderna**: Design limpo e profissional
- **Navegação Intuitiva**: Sidebar com árvore de páginas
- **Multi-Scope**: Suporte para diferentes escopos (Global, Backend, Frontend, Sensors)
- **Exportação**: Exportar seções como HTML
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Interativo**: Animações suaves e feedback visual
- **Temas**: Esquema de cores profissional

## 🚀 Como Usar

### Abertura Local

1. **Navegue até a pasta do projeto:**
   ```powershell
   cd "c:\PI - IV - V1\docs-web"
   ```

2. **Abra o arquivo `doc_arq.html` no navegador:**
   - **Opção 1**: Clique duplo no arquivo `doc_arq.html`
   - **Opção 2**: Via PowerShell:
     ```powershell
     start doc_arq.html
     ```
   - **Opção 3**: Arraste o arquivo para o navegador

### Com Servidor Local (Recomendado)

Para melhor experiência, use um servidor HTTP local:

#### Python (se disponível):
```powershell
python -m http.server 8000
```
Acesse: http://localhost:8000

#### Node.js (se disponível):
```powershell
npx http-server -p 8000
```
Acesse: http://localhost:8000

#### VS Code Live Server:
1. Instale a extensão "Live Server"
2. Clique direito em `doc_arq.html`
3. Selecione "Open with Live Server"

## 📁 Estrutura de Arquivos

```
docs-web/
├── doc_arq.html            # Documentação da Arquitetura (página principal)
├── assets/
│   ├── css/
│   │   └── main.css       # Estilos da aplicação
│   └── js/
│       └── main.js        # JavaScript interativo
└── README.md              # Este arquivo
```

## 🎨 Seções Disponíveis

### Páginas Principais

1. **Início (Home)**
   - Visão geral do projeto
   - Cards de navegação rápida
   - Stack tecnológico

2. **Proposta Arquitetônica**
   - Visão geral da arquitetura
   - Camadas do sistema
   - Fluxo de dados
   - Características principais

3. **Modelo de Solução**
   - Estrutura de módulos
   - Componentes do backend
   - Módulo de sensores
   - Padrões de design

4. **Modelo de Topologia**
   - Topologia de rede
   - Infraestrutura
   - Componentes e status

5. **Integrações**
   - LoRa (Long Range)
   - Zigbee
   - Sigfox
   - RFID
   - Formato de mensagens

6. **Especificações API**
   - 29 Endpoints ativos organizados em 5 categorias
   - Autenticação JWT implementada
   - Documentação completa dos contratos REST

7. **Modelo de Dados**
   - Entidades principais
   - Schemas JSON
   - Estrutura de dados

8. **Segurança**
   - Medidas implementadas
   - Melhorias planejadas

9. **Operações**
   - Guias de inicialização
   - Monitoramento
   - Procedimentos operacionais

## 🔧 Funcionalidades Interativas

### Navegação
- **Sidebar**: Clique nos itens para navegar
- **Header**: Links de navegação rápida
- **Breadcrumbs**: Rastreamento de localização

### Seletor de Scope
- Dropdown no header
- Opções: GLOBAL, BACKEND, FRONTEND, SENSORS
- Filtra conteúdo por contexto

### Exportação
- Botão "Export" no header
- Exporta seção atual como HTML
- Download automático

### Atalhos de Teclado
- `Ctrl/Cmd + E`: Exportar seção atual
- `Ctrl/Cmd + P`: Imprimir seção atual
- `Ctrl/Cmd + K`: Focar na busca (se implementada)

### Copy Code
- Passe o mouse sobre blocos de código
- Botão "Copiar" aparece automaticamente
- Copia código para clipboard

## 🎯 Personalizações Disponíveis

### Cores (CSS Variables em `:root`)
```css
--primary-color: #2563eb;
--secondary-color: #1e40af;
--accent-color: #3b82f6;
--success-color: #10b981;
--warning-color: #f59e0b;
--danger-color: #ef4444;
```

### Adicionar Nova Seção
1. Adicione item na sidebar (HTML):
```html
<div class="nav-item" onclick="navigateTo('nova-secao')">
    <i class="fas fa-icon"></i> Nova Seção
</div>
```

2. Adicione conteúdo (HTML):
```html
<section id="nova-secao" class="content-section">
    <h1>Nova Seção</h1>
    <p>Conteúdo...</p>
</section>
```

## 📱 Responsividade

- **Desktop** (>1024px): Layout completo com sidebar
- **Tablet** (768-1024px): Sidebar colapsável
- **Mobile** (<768px): Menu hamburger, layout otimizado

## 🔍 SEO e Acessibilidade

- Estrutura semântica HTML5
- Tags meta apropriadas
- Contraste de cores acessível
- Navegação por teclado
- ARIA labels (pode ser expandido)

## 🚀 Melhorias Futuras

- [ ] Sistema de busca completo
- [ ] Modo escuro/claro
- [ ] Mais idiomas (EN, ES)
- [ ] Versionamento de documentação
- [ ] Comentários e feedback
- [ ] Integração com Git para histórico
- [ ] PDF export
- [ ] Markdown support
- [ ] API para geração dinâmica

## 📝 Manutenção

### Atualizar Conteúdo

1. Edite `doc_arq.html` diretamente
2. Modifique as seções `<section id="...">`
3. Salve e recarregue no navegador

### Atualizar Estilos
1. Edite `assets/css/main.css`
2. Use variáveis CSS para consistência
3. Teste responsividade

### Adicionar Funcionalidades
1. Edite `assets/js/main.js`
2. Use funções modulares
3. Adicione event listeners no DOMContentLoaded

## 🐛 Solução de Problemas

### Estilos não carregam
- Verifique se `assets/css/main.css` existe
- Confirme o caminho relativo
- Use servidor HTTP local

### JavaScript não funciona
- Abra o Console do navegador (F12)
- Verifique erros
- Confirme que `assets/js/main.js` foi carregado

### Ícones não aparecem
- Verifique conexão com internet (Font Awesome CDN)
- Ou baixe Font Awesome localmente

## 📄 Licença

Este projeto faz parte do trabalho acadêmico IoT Gateway.

## 👥 Contribuição

Para adicionar ou modificar conteúdo:
1. Clone o repositório
2. Faça as alterações
3. Teste localmente
4. Commit e push

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação técnica em `/docs`
- Verifique os exemplos em `/tests`

---

**Versão**: 2.0.0  
**Última atualização**: 20 de Outubro de 2025  
**Desenvolvido para**: Projeto Integrador IV - Sistema IoT Completo (CEU Três Pontes)
