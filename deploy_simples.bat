@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🚀 DEPLOY RÁPIDO - SISTEMA DE ESTOQUE 🚀              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar se já existe .git
if exist ".git" (
    echo ⚠️  Este diretório já é um repositório Git!
    echo.
    echo Escolha uma opção:
    echo   1 - Criar novo repositório (apaga o .git atual)
    echo   2 - Usar repositório existente
    echo   3 - Cancelar
    echo.
    set /p OPCAO="Opção: "
    
    if "%OPCAO%"=="1" (
        echo.
        echo 🗑️  Removendo .git antigo...
        rmdir /s /q .git
        echo ✅ Removido!
    ) else if "%OPCAO%"=="2" (
        echo.
        echo ✅ Usando repositório existente
        goto :usar_existente
    ) else (
        echo.
        echo ❌ Operação cancelada!
        pause
        exit /b 0
    )
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   INFORMAÇÕES DO REPOSITÓRIO
echo ═══════════════════════════════════════════════════════════
echo.
set /p GITHUB_USER="Seu usuário do GitHub: "
set /p REPO_NAME="Nome do repositório (ex: sistema-estoque): "
echo.

echo ✅ Configuração:
echo    URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause

echo.
echo [1/5] 📦 Inicializando Git...
git init
git branch -M main

:usar_existente
echo.
echo [2/5] 📝 Adicionando arquivos...
git add .

echo.
echo [3/5] 💾 Criando commit...
git commit -m "Deploy sistema de estoque para Render"

echo.
echo [4/5] 🔗 Configurando remote...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo [5/5] 🚀 Enviando para GitHub...
echo.
echo ⚠️  Você precisará autenticar no GitHub!
echo.
pause
git push -u origin main -f

if errorlevel 1 (
    echo.
    echo ❌ Erro no push!
    echo.
    echo 💡 SOLUÇÕES:
    echo    1. Crie o repositório: https://github.com/new
    echo    2. Nome: %REPO_NAME%
    echo    3. Deixe PÚBLICO (necessário para Render gratuito)
    echo    4. NÃO inicialize com README
    echo    5. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ CÓDIGO NO GITHUB! ✅                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🎯 AGORA NO RENDER:
echo.
echo 1. Acesse: https://render.com
echo 2. Login → New + → Web Service
echo 3. Conecte: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo 4. Clique "Create Web Service"
echo 5. Aguarde 2-5 minutos
echo.
echo 🔐 Login padrão:
echo    Usuário: admin
echo    Senha: admin123
echo.
echo Abrir Render.com? (S/N)
set /p ABRIR=""
if /i "%ABRIR%"=="S" start https://render.com
echo.
pause
