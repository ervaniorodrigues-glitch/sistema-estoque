# 🚀 Guia Definitivo - Render com Backup Automático

## ✅ Vantagens do Render
- Sistema fica online (hiberna após 15min de inatividade)
- Quando alguém acessa, acorda automaticamente em ~30 segundos
- PostgreSQL gratuito
- Deploy automático via Git

## ⚠️ Problema: Dados do PostgreSQL são perdidos quando hiberna

## 💡 Solução: Sistema de Backup/Restore Rápido

---

## 📋 Passo 1: Acessar o Render

1. Acesse: https://dashboard.render.com
2. Faça login
3. Você já deve ter:
   - ✅ Web Service: `sistema-estoque-cjjg`
   - ✅ PostgreSQL: `estoque_sht3`

---

## 📋 Passo 2: Manter o Sistema Acordado (Opcional)

Se você quiser que o sistema fique sempre ativo, existem serviços gratuitos que fazem ping:

### Opção A: UptimeRobot (Recomendado)
1. Acesse: https://uptimerobot.com
2. Crie conta gratuita
3. Adicione monitor:
   - URL: `https://sistema-estoque-cjjg.onrender.com`
   - Intervalo: 5 minutos
4. O UptimeRobot vai acessar seu site a cada 5 minutos, mantendo-o acordado

### Opção B: Cron-Job.org
1. Acesse: https://cron-job.org
2. Crie conta gratuita
3. Adicione job:
   - URL: `https://sistema-estoque-cjjg.onrender.com`
   - Intervalo: 5 minutos

---

## 📋 Passo 3: Workflow de Uso Diário

### Quando o sistema hibernar:

1. **Acesse o sistema**: `https://sistema-estoque-cjjg.onrender.com`
2. **Aguarde 30 segundos** (ele vai acordar)
3. **Faça login** com: `master` / `@Senha01`
4. **Vá em Configurações → Backup/Restore**
5. **Clique em "Restaurar Backup"**
6. **Selecione o último backup** do seu computador
7. **Aguarde a importação** (alguns segundos)
8. **Pronto!** Todos os dados estão de volta

### Antes de sair do sistema:

1. **Vá em Configurações → Backup/Restore**
2. **Clique em "Fazer Backup"**
3. **Baixe o arquivo** para seu computador
4. **Guarde em uma pasta** (ex: `Backups_Sistema`)

---

## 📋 Passo 4: Automatizar Backup (Futuro)

Posso adicionar uma funcionalidade que:
- Faz backup automático a cada hora
- Envia por email
- Ou salva no Google Drive

Quer que eu implemente isso?

---

## 🔧 Comandos Úteis

### Ver logs do Render:
1. Acesse: https://dashboard.render.com
2. Clique no seu web service
3. Clique em "Logs"

### Forçar novo deploy:
1. Acesse: https://dashboard.render.com
2. Clique no seu web service
3. Clique em "Manual Deploy" → "Deploy latest commit"

---

## 📊 Resumo

| Situação | Solução |
|----------|---------|
| Sistema hibernou | Acesse a URL, aguarde 30s |
| Dados sumiram | Restaure o último backup |
| Quer manter acordado | Use UptimeRobot |
| Fazer backup | Configurações → Backup |

---

## 🎯 Próximos Passos

1. Configure o UptimeRobot para manter o sistema acordado
2. Crie uma rotina de fazer backup diário
3. Guarde os backups em uma pasta organizada
4. Considere contratar HostGator no futuro para ter mais estabilidade

---

**URL do Sistema**: https://sistema-estoque-cjjg.onrender.com
**Usuário**: master
**Senha**: @Senha01

---

Quer que eu te ajude a configurar o UptimeRobot agora?
