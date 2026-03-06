@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        🚀 DEPLOY AUTOMÁTICO - SISTEMA DE ESTOQUE 🚀       ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Git não está instalado!
    echo.
    echo 📥 Baixe e instale o Git:
    echo    https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git detectado!
echo.

REM Perguntar informações do usuário
echo ═══════════════════════════════════════════════════════════
echo   CONFIGURAÇÃO DO GITHUB
echo ═══════════════════════════════════════════════════════════
echo.
set /p GITHUB_USER="Digite seu usuário do GitHub: "
set /p REPO_NAME="Digite o nome do repositório (ex: sistema-estoque): "
echo.

REM Confirmar
echo.
echo ═══════════════════════════════════════════════════════════
echo   CONFIRMAÇÃO
echo ═══════════════════════════════════════════════════════════
echo.
echo   Usuário GitHub: %GITHUB_USER%
echo   Repositório: %REPO_NAME%
echo   URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
set /p CONFIRMA="Está correto? (S/N): "
if /i not "%CONFIRMA%"=="S" (
    echo.
    echo ❌ Operação cancelada!
    pause
    exit /b 0
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   INICIANDO DEPLOY...
echo ═══════════════════════════════════════════════════════════
echo.

REM Passo 1: Inicializar Git
echo [1/6] 📦 Inicializando repositório Git...
git init
if errorlevel 1 (
    echo ❌ Erro ao inicializar Git
    pause
    exit /b 1
)
echo ✅ Repositório inicializado!
echo.

REM Passo 2: Adicionar arquivos
echo [2/6] 📝 Adicionando arquivos ao Git...
git add .
if errorlevel 1 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)
echo ✅ Arquivos adicionados!
echo.

REM Passo 3: Commit
echo [3/6] 💾 Criando commit inicial...
git commit -m "Deploy inicial do sistema de estoque"
if errorlevel 1 (
    echo ❌ Erro ao criar commit
    pause
    exit /b 1
)
echo ✅ Commit criado!
echo.

REM Passo 4: Renomear branch
echo [4/6] 🌿 Configurando branch main...
git branch -M main
if errorlevel 1 (
    echo ❌ Erro ao renomear branch
    pause
    exit /b 1
)
echo ✅ Branch configurada!
echo.

REM Passo 5: Adicionar remote
echo [5/6] 🔗 Conectando ao GitHub...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
if errorlevel 1 (
    echo ⚠️  Remote já existe, removendo e adicionando novamente...
    git remote remove origin
    git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
)
echo ✅ Conectado ao GitHub!
echo.

REM Passo 6: Push
echo [6/6] 🚀 Enviando código para o GitHub...
echo.
echo ⚠️  ATENÇÃO: Você precisará fazer login no GitHub!
echo.
pause
git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ Erro ao enviar código!
    echo.
    echo 💡 POSSÍVEIS SOLUÇÕES:
    echo    1. Certifique-se que o repositório existe no GitHub
    echo    2. Crie o repositório em: https://github.com/new
    echo    3. Use o nome: %REPO_NAME%
    echo    4. Deixe como PÚBLICO (necessário para Render gratuito)
    echo.
    pause
    exit /b 1
)

echo.
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ CÓDIGO ENVIADO COM SUCESSO! ✅            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo ═══════════════════════════════════════════════════════════
echo   PRÓXIMOS PASSOS - DEPLOY NO RENDER
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Acesse: https://render.com
echo.
echo 2. Faça login (pode usar conta do GitHub)
echo.
echo 3. Clique em "New +" → "Web Service"
echo.
echo 4. Conecte seu repositório:
echo    https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo 5. O Render detectará automaticamente as configurações
echo.
echo 6. Clique em "Create Web Service"
echo.
echo 7. Aguarde 2-5 minutos para o deploy completar
echo.
echo 8. Acesse sua URL e faça login:
echo    Usuário: admin
echo    Senha: admin123
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 📖 Para mais detalhes, leia: DEPLOY_RENDER.md
echo.
echo Deseja abrir o Render.com agora? (S/N)
set /p ABRIR_RENDER=""
if /i "%ABRIR_RENDER%"=="S" (
    start https://render.com
)
echo.
echo Deseja abrir seu repositório no GitHub? (S/N)
set /p ABRIR_GITHUB=""
if /i "%ABRIR_GITHUB%"=="S" (
    start https://github.com/%GITHUB_USER%/%REPO_NAME%
)
echo.
echo.
echo ✨ Processo concluído! Boa sorte com seu deploy! ✨
echo.
pause
