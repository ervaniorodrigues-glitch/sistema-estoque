# Lógica de Programação de Devolução e Prorrogação de Empréstimos

## Resumo da Implementação

A lógica de cores e prorrogação foi implementada conforme solicitado. O sistema agora marca visualmente o status de cada empréstimo através de cores de fundo e fonte.

---

## Fluxo de Cores e Estados

### 1. **EMPRÉSTIMO NORMAL (Sem Prorrogação)**
- **Cor de Fundo**: Branco (padrão)
- **Dias Restantes**: Contagem regressiva normal (ex: "5 dias restantes")
- **Ação**: Usuário pode devolver ou prorrogar

### 2. **FALTA 1 DIA PARA VENCER**
- **Cor de Fundo**: Vermelho Clarinho (`#ffe6e6`)
- **Cor da Fonte**: Preta (normal)
- **Dias Restantes**: "1 dia (vence amanhã)"
- **Destaque**: Leve, apenas para marcar atenção

### 3. **VENCE HOJE**
- **Cor de Fundo**: Branco
- **Cor da Fonte**: Vermelha com Negrito
- **Dias Restantes**: "VENCE HOJE"
- **Destaque**: Forte, para alertar urgência

### 4. **PRAZO VENCIDO (Não Devolvido)**
- **Cor de Fundo**: Vermelho Clarinho (`#ffcccc`)
- **Cor da Fonte**: Vermelha com Negrito
- **Dias Restantes**: "VENCIDO (X dias)"
- **Destaque**: Forte, linha toda vermelha para indicar atraso

### 5. **PRORROGAÇÃO (Nova Data Definida)**
- **Cor de Fundo**: Verde Clarinho (`#e6ffe6`)
- **Cor da Fonte**: Preta (normal)
- **Dias Restantes**: "X dias restantes (prorrogado)"
- **Destaque**: Verde para indicar que foi prorrogado
- **Ação**: Se vencer novamente, volta para vermelho

### 6. **DEVOLVIDO**
- **Cor de Fundo**: Branco (padrão)
- **Cor da Fonte**: Verde (status-devolvido)
- **Dias Restantes**: Dias entre empréstimo e devolução
- **Destaque**: Nenhum, apenas indicação de status

---

## Como Funciona a Prorrogação

### Processo:
1. **Usuário seleciona um empréstimo EMPRESTADO**
2. **Preenche a data de devolução com uma NOVA data**
3. **Clica em "Alterar"** (botão muda de cor para amarelo)
4. **Sistema registra a prorrogação**:
   - Salva a data anterior em `data_devolucao` (marca que houve prorrogação)
   - Atualiza `data_devolucao_prevista` com a nova data
   - Linha fica **VERDE CLARINHA** para destacar prorrogação

### Comportamento Após Prorrogação:
- Se a nova data for cumprida: Linha volta ao normal
- Se a nova data vencer: Linha fica **VERMELHA** novamente
- Se prorrogar novamente: Volta para **VERDE CLARINHA**

---

## Campos do Banco de Dados

```
Emprestimo:
├── data_devolucao_prevista  → Data planejada para devolução
├── data_devolucao           → Data real de devolução (ou data anterior se prorrogado)
└── status                   → EMPRESTADO ou DEVOLVIDO
```

### Lógica de Detecção de Prorrogação:
- Se `data_devolucao` está preenchida E `status = EMPRESTADO` → É uma prorrogação
- Se `data_devolucao` está vazio E `status = EMPRESTADO` → É um empréstimo normal

---

## Contagem Regressiva

A contagem é **decrescente** e atualiza automaticamente:

```
Hoje: 21/01/2026
Data Prevista: 25/01/2026

21/01 → "4 dias restantes"
22/01 → "3 dias restantes"
23/01 → "2 dias restantes"
24/01 → "1 dia (vence amanhã)" [VERMELHO CLARINHO]
25/01 → "VENCE HOJE" [BRANCO + FONTE VERMELHA NEGRITO]
26/01 → "VENCIDO (1 dia)" [VERMELHO CLARINHO + FONTE VERMELHA NEGRITO]
```

---

## Fluxo Visual Completo

```
┌─────────────────────────────────────────────────────────────┐
│ EMPRÉSTIMO NORMAL                                           │
│ Fundo: Branco | Fonte: Preta | "5 dias restantes"         │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   [Usuário Prorrogar]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PRORROGAÇÃO ATIVA                                           │
│ Fundo: Verde Clarinho | Fonte: Preta | "5 dias (prorrogado)"│
└─────────────────────────────────────────────────────────────┘
                          ↓
                   [Passar 4 dias]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ FALTA 1 DIA                                                 │
│ Fundo: Vermelho Clarinho | Fonte: Preta | "1 dia"         │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   [Passar 1 dia]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ VENCE HOJE                                                  │
│ Fundo: Branco | Fonte: Vermelha Negrito | "VENCE HOJE"    │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   [Passar 1 dia]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ VENCIDO                                                     │
│ Fundo: Vermelho Clarinho | Fonte: Vermelha Negrito | "VENCIDO"│
└─────────────────────────────────────────────────────────────┘
                          ↓
                   [Usuário Devolver]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ DEVOLVIDO                                                   │
│ Fundo: Branco | Fonte: Verde | "X dias de empréstimo"     │
└─────────────────────────────────────────────────────────────┘
```

---

## Alterações Realizadas

### Frontend (estoque_web/templates/emprestimos.html)
- ✅ Função `exibirEmprestimos()` atualizada com lógica de cores
- ✅ Detecção de prorrogação via `data_devolucao` preenchida
- ✅ Cores aplicadas dinamicamente ao renderizar tabela
- ✅ Função `alterarEmprestimo()` agora diferencia devolução de prorrogação

### Backend (estoque_web/app.py)
- ✅ Nova rota `/api/emprestimos/<id>/prorrogar` para prorrogações
- ✅ Lógica de registro de prorrogação em `data_devolucao`
- ✅ Conversão de datas de datetime-local para formato brasileiro

---

## Como Testar

1. **Criar um empréstimo** com data de devolução em 5 dias
2. **Observar a linha** com cor normal
3. **Selecionar o empréstimo** e alterar a data para 3 dias depois
4. **Clicar em "Alterar"** → Linha fica VERDE
5. **Aguardar 2 dias** (ou simular alterando a data do sistema)
6. **Recarregar a página** → Linha fica VERMELHA CLARINHA
7. **Aguardar mais 1 dia** → Linha fica BRANCA com FONTE VERMELHA NEGRITO
8. **Devolver o item** → Linha volta ao normal com status DEVOLVIDO

---

## Notas Importantes

- A contagem de dias é **automática** e atualiza ao recarregar a página
- A cor muda conforme a data do sistema
- Prorrogações são **ilimitadas** - o usuário pode prorrogar quantas vezes quiser
- Cada prorrogação marca a data anterior em `data_devolucao`
- O sistema diferencia automaticamente entre devolução e prorrogação pelo status

