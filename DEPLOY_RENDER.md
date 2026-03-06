# 🚀 Guia de Deploy no Render

## Passo 1: Preparar o Código

✅ Todos os arquivos necessários já foram criados:
- `requirements.txt` - Dependências Python
- `render.yaml` - Configuração do Render
- `init_render.py` - Script de inicialização do banco
- `.gitignore` - Arquivos a ignorar no Git

## Passo 2: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome: `sistema-estoque` (ou outro nome)
4. Deixe como **Público** (necessário para plano gratuito do Render)
5. Clique em "Create repository"

## Passo 3: Enviar Código para o GitHub

Abra o terminal na pasta do projeto e execute:

```bash
git init
git add .
git commit -m "Deploy inicial do sistema de estoque"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/sistema-estoque.git
git push -u origin main
```

**Substitua `SEU_USUARIO` pelo seu usuário do GitHub!**

## Passo 4: Deploy no Render

1. Acesse [Render](https://render.com) e faça login (pode usar conta do GitHub)
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `sistema-estoque`
5. O Render detectará automaticamente o `render.yaml`
6. Clique em "Create Web Service"

## Passo 5: Aguardar Deploy

- O Render vai instalar as dependências
- Criar o banco de dados
- Iniciar o servidor
- Isso leva cerca de 2-5 minutos

## Passo 6: Acessar o Sistema

Após o deploy, você receberá uma URL como:
```
https://sistema-estoque-xxxx.onrender.com
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `admin123`

## ⚠️ Importante - Plano Gratuito

O plano gratuito do Render tem algumas limitações:

1. **Sleep após inatividade**: O serviço "dorme" após 15 minutos sem uso
   - Primeira requisição após sleep demora ~30 segundos
   
2. **750 horas/mês**: Suficiente para uso pessoal/testes

3. **Banco SQLite**: Os dados são perdidos a cada novo deploy
   - Para produção, considere usar PostgreSQL (também gratuito no Render)

## 🔄 Atualizar o Sistema

Quando fizer mudanças no código:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

O Render fará o deploy automaticamente!

## 📝 Dicas

- Mude a senha do admin após primeiro acesso
- Faça backup regular do banco de dados
- Para produção séria, considere o plano pago ($7/mês)

## 🆘 Problemas?

Se o deploy falhar:
1. Verifique os logs no painel do Render
2. Certifique-se que todos os arquivos foram enviados ao GitHub
3. Verifique se o `requirements.txt` está correto

## 🎉 Pronto!

Seu sistema de estoque está online e acessível de qualquer lugar!
