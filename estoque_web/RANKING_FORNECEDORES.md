# 📊 Ranking de Fornecedores - Dashboard

## 🎯 Funcionalidade Implementada

Sistema de ranking de fornecedores por gastos no dashboard principal, com filtros de categoria e ano.

---

## ✨ Características

### 1. **Visualização em Tempo Real**
- Gráfico de barras horizontais coloridas
- Top 10 fornecedores com maior gasto
- Porcentagem relativa ao maior valor
- Total gasto exibido em destaque

### 2. **Filtros Disponíveis**

#### Filtro por Categoria
- Lista todas as categorias cadastradas no sistema
- Opção "Todas as Categorias" para visão geral
- Atualização automática ao selecionar

#### Filtro por Ano
- Últimos 5 anos disponíveis
- Opção "Todos os Anos" para histórico completo
- Baseado na data de cadastro dos produtos

### 3. **Cálculo de Gastos**
```
Gasto por Fornecedor = Σ (Preço de Compra × Estoque Atual)
```

Para cada produto:
- Considera apenas produtos ativos
- Multiplica preço de compra pelo estoque atual
- Agrupa por fornecedor
- Soma todos os valores

---

## 🎨 Interface

### Cards de Estatísticas (Topo)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  📦 36      │  👥 16      │  🏢 3       │  👤 0       │
│  Produtos   │ Funcionários│ Fornecedores│  Clientes   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Painel de Ranking
```
┌─────────────────────────────────────────────────────────┐
│ 📊 RANKING DE FORNECEDORES POR GASTOS                   │
├─────────────────────────────────────────────────────────┤
│ Categoria: [Todas ▼]  Ano: [Todos ▼]  Total: R$ 3.061,75│
├─────────────────────────────────────────────────────────┤
│ 1º Bosch        ████████████████████████ 100% R$ 1.447,74│
│ 2º Hengst       ████████████████         65%  R$ 512,43  │
│ 3º Ascorel      ████████                 35%  R$ 553,14  │
│ 4º Weg          ██                       8%   R$ 188,99  │
│ ...                                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Implementação Técnica

### Frontend (index.html)

**Funções JavaScript:**
- `carregarCategorias()` - Popula dropdown de categorias
- `carregarAnos()` - Popula dropdown de anos (últimos 5)
- `carregarRanking()` - Busca dados da API
- `renderizarRanking(data)` - Renderiza barras coloridas
- `obterCor(index)` - Define cores para cada posição
- `formatarMoeda(valor)` - Formata valores em R$

**Estilos CSS:**
- `.ranking-bar` - Container de cada barra
- `.ranking-bar-fill` - Barra preenchida com gradiente
- `.ranking-value` - Valor em reais
- `.ranking-filters` - Área de filtros

### Backend (app.py)

**Rota:** `GET /api/ranking-fornecedores`

**Parâmetros:**
- `categoria` (opcional) - Nome da categoria
- `ano` (opcional) - Ano para filtrar

**Resposta JSON:**
```json
{
  "ranking": [
    {
      "fornecedor": "Bosch",
      "total": 1447.74
    },
    {
      "fornecedor": "Hengst",
      "total": 512.43
    }
  ],
  "total_gasto": 3061.75
}
```

**Query SQL:**
```sql
SELECT 
    fornecedor,
    SUM(preco_compra * estoque_atual) as total_gasto
FROM produtos
WHERE 
    fornecedor IS NOT NULL 
    AND fornecedor != ''
    AND ativo = 1
    [AND categoria = ?]
    [AND YEAR(data_cadastro) = ?]
GROUP BY fornecedor
ORDER BY total_gasto DESC
LIMIT 10
```

---

## 📈 Exemplos de Uso

### Caso 1: Visão Geral
```
Filtros: Todas as Categorias | Todos os Anos
Resultado: Top 10 fornecedores de todo o histórico
```

### Caso 2: Categoria Específica
```
Filtros: EPI | Todos os Anos
Resultado: Top 10 fornecedores de EPIs
```

### Caso 3: Análise Anual
```
Filtros: Todas as Categorias | 2022
Resultado: Top 10 fornecedores de 2022
```

### Caso 4: Análise Detalhada
```
Filtros: ELÉTRICA | 2022
Resultado: Top 10 fornecedores de produtos elétricos em 2022
```

---

## 🎨 Cores do Ranking

As barras usam gradientes diferentes para cada posição:

1. 🔴 Vermelho (#e74c3c → #c0392b)
2. 🔵 Azul (#3498db → #2980b9)
3. 🟢 Verde (#2ecc71 → #27ae60)
4. 🟠 Laranja (#f39c12 → #e67e22)
5. 🟣 Roxo (#9b59b6 → #8e44ad)
6. 🔷 Turquesa (#1abc9c → #16a085)
7. ⚫ Cinza Escuro (#34495e → #2c3e50)
8. 🟤 Laranja Escuro (#e67e22 → #d35400)
9. ⚪ Cinza (#95a5a6 → #7f8c8d)
10. 🟦 Verde Água (#16a085 → #138d75)

---

## 📊 Dados Considerados

### Incluídos:
✅ Produtos ativos
✅ Produtos com fornecedor definido
✅ Produtos com preço de compra > 0
✅ Estoque atual do produto

### Excluídos:
❌ Produtos inativos
❌ Produtos sem fornecedor
❌ Produtos com fornecedor vazio

---

## 🔄 Atualização dos Dados

Os dados são atualizados automaticamente quando:
- Página é carregada
- Filtro de categoria é alterado
- Filtro de ano é alterado

**Tempo de resposta:** < 1 segundo (depende do volume de dados)

---

## 💡 Dicas de Uso

### Para Gestores:
- Use "Todas as Categorias" para visão macro
- Filtre por ano para análise de tendências
- Identifique fornecedores estratégicos

### Para Compradores:
- Filtre por categoria específica
- Compare gastos entre fornecedores
- Identifique oportunidades de negociação

### Para Análise Financeira:
- Acompanhe total gasto por período
- Identifique concentração de gastos
- Planeje orçamento por fornecedor

---

## 🚀 Melhorias Futuras (Sugestões)

1. **Exportar para Excel/PDF**
   - Botão para exportar ranking
   - Incluir gráficos no relatório

2. **Comparação de Períodos**
   - Comparar ano atual vs anterior
   - Mostrar variação percentual

3. **Drill-down**
   - Clicar no fornecedor para ver detalhes
   - Listar produtos do fornecedor

4. **Alertas**
   - Notificar quando gasto ultrapassar limite
   - Alertar sobre concentração excessiva

5. **Mais Filtros**
   - Filtro por marca
   - Filtro por faixa de valor
   - Filtro por status de estoque

---

## ✅ Testado e Funcionando

- ✅ Carregamento de categorias
- ✅ Carregamento de anos
- ✅ Filtro por categoria
- ✅ Filtro por ano
- ✅ Cálculo de gastos
- ✅ Renderização de barras
- ✅ Formatação de moeda
- ✅ Cores diferenciadas
- ✅ Responsivo
- ✅ Sem erros no console

---

**Implementado com sucesso! 🎉**
