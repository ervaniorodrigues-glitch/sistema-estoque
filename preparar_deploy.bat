@echo off
echo ========================================
echo   PREPARANDO DEPLOY NO RENDER
echo ========================================
echo.

echo [1/3] Inicializando repositorio Git...
git init
if errorlevel 1 (
    echo ERRO: Git nao esta instalado!
    echo Baixe em: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo [2/3] Adicionando arquivos...
git add .

echo.
echo [3/3] Criando commit inicial...
git commit -m "Deploy inicial do sistema de estoque"

echo.
echo ========================================
echo   PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Crie um repositorio no GitHub
echo    https://github.com/new
echo.
echo 2. Execute os comandos abaixo:
echo.
echo    git branch -M main
echo    git remote add origin https://github.com/SEU_USUARIO/sistema-estoque.git
echo    git push -u origin main
echo.
echo 3. Acesse Render.com e conecte seu repositorio
echo.
echo Leia o arquivo DEPLOY_RENDER.md para mais detalhes!
echo.
pause
