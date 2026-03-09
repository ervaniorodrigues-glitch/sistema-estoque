"""
WSGI configuration for PythonAnywhere
"""
import sys
import os

# Adicionar o diretório do projeto ao path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar variáveis de ambiente
os.environ.setdefault('SECRET_KEY', 'K8x#mP9$vL2@nQ5&wR7!jT4%yU6^bN3*cM1+dF0-eG8=')

# Importar a aplicação Flask
from app import app as application

if __name__ == '__main__':
    application.run()
