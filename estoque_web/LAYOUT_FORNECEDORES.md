# Layout Cadastro de Fornecedores - Baseado no Desktop

## Estrutura Geral
- **Listbox lateral esquerda** (280px de largura)
- **Formulário à direita** (resto do espaço)

---

## FORMULÁRIO - Disposição dos Campos

### LINHA 1
```
[Nome/Razão Social - 350px]                    [Código - 120px (readonly, rosa)]
```

### LINHA 2
```
[CNPJ - 200px]    [Telefone - 175px]
```

### LINHA 3
```
[Email - 250px]    [Oficina - 200px]
```

### LINHA 4
```
[Contato - 150px]    [CEP - 150px]
```

### LINHA 5
```
[Endereço - 380px]    [Cidade - 200px]    [UF - 35px]
```

---

## Tamanhos de Referência (CSS)
- **small**: 100px
- **medium**: 180px
- **Código**: 120px (readonly, fundo rosa #ffe6e6)
- **UF**: 35px (texto centralizado)
- **Telefone**: 175px
- **Email**: 250px
- **Oficina**: 200px
- **Contato**: 150px
- **CEP**: 150px
- **Endereço**: 380px
- **Cidade**: 200px

---

## Campos Obrigatórios
- Nome/Razão Social (*)

---

## Campos Readonly
- Código (fundo rosa #ffe6e6, tabindex="-1")

---

## Formatações Automáticas
- **CNPJ**: 00.000.000/0000-00
- **Telefone**: (00) 00000-0000
- **CEP**: 00000-000

---

## Busca CEP
- Ao sair do campo CEP (onblur), busca endereço via ViaCEP
- Preenche automaticamente: Endereço, Cidade, UF

---

## Botões (Toolbar)
- NOVO
- Limpar
- Salvar (aparece ao digitar)
- Alterar (aparece ao selecionar)
- Excluir (aparece ao selecionar)
- Ativar/Inativar (muda texto dinamicamente)
