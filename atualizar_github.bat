@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     📤 ATUALIZAR REPOSITÓRIO EXISTENTE 📤                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Usar o repositório que você já tem
set GITHUB_USER=ervanrodrigues-glitch
set REPO_NAME=Estoque

echo ✅ Repositório detectado:
echo    https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

REM Verificar se já existe .git
if exist ".git" (
    echo.
    echo ⚠️  Já existe um repositório Git aqui!
    echo.
    echo Deseja:
    echo   1 - Atualizar o repositório existente
    echo   2 - Reconfigurar do zero
    echo   3 - Cancelar
    echo.
    set /p OPCAO="Opção: "
    
    if "%OPCAO%"=="2" (
        echo.
        echo 🗑️  Removendo .git antigo...
        rmdir /s /q .git
        echo ✅ Removido!
        goto :init_git
    ) else if "%OPCAO%"=="3" (
        echo.
        echo ❌ Operação cancelada!
        pause
        exit /b 0
    )
    
    REM Opção 1 - Atualizar existente
    echo.
    echo ✅ Atualizando repositório existente...
    goto :add_files
)

:init_git
echo.
echo [1/5] 📦 Inicializando Git...
git init
git branch -M main

:add_files
echo.
echo [2/5] 📝 Adicionando arquivos...
git add .

echo.
echo [3/5] 💾 Criando commit...
git commit -m "Atualização: Sistema pronto para deploy no Render"

echo.
echo [4/5] 🔗 Configurando remote...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo [5/5] 🚀 Enviando para GitHub...
echo.
echo ⚠️  Você precisará autenticar!
echo.
pause
git push -u origin main -f

if errorlevel 1 (
    echo.
    echo ❌ Erro no push!
    echo.
    echo 💡 Tente:
    echo    git push -u origin main --force
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           ✅ CÓDIGO ATUALIZADO NO GITHUB! ✅              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🎯 PRÓXIMO PASSO - DEPLOY NO RENDER:
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
echo 5. O Render detectará o render.yaml automaticamente
echo.
echo 6. Clique em "Create Web Service"
echo.
echo 7. Aguarde 2-5 minutos para o deploy
echo.
echo 8. Acesse sua URL com:
echo    👤 Usuário: admin
echo    🔑 Senha: admin123
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Abrir Render.com agora? (S/N)
set /p ABRIR=""
if /i "%ABRIR%"=="S" start https://render.com
echo.
echo Abrir seu repositório no GitHub? (S/N)
set /p ABRIR_GH=""
if /i "%ABRIR_GH%"=="S" start https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo ✨ Pronto! Agora é só fazer o deploy no Render! ✨
echo.
pause
