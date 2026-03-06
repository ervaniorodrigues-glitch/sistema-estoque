#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Principal de Controle de Estoque
COM SISTEMA DE PROTEÇÃO DE DADOS INTEGRADO
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
from cadastro_produtos import CadastroProdutos
from backup_manager import BackupManager
from database_validator import DatabaseValidator
from data_protection import DataProtection
from cadastro_fornecedores_completo import CadastroFornecedores
from cadastro_clientes_completo import CadastroClientes
from emprestimos_novo import Emprestimos
from lancamentos_estoque import LancamentosEstoque
from cadastros_diversos_COMPLETO import CadastrosDiversos
from relatorios import Relatorios
from sistema_login import SistemaLogin
from cadastro_usuarios import CadastroUsuarios
from sistema_ativacao import SistemaAtivacao
from autorizacao_senhas import AutorizacaoSenhas
from configuracoes_sistema import ConfiguracoesSistema

class SistemaEstoque:
    def __init__(self):
        self.db_path = "estoque.db"
        self.root = tk.Tk()
        self.root.title("Sistema de Controle de Estoque")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 🛡️ SISTEMA DE PROTEÇÃO DE DADOS
        self.backup_manager = BackupManager(self.db_path)
        self.data_protection = DataProtection(self.db_path)
        self.database_validator = DatabaseValidator(self.db_path)
        
        # Instâncias dos módulos para sincronização
        self.cadastros_diversos = None
        self.cadastro_produtos = None
        self.cadastro_fornecedores = None
        
        # Sistema de login
        self.sistema_login = SistemaLogin(self.db_path)
        self.cadastro_usuarios_modulo = None
        self.autorizacao_senhas_modulo = None
        self.configuracoes_modulo = None
        self.usuario_logado = False  # Controle de acesso
        self.usuario_admin = False  # Controle se é administrador
        self.permissoes_usuario = {}  # Armazenar permissões do usuário logado
        
        # Timer de inatividade (60 minutos = 3600000 ms)
        self.timer_inatividade = None
        self.tempo_inatividade = 3600000  # 60 minutos em milissegundos
        
        # Sistema de ativação
        self.sistema_ativacao = SistemaAtivacao(self.db_path)
        
        # 🔧 VERIFICAR DEPENDÊNCIAS
        self.verificar_dependencias()
        
        # 🔧 VALIDAR E PROTEGER BANCO DE DADOS
        self.inicializar_protecao_dados()
        
        # �  CRIAR PASTA DE IMAGENS
        self.criar_pasta_imagens()
        
        # Sistema sempre inicia sem verificação automática de licença
        
        # Criar interface básica (sem acesso aos menus principais)
        self.criar_interface()
        
        # Centralizar janela após criar interface
        self.centralizar_janela()
        
        # Verificar banco de dados
        self.verificar_banco()
        
        # Configurar sistema de sincronização
        self.configurar_sincronizacao()
    
    def inicializar_sistema_apos_login(self):
        """Inicializar sistema após login bem-sucedido"""
        # Marcar como logado e recriar menu
        self.usuario_logado = True
        
        # Verificar se é administrador e carregar permissões
        usuario = self.sistema_login.usuario_logado
        if usuario:
            self.usuario_admin = usuario.get('autorizar_usuarios', False)
            self.permissoes_usuario = {
                'consulta': 1 if usuario.get('consulta', 0) else 0,
                'inclusao': 1 if usuario.get('inclusao', 0) else 0,
                'alteracao': 1 if usuario.get('alteracao', 0) else 0,
                'exclusao': 1 if usuario.get('exclusao', 0) else 0,
                'controle_especial_1': 1 if usuario.get('controle_especial_1', 0) else 0,  # Impressão
                'controle_especial_2': 1 if usuario.get('controle_especial_2', 0) else 0,  # Export Excel/PDF
                'autorizar_usuarios': 1 if usuario.get('autorizar_usuarios', 0) else 0
            }
            
            # Debug: Mostrar permissões carregadas
            print(f"DEBUG - Usuário: {usuario.get('nome')}")
            print(f"DEBUG - Admin: {self.usuario_admin}")
            print(f"DEBUG - Permissões: {self.permissoes_usuario}")
        
        self.criar_menu()  # Recriar menu com acesso completo
        
        # Iniciar timer de inatividade
        self.iniciar_timer_inatividade()
        
        # Configurar eventos de atividade
        self.configurar_eventos_atividade()
        
        # Atualizar status com usuário logado
        if usuario:
            tipo = "Administrador" if self.usuario_admin else "Usuário"
            self.status_bar.config(text=f"Usuário logado: {usuario['nome']} ({tipo})")
        
        # Se for admin, verificar solicitações de senha pendentes
        if self.usuario_admin:
            self.verificar_solicitacoes_senha_pendentes()
        
    def centralizar_janela(self):
        """Centralizar janela na tela"""
        # Definir tamanho da janela
        width = 800
        height = 600
        
        # Obter dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posição central
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Aplicar geometria
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Forçar atualização
        self.root.update_idletasks()
    
    def criar_pasta_imagens(self):
        """Criar pasta Imagens para armazenar fotos dos produtos"""
        try:
            pasta_imagens = "Imagens"
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)
                print(f"📁 Pasta '{pasta_imagens}' criada com sucesso!")
            else:
                print(f"📁 Pasta '{pasta_imagens}' já existe")
        except Exception as e:
            print(f"❌ Erro ao criar pasta Imagens: {e}")
    
    def criar_interface(self):
        """Criar interface principal do sistema"""
        
        # Título principal (altura reduzida)
        titulo_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        titulo_frame.pack(fill=tk.X, padx=10, pady=10)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="Bem-vindo ao Sistema de Controle de Estoque", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(expand=True)
        
        # Criar menu bar
        self.criar_menu()
        
        # Frame principal com imagem de fundo
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tentar carregar e exibir imagem de fundo
        try:
            from PIL import Image, ImageTk
            import os
            
            # Caminho da imagem
            caminho_imagem = os.path.join("Imagens", "Imagem-Fundo.jpg")
            
            if os.path.exists(caminho_imagem):
                # Carregar e redimensionar imagem
                imagem_original = Image.open(caminho_imagem)
                
                # Redimensionar para caber na área disponível (imagem maior)
                largura_max = 600
                altura_max = 450
                imagem_original.thumbnail((largura_max, altura_max), Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                self.imagem_fundo = ImageTk.PhotoImage(imagem_original)
                
                # Mensagem bem no topo (logo abaixo do cabeçalho)
                mensagem_frame = tk.Frame(main_frame, bg='#f8f9fa')
                mensagem_frame.place(relx=0.5, rely=0.1, anchor='center')
                
                tk.Label(mensagem_frame, text="Utilize o menu acima para acessar as funcionalidades do sistema", 
                        font=('Arial', 12), fg='#7f8c8d', bg='#f8f9fa').pack()
                
                # Frame para a imagem (centralizado verticalmente)
                imagem_frame = tk.Frame(main_frame, bg='#f8f9fa')
                imagem_frame.place(relx=0.5, rely=0.45, anchor='center')
                
                # Label com imagem de fundo
                imagem_label = tk.Label(imagem_frame, image=self.imagem_fundo, bg='#f8f9fa')
                imagem_label.pack()
                
            else:
                # Fallback caso a imagem não exista
                self.criar_interface_sem_imagem(main_frame)
                
        except ImportError:
            # Fallback caso PIL não esteja disponível
            print("⚠️ PIL não disponível - interface sem imagem de fundo")
            self.criar_interface_sem_imagem(main_frame)
        except Exception as e:
            # Fallback para qualquer outro erro
            print(f"⚠️ Erro ao carregar imagem: {e}")
            self.criar_interface_sem_imagem(main_frame)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Sistema pronto para uso", 
                                  relief=tk.SUNKEN, anchor=tk.W, bg='#ecf0f1')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def criar_interface_sem_imagem(self, main_frame):
        """Criar interface sem imagem de fundo (fallback)"""
        # Mensagem bem no topo (logo abaixo do cabeçalho)
        mensagem_frame = tk.Frame(main_frame, bg='#f8f9fa')
        mensagem_frame.place(relx=0.5, rely=0.1, anchor='center')
        
        tk.Label(mensagem_frame, text="Utilize o menu acima para acessar as funcionalidades do sistema", 
                font=('Arial', 12), fg='#7f8c8d', bg='#f8f9fa').pack()
    
    def criar_menu(self):
        """Criar menu bar com categorias organizadas e controle de acesso"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # ===== MENUS PRINCIPAIS (só aparecem se logado E com permissões além de consulta) =====
        if self.usuario_logado and (self.usuario_admin or 
                                   self.verificar_permissao('inclusao') or 
                                   self.verificar_permissao('alteracao') or 
                                   self.verificar_permissao('exclusao')):
            # Menu Cadastros - Reorganizado
            menu_cadastros = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="📋 Cadastros", menu=menu_cadastros)
            menu_cadastros.add_command(label="📦 Produtos", command=self.abrir_produtos)
            menu_cadastros.add_command(label="👤 Funcionários", command=self.abrir_funcionarios)
            menu_cadastros.add_separator()
            menu_cadastros.add_command(label="🏢 Fornecedores", command=self.abrir_fornecedores)
            menu_cadastros.add_command(label="👥 Clientes", command=self.abrir_clientes)
            menu_cadastros.add_separator()
            menu_cadastros.add_command(label="⚙️ Cadastros Diversos", command=self.abrir_cadastros_diversos)
            
            # Menu Estoque - Simplificado (direto)
            menubar.add_command(label="📦 Estoque", command=self.abrir_entrada_saida)
            
            # Movimentações - Direto na barra principal
            menubar.add_command(label="📋 Movimentações", command=self.relatorio_movimentacoes)
        
        # ===== MENU ESPECIAL PARA USUÁRIOS APENAS CONSULTA =====
        elif self.usuario_logado and self.verificar_permissao('consulta'):
            # Menu Consultas (apenas visualização)
            menu_consultas = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="👁️ Consultas", menu=menu_consultas)
            menu_consultas.add_command(label="📦 Consultar Produtos", command=self.consultar_produtos_readonly)
            menu_consultas.add_command(label="🏢 Consultar Fornecedores", command=self.consultar_fornecedores_readonly)
            menu_consultas.add_command(label="👥 Consultar Clientes", command=self.consultar_clientes_readonly)
            menu_consultas.add_command(label="👤 Consultar Funcionários", command=self.consultar_funcionarios_readonly)
            menu_consultas.add_separator()
            menu_consultas.add_command(label="📊 Consultar Estoque", command=self.consultar_estoque_readonly)
            menu_consultas.add_command(label="🔄 Consultar Empréstimos", command=self.consultar_emprestimos_readonly)
            menu_consultas.add_command(label="📂 Consultar Categoria", command=self.consultar_categoria_readonly)
            menu_consultas.add_separator()
            menu_consultas.add_command(label="📋 Consultar Movimentações", command=self.consultar_movimentacoes_readonly)
        
        # Menu Sistema - APENAS PARA ADMINISTRADORES
        if self.usuario_admin:
                menu_sistema = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="⚙️ Sistema", menu=menu_sistema)
            
                # Submenu de Backup e Proteção
                menu_backup = tk.Menu(menu_sistema, tearoff=0)
                menu_sistema.add_cascade(label="🛡️ Backup e Proteção", menu=menu_backup)
                menu_backup.add_command(label="💾 Backup Manual", command=self.fazer_backup_manual)
                menu_backup.add_command(label="🔄 Restaurar Backup", command=self.restaurar_backup)
                menu_backup.add_command(label="📊 Status do Sistema", command=self.mostrar_status_protecao)
                menu_backup.add_command(label="🔍 Validar Banco", command=self.validar_banco_manual)
                menu_backup.add_command(label="📋 Listar Backups", command=self.listar_backups)
                
                menu_sistema.add_separator()
                
                # Menu Configurações
                menu_sistema.add_command(label="⚙️ Configurações", command=self.abrir_configuracoes)
                
                menu_sistema.add_separator()
                
                # Gerenciamento de Usuários (apenas para admin)
                menu_sistema.add_command(label="👤 Cadastro de Usuários", command=self.cadastro_usuarios)
                menu_sistema.add_command(label="🔑 Autorização de Senhas", command=self.autorizacao_senhas)
                
                menu_sistema.add_separator()
                
                # Submenu de Limpeza
                menu_limpeza = tk.Menu(menu_sistema, tearoff=0)
                menu_sistema.add_cascade(label="🧹 Limpeza de Dados", menu=menu_limpeza)
                menu_limpeza.add_command(label="🗑️ Zerar Tudo", command=self.zerar_tudo_completo)
                menu_limpeza.add_separator()
                menu_limpeza.add_command(label="📦 Zerar Estoque", command=self.zerar_apenas_estoque)
                menu_limpeza.add_command(label="📋 Limpar Histórico", command=self.limpar_historico)
                menu_limpeza.add_command(label="🔄 Limpar Movimentações", command=self.limpar_movimentacoes)
                menu_limpeza.add_separator()
                
                # Submenu de Limpeza de Cadastros
                menu_cadastros_limpeza = tk.Menu(menu_limpeza, tearoff=0)
                menu_limpeza.add_cascade(label="👥 Limpar Cadastros", menu=menu_cadastros_limpeza)
                menu_cadastros_limpeza.add_command(label="📦 Zerar Cadastro de Produtos", command=self.limpar_produtos)
                menu_cadastros_limpeza.add_command(label="👤 Zerar Cadastro de Funcionários", command=self.limpar_funcionarios)
                menu_cadastros_limpeza.add_command(label="🏢 Zerar Cadastro de Fornecedores", command=self.limpar_fornecedores)
                menu_cadastros_limpeza.add_command(label="👥 Zerar Cadastro de Clientes", command=self.limpar_clientes)
                
                # Submenu de Limpeza de Empréstimos
                menu_emprestimos_limpeza = tk.Menu(menu_limpeza, tearoff=0)
                menu_limpeza.add_cascade(label="🔄 Limpar Empréstimos", menu=menu_emprestimos_limpeza)
                menu_emprestimos_limpeza.add_command(label="📋 Zerar Lançamentos de Empréstimo", command=self.limpar_emprestimos)
                menu_emprestimos_limpeza.add_command(label="📊 Zerar Histórico de Empréstimo", command=self.limpar_historico_emprestimos)
                
                menu_sistema.add_separator()
                menu_sistema.add_command(label="🚪 Sair", command=self.sair_sistema)
        
        # ===== MENU USUÁRIOS E LOGIN (SEMPRE VISÍVEL - FORA DE TODAS AS CONDIÇÕES) =====
        menu_usuarios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👤 Usuários e Login", menu=menu_usuarios)
        
        # Efetuar Login (sempre visível)
        menu_usuarios.add_command(label="🔐 Efetuar Login", command=self.efetuar_login)
        
        # Logout (apenas se logado)
        if self.usuario_logado:
            menu_usuarios.add_separator()
            menu_usuarios.add_command(label="🚪 Logout", command=self.fazer_logout)
    
    def verificar_permissao(self, tipo_permissao):
        """Verificar se o usuário tem permissão para determinada ação"""
        if self.usuario_admin:
            return True  # Administrador tem todas as permissões
        
        if not self.usuario_logado:
            return False  # Usuário não logado não tem permissão
        
        tem_permissao = self.permissoes_usuario.get(tipo_permissao, 0) == 1
        print(f"DEBUG - Verificando {tipo_permissao}: {tem_permissao} (valor: {self.permissoes_usuario.get(tipo_permissao, 0)})")
        return tem_permissao
    
    def bloquear_acao_sem_permissao(self, tipo_permissao, acao="esta ação"):
        """Bloquear ação se usuário não tiver permissão"""
        if not self.verificar_permissao(tipo_permissao):
            messagebox.showwarning("Acesso Negado", 
                                 f"Você não tem permissão para {acao}.\n\n" +
                                 f"Permissão necessária: {tipo_permissao.upper()}\n" +
                                 f"Entre em contato com o administrador.")
            return True
        return False
    
    def verificar_banco(self):
        """Verificar se banco de dados existe e está funcionando"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar tabelas principais
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('produtos', 'fornecedores', 'clientes', 'funcionarios')
            """)
            
            tabelas = cursor.fetchall()
            tabelas_encontradas = [t[0] for t in tabelas]
            
            # Se não tiver todas as tabelas, criar automaticamente
            if len(tabelas_encontradas) < 4:
                print("⚠️ Tabelas faltando no banco de dados. Criando automaticamente...")
                self.criar_tabelas_automaticamente()
                self.status_bar.config(text="✅ Banco de dados configurado automaticamente - Sistema pronto")
            else:
                self.status_bar.config(text="✅ Banco de dados OK - Sistema pronto")
            
            conn.close()
                
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
            self.status_bar.config(text=f"❌ Erro no banco: {e}")
    
    def criar_tabelas_automaticamente(self):
        """Criar tabelas automaticamente se não existirem"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            print("🔧 Criando tabelas automaticamente...")
            
            # Tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    codigo INTEGER PRIMARY KEY,
                    descricao TEXT NOT NULL,
                    unidade TEXT,
                    marca TEXT,
                    categoria TEXT,
                    preco_compra REAL DEFAULT 0,
                    preco REAL DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 0,
                    estoque_maximo INTEGER DEFAULT 0,
                    estoque_atual INTEGER DEFAULT 0,
                    foto TEXT,
                    fornecedor TEXT,
                    ativo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de fornecedores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fornecedores (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    uf TEXT,
                    cep TEXT,
                    cnpj TEXT,
                    contato TEXT,
                    ativo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT,
                    telefone TEXT,
                    celular TEXT,
                    fax TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    uf TEXT,
                    cep TEXT,
                    anotacoes TEXT,
                    ativo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de funcionários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cargo TEXT,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    uf TEXT,
                    cpf TEXT,
                    data_admissao TEXT,
                    salario REAL,
                    ativo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de empréstimos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT,
                    data TEXT,
                    funcionario TEXT,
                    cargo TEXT,
                    cod_produto TEXT,
                    descricao_item TEXT,
                    observacoes TEXT,
                    status TEXT DEFAULT 'EMPRESTADO',
                    data_devolucao TEXT
                )
            ''')
            
            # Tabela de log de movimentações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS log_movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_produto TEXT,
                    tipo_movimento TEXT,
                    quantidade_movimento INTEGER,
                    origem TEXT,
                    data_movimento DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabelas auxiliares
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS unidades_div (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS marcas_div (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias_div (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operacoes_div (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')
            
            # Inserir dados básicos
            unidades = ['UN', 'KG', 'LT', 'MT', 'CX', 'PC', 'DZ', 'ML', 'GR']
            for unidade in unidades:
                cursor.execute("INSERT OR IGNORE INTO unidades_div (nome) VALUES (?)", (unidade,))
            
            marcas = ['Genérica', 'Nacional', 'Importada', 'Própria']
            for marca in marcas:
                cursor.execute("INSERT OR IGNORE INTO marcas_div (nome) VALUES (?)", (marca,))
            
            categorias = ['Alimentação', 'Limpeza', 'Escritório', 'Eletrônicos', 'Diversos']
            for categoria in categorias:
                cursor.execute("INSERT OR IGNORE INTO categorias_div (nome) VALUES (?)", (categoria,))
            
            operacoes = ['Compra de Mercadorias', 'Venda de Mercadorias', 'Transferência', 'Ajuste de Estoque']
            for operacao in operacoes:
                cursor.execute("INSERT OR IGNORE INTO operacoes_div (nome) VALUES (?)", (operacao,))
            
            # Migração: Adicionar campos faltantes na tabela clientes
            self.migrate_clientes_table(cursor)
            
            conn.commit()
            conn.close()
            
            print("✅ Tabelas criadas automaticamente com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas automaticamente: {e}")
    
    def migrate_clientes_table(self, cursor):
        """Migrar tabela clientes adicionando campos faltantes"""
        try:
            # Verificar quais colunas existem
            cursor.execute("PRAGMA table_info(clientes)")
            colunas_existentes = [row[1] for row in cursor.fetchall()]
            
            # Adicionar celular se não existir
            if 'celular' not in colunas_existentes:
                cursor.execute("ALTER TABLE clientes ADD COLUMN celular TEXT")
                print("✅ Campo 'celular' adicionado à tabela clientes")
            
            # Adicionar fax se não existir
            if 'fax' not in colunas_existentes:
                cursor.execute("ALTER TABLE clientes ADD COLUMN fax TEXT")
                print("✅ Campo 'fax' adicionado à tabela clientes")
            
            # Adicionar anotacoes se não existir
            if 'anotacoes' not in colunas_existentes:
                cursor.execute("ALTER TABLE clientes ADD COLUMN anotacoes TEXT")
                print("✅ Campo 'anotacoes' adicionado à tabela clientes")
                
        except Exception as e:
            print(f"⚠️ Erro na migração da tabela clientes: {e}")
    
    def inicializar_protecao_dados(self):
        """Inicializar sistema de proteção de dados"""
        try:
            print("🛡️ INICIALIZANDO SISTEMA DE PROTEÇÃO DE DADOS...")
            
            # 1. Validar estrutura do banco (com tratamento de erro)
            try:
                self.database_validator.validar_estrutura_completa()
            except Exception as e:
                print(f"⚠️ Erro na validação do banco: {e}")
                print("⚠️ Continuando inicialização...")
            
            # 2. Corrigir produtos inativos (com tratamento de erro)
            try:
                self.database_validator.corrigir_produtos_inativos()
            except Exception as e:
                print(f"⚠️ Erro na correção de produtos: {e}")
                print("⚠️ Continuando inicialização...")
            
            # 3. Criar backup inicial (com tratamento de erro)
            try:
                backup_inicial = self.backup_manager.criar_backup_automatico()
                if backup_inicial:
                    print(f"✅ Backup inicial criado: {os.path.basename(backup_inicial)}")
                else:
                    print("⚠️ Backup inicial não foi criado")
            except Exception as e:
                print(f"⚠️ Erro ao criar backup inicial: {e}")
                print("⚠️ Sistema continuará sem backup inicial")
            
            # 4. Verificar integridade (com tratamento de erro)
            try:
                if self.data_protection.verificar_integridade_periodica():
                    print("✅ Sistema de proteção inicializado com sucesso!")
                else:
                    print("⚠️ Problemas detectados - sistema continuará funcionando")
            except Exception as e:
                print(f"⚠️ Erro na verificação de integridade: {e}")
                print("⚠️ Sistema continuará funcionando")
                
            print("✅ Inicialização da proteção concluída!")
                
        except Exception as e:
            print(f"⚠️ Erro geral na inicialização da proteção: {e}")
            print("⚠️ Sistema continuará funcionando sem proteção completa")
    
    def verificar_dependencias(self):
        """Verificar se todas as dependências estão instaladas"""
        try:
            print("🔍 Verificando dependências...")
            
            # Lista de dependências críticas
            dependencias = {
                'PIL': 'Pillow',
                'pandas': 'pandas',
                'openpyxl': 'openpyxl'
            }
            
            dependencias_faltando = []
            
            for modulo, pacote in dependencias.items():
                try:
                    if modulo == 'PIL':
                        from PIL import Image, ImageTk
                    elif modulo == 'pandas':
                        import pandas
                    elif modulo == 'openpyxl':
                        import openpyxl
                    print(f"✅ {pacote}: OK")
                except ImportError:
                    print(f"⚠️ {pacote}: FALTANDO")
                    dependencias_faltando.append(pacote)
            
            if dependencias_faltando:
                print(f"⚠️ Dependências faltando: {', '.join(dependencias_faltando)}")
                print("⚠️ Algumas funcionalidades podem não funcionar corretamente")
                print("💡 Execute: pip install " + " ".join(dependencias_faltando))
            else:
                print("✅ Todas as dependências estão instaladas!")
                
        except Exception as e:
            print(f"⚠️ Erro ao verificar dependências: {e}")
    
    def configurar_sincronizacao(self):
        """Configurar sistema de sincronização entre módulos"""
        pass  # Será configurado quando os módulos forem abertos
    
    def callback_sincronizacao(self, tipo_alteracao, secao, item_antigo=None, item_novo=None):
        """Callback para sincronizar alterações entre módulos"""
        try:
            print(f"📢 Callback chamado: tipo={tipo_alteracao}, secao={secao}")
            print(f"   cadastro_produtos={self.cadastro_produtos}, cadastro_fornecedores={self.cadastro_fornecedores}")
            
            # Log da sincronização
            nomes_secoes = {1: "Unidades", 2: "Marcas", 3: "Categorias", 4: "Operações"}
            secao_nome = nomes_secoes.get(secao, f"Seção {secao}")
            
            if tipo_alteracao == 'inserir':
                print(f"🔄 Sincronização: {item_novo} adicionado em {secao_nome}")
            elif tipo_alteracao == 'alterar':
                print(f"🔄 Sincronização: {item_antigo} alterado para {item_novo} em {secao_nome}")
            elif tipo_alteracao == 'excluir':
                print(f"🔄 Sincronização: {item_antigo} removido de {secao_nome}")
            elif tipo_alteracao == 'limpar_geral':
                print(f"🔄 Sincronização: Limpeza geral realizada em {secao_nome}")
            
            # Atualizar cadastro de produtos se estiver aberto
            if self.cadastro_produtos:
                try:
                    if hasattr(self.cadastro_produtos, 'window') and self.cadastro_produtos.window and self.cadastro_produtos.window.winfo_exists():
                        if hasattr(self.cadastro_produtos, 'atualizar_comboboxes'):
                            print(f"✅ Atualizando comboboxes do Cadastro de Produtos")
                            self.cadastro_produtos.atualizar_comboboxes()
                        else:
                            print(f"⚠️ Cadastro de Produtos não tem método atualizar_comboboxes")
                    else:
                        print(f"⚠️ Janela do Cadastro de Produtos não existe ou não está visível")
                except Exception as e:
                    print(f"⚠️ Erro ao atualizar cadastro de produtos: {e}")
            else:
                print(f"⚠️ Cadastro de Produtos não está instanciado")
            
            # Atualizar cadastro de fornecedores se estiver aberto
            if self.cadastro_fornecedores:
                try:
                    if hasattr(self.cadastro_fornecedores, 'window') and self.cadastro_fornecedores.window and self.cadastro_fornecedores.window.winfo_exists():
                        if hasattr(self.cadastro_fornecedores, 'atualizar_comboboxes_fornecedores'):
                            print(f"✅ Atualizando comboboxes do Cadastro de Fornecedores")
                            self.cadastro_fornecedores.atualizar_comboboxes_fornecedores()
                except Exception as e:
                    print(f"⚠️ Erro ao atualizar cadastro de fornecedores: {e}")
                
        except Exception as e:
            print(f"Erro na sincronização: {e}")
    
    # Métodos para abrir módulos
    def abrir_produtos(self):
        """Abrir cadastro de produtos"""
        if self.bloquear_acao_sem_permissao('consulta', 'acessar o cadastro de produtos'):
            return
            
        try:
            self.root.withdraw()  # Ocultar janela principal
            self.cadastro_produtos = CadastroProdutos(self.root, self.db_path, self.callback_sincronizacao)
            
            # Passar permissões para o módulo
            if hasattr(self.cadastro_produtos, 'permissoes'):
                self.cadastro_produtos.permissoes = self.permissoes_usuario
            if hasattr(self.cadastro_produtos, 'usuario_admin'):
                self.cadastro_produtos.usuario_admin = self.usuario_admin
            
            self.cadastro_produtos.abrir()
            
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(self.cadastro_produtos, 'window') and self.cadastro_produtos.window:
                self.cadastro_produtos.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(self.cadastro_produtos.window))
            self.status_bar.config(text="Cadastro de Produtos aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            print(f"Erro detalhado ao abrir produtos: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir produtos: {e}")
    
    def abrir_fornecedores(self):
        """Abrir cadastro de fornecedores"""
        if self.bloquear_acao_sem_permissao('consulta', 'acessar o cadastro de fornecedores'):
            return
            
        try:
            self.root.withdraw()  # Ocultar janela principal
            self.cadastro_fornecedores = CadastroFornecedores(self.root, self.db_path, self.callback_sincronizacao)
            
            # Passar permissões para o módulo
            if hasattr(self.cadastro_fornecedores, 'permissoes'):
                self.cadastro_fornecedores.permissoes = self.permissoes_usuario
            if hasattr(self.cadastro_fornecedores, 'usuario_admin'):
                self.cadastro_fornecedores.usuario_admin = self.usuario_admin
            
            self.cadastro_fornecedores.abrir()
            
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(self.cadastro_fornecedores, 'window') and self.cadastro_fornecedores.window:
                self.cadastro_fornecedores.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(self.cadastro_fornecedores.window))
            self.status_bar.config(text="Cadastro de Fornecedores aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            print(f"Erro detalhado ao abrir fornecedores: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir fornecedores: {e}")
    
    def abrir_clientes(self):
        """Abrir cadastro de clientes"""
        if self.bloquear_acao_sem_permissao('consulta', 'acessar o cadastro de clientes'):
            return
            
        try:
            self.root.withdraw()  # Ocultar janela principal
            clientes = CadastroClientes(self.root, self.db_path)
            
            # Passar permissões para o módulo
            if hasattr(clientes, 'permissoes'):
                clientes.permissoes = self.permissoes_usuario
            if hasattr(clientes, 'usuario_admin'):
                clientes.usuario_admin = self.usuario_admin
            
            clientes.abrir()
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(clientes, 'window') and clientes.window:
                clientes.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(clientes.window))
            self.status_bar.config(text="Cadastro de Clientes aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            print(f"Erro detalhado ao abrir clientes: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir clientes: {e}")
    
    def abrir_funcionarios(self):
        """Abrir cadastro de funcionários"""
        try:
            self.root.withdraw()  # Ocultar janela principal
            from cadastro_funcionarios_completo import CadastroFuncionarios
            funcionarios = CadastroFuncionarios(self.root, self.db_path)
            funcionarios.abrir()
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(funcionarios, 'window') and funcionarios.window:
                funcionarios.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(funcionarios.window))
            self.status_bar.config(text="Cadastro de Funcionários aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            messagebox.showerror("Erro", f"Erro ao abrir funcionários: {e}")
    
    def fechar_modulo(self, janela_modulo):
        """Fechar módulo e mostrar janela principal"""
        try:
            janela_modulo.destroy()
        except:
            pass
        self.root.deiconify()  # Mostrar janela principal
    
    def abrir_cadastros_diversos(self):
        """Abrir cadastros diversos"""
        try:
            self.cadastros_diversos = CadastrosDiversos(self.root, self.db_path, self.callback_sincronizacao)
            self.cadastros_diversos.abrir()
            
            self.status_bar.config(text="Cadastros Diversos aberto")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastros diversos: {e}")
    
    def abrir_emprestimos(self):
        """Abrir sistema de empréstimos"""
        try:
            self.root.withdraw()  # Ocultar janela principal
            emprestimos = Emprestimos(self.root, self.db_path, self.callback_sincronizacao)
            emprestimos.abrir()
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(emprestimos, 'window') and emprestimos.window:
                emprestimos.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(emprestimos.window))
            self.status_bar.config(text="Sistema de Empréstimos aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            messagebox.showerror("Erro", f"Erro ao abrir empréstimos: {e}")
    
    def abrir_entrada_saida(self):
        """Abrir sistema de entrada e saída de estoque"""
        try:
            # NÃO ocultar a janela principal - deixar visível
            lancamentos_estoque = LancamentosEstoque(self.root, self.db_path, self.callback_sincronizacao, self.sistema_login)
            lancamentos_estoque.abrir()
            self.status_bar.config(text="Sistema de Entrada/Saída aberto")
        except Exception as e:
            print(f"Erro ao abrir entrada/saída: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir sistema de entrada/saída: {e}")
    
    def abrir_categoria(self):
        """Abrir sistema de categoria"""
        try:
            self.root.withdraw()  # Ocultar janela principal
            from categoria import Categoria
            categoria = Categoria(self.root, self.db_path)
            categoria.abrir()
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(categoria, 'window') and categoria.window:
                categoria.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(categoria.window))
            self.status_bar.config(text="Sistema de Categoria aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            messagebox.showerror("Erro", f"Erro ao abrir categoria: {e}")
    
    def abrir_venda(self):
        """Abrir sistema de venda"""
        try:
            self.root.withdraw()  # Ocultar janela principal
            from venda import Venda
            venda = Venda(self.root, self.db_path, self.callback_sincronizacao)
            venda.abrir()
            # Configurar callback para mostrar janela principal quando fechar
            if hasattr(venda, 'window') and venda.window:
                venda.window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_modulo(venda.window))
            self.status_bar.config(text="Sistema de Venda aberto")
        except Exception as e:
            self.root.deiconify()  # Mostrar janela principal em caso de erro
            messagebox.showerror("Erro", f"Erro ao abrir venda: {e}")
    
    def consultar_estoque(self):
        """Consultar estoque atual"""
        try:
            relatorios = Relatorios(self.root, self.db_path)
            
            # Passar permissões para o módulo de relatórios
            relatorios.permissoes = self.permissoes_usuario
            relatorios.usuario_admin = self.usuario_admin
            
            relatorios.consulta_rapida_estoque()
            self.status_bar.config(text="Consulta de estoque realizada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {e}")
    
    def relatorio_posicao(self):
        """Relatório de posição do estoque"""
        try:
            relatorios = Relatorios(self.root, self.db_path)
            relatorios.relatorio_posicao_estoque()
            self.status_bar.config(text="Relatório de posição gerado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no relatório: {e}")
    
    def relatorio_movimentacoes(self):
        """Relatório de movimentações"""
        try:
            relatorios = Relatorios(self.root, self.db_path)
            
            # Passar permissões para o módulo de relatórios
            relatorios.permissoes = self.permissoes_usuario
            relatorios.usuario_admin = self.usuario_admin
            
            relatorios.relatorio_movimentacoes()
            self.status_bar.config(text="Relatório de movimentações gerado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no relatório: {e}")
    
    def exportar_excel(self):
        """Exportar dados para Excel"""
        try:
            relatorios = Relatorios(self.root, self.db_path)
            relatorios.exportar_excel()
            self.status_bar.config(text="Dados exportados para Excel")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na exportação: {e}")
    
    def fazer_backup_manual(self):
        """Fazer backup manual do banco"""
        try:
            arquivo = self.backup_manager.criar_backup_manual()
            if arquivo:
                self.status_bar.config(text="Backup manual realizado com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no backup: {e}")
    
    def restaurar_backup(self):
        """Restaurar backup"""
        try:
            if self.backup_manager.restaurar_backup():
                self.status_bar.config(text="Backup restaurado com sucesso")
                # Reinicializar proteção após restauração
                self.inicializar_protecao_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na restauração: {e}")
    
    def mostrar_status_protecao(self):
        """Mostrar status do sistema de proteção"""
        try:
            status = self.backup_manager.status_sistema()
            
            status_window = tk.Toplevel(self.root)
            status_window.title("Status do Sistema de Proteção")
            status_window.geometry("500x400")
            status_window.configure(bg='#f8f9fa')
            status_window.transient(self.root)
            status_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(status_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="🛡️ Status do Sistema de Proteção", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Informações do sistema
            info_frame = tk.Frame(main_frame, bg='#fff', relief=tk.SUNKEN, bd=2)
            info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Dados do sistema
            dados_sistema = [
                ("📦 Produtos", status.get('produtos', 'N/A')),
                ("👥 Clientes", status.get('clientes', 'N/A')),
                ("🏢 Fornecedores", status.get('fornecedores', 'N/A')),
                ("👤 Funcionários", status.get('funcionarios', 'N/A')),
                ("🔄 Empréstimos", status.get('emprestimos', 'N/A')),
                ("💾 Total de Backups", status.get('total_backups', 'N/A')),
                ("🕒 Último Backup", status.get('ultimo_backup', 'N/A'))
            ]
            
            for i, (label, valor) in enumerate(dados_sistema):
                row_frame = tk.Frame(info_frame, bg='#fff')
                row_frame.pack(fill=tk.X, padx=10, pady=2)
                
                tk.Label(row_frame, text=label, font=('Arial', 10), 
                        bg='#fff', anchor='w').pack(side=tk.LEFT)
                tk.Label(row_frame, text=str(valor), font=('Arial', 10, 'bold'), 
                        bg='#fff', fg='#2c3e50', anchor='e').pack(side=tk.RIGHT)
            
            # Botão fechar
            tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=status_window.destroy).pack(pady=20)
                     
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar status: {e}")
    
    def validar_banco_manual(self):
        """Validar banco de dados manualmente"""
        try:
            # Mostrar janela de progresso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Validando Banco de Dados")
            progress_window.geometry("400x150")
            progress_window.configure(bg='#f8f9fa')
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            tk.Label(progress_window, text="🔍 Validando estrutura do banco...", 
                    font=('Arial', 12), bg='#f8f9fa').pack(pady=30)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=50, fill=tk.X)
            progress_bar.start()
            
            # Atualizar interface
            progress_window.update()
            
            # Executar validação
            self.database_validator.validar_estrutura_completa()
            
            # Fechar janela de progresso
            progress_bar.stop()
            progress_window.destroy()
            
            messagebox.showinfo("Validação Concluída", 
                              "Validação do banco de dados concluída!\n\n"
                              "Verifique o console para detalhes.")
            self.status_bar.config(text="Validação do banco concluída")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na validação: {e}")
    
    def listar_backups(self):
        """Listar todos os backups disponíveis"""
        try:
            backups = self.backup_manager.listar_backups()
            
            backup_window = tk.Toplevel(self.root)
            backup_window.title("Lista de Backups")
            backup_window.geometry("700x500")
            backup_window.configure(bg='#f8f9fa')
            backup_window.transient(self.root)
            backup_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(backup_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="💾 Lista de Backups Disponíveis", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de backups
            columns = ('Nome', 'Tipo', 'Data', 'Tamanho')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
            
            # Configurar colunas
            tree.heading('Nome', text='Nome do Arquivo')
            tree.heading('Tipo', text='Tipo')
            tree.heading('Data', text='Data/Hora')
            tree.heading('Tamanho', text='Tamanho')
            
            tree.column('Nome', width=250)
            tree.column('Tipo', width=100)
            tree.column('Data', width=150)
            tree.column('Tamanho', width=100)
            
            # Adicionar backups à tabela
            for backup in backups:
                tamanho_mb = backup['tamanho'] / (1024 * 1024)
                tree.insert('', tk.END, values=(
                    backup['nome'],
                    backup['tipo'],
                    backup['data'],
                    f"{tamanho_mb:.2f} MB"
                ))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Botão fechar
            tk.Button(backup_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=backup_window.destroy).pack(pady=10)
                     
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar backups: {e}")
    
    def sair_sistema(self):
        """Sair do sistema"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.root.quit()
    
    # ===== FUNÇÕES DO SISTEMA DE USUÁRIOS =====
    
    def efetuar_login(self):
        """Abrir tela de login"""
        self.sistema_login.tela_login(parent=self.root, callback_sucesso=self.inicializar_sistema_apos_login)
    
    def login_realizado(self):
        """Callback executado após login bem-sucedido"""
        usuario = self.sistema_login.usuario_logado
        if usuario:
            self.status_bar.config(text=f"Usuário logado: {usuario['nome']} ({usuario['depto']})")
    
    def cadastro_usuarios(self):
        """Abrir cadastro de usuários"""
        if not self.cadastro_usuarios_modulo:
            self.cadastro_usuarios_modulo = CadastroUsuarios(self.root, self.db_path)
        self.cadastro_usuarios_modulo.abrir()
    
    def autorizacao_senhas(self):
        """Abrir autorização de senhas"""
        if not self.autorizacao_senhas_modulo:
            self.autorizacao_senhas_modulo = AutorizacaoSenhas(self.root, self.db_path)
        self.autorizacao_senhas_modulo.abrir()
    
    def abrir_configuracoes(self):
        """Abrir configurações do sistema"""
        if not self.configuracoes_modulo:
            self.configuracoes_modulo = ConfiguracoesSistema(self.root, self.db_path)
        self.configuracoes_modulo.abrir()
    
    # ===== FUNÇÕES DE CONSULTA READONLY =====
    def consultar_produtos_readonly(self):
        """Abrir cadastro de produtos em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Produtos (Apenas Visualização)")
            consulta_window.geometry("1000x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="📦 Consulta de Produtos", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de produtos
            columns = ('Código', 'Descrição', 'Estoque', 'Unidade', 'Categoria', 'Marca', 'Preço')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column('Código', width=80)
            tree.column('Descrição', width=250)
            tree.column('Estoque', width=80)
            tree.column('Unidade', width=80)
            tree.column('Categoria', width=120)
            tree.column('Marca', width=120)
            tree.column('Preço', width=100)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT codigo, descricao, estoque_atual, unidade, categoria, marca, preco 
                FROM produtos 
                WHERE ativo = 1 
                ORDER BY descricao
            """)
            produtos = cursor.fetchall()
            conn.close()
            
            for produto in produtos:
                # Formatar preço
                produto_formatado = list(produto)
                if produto_formatado[6]:  # preço
                    produto_formatado[6] = f"R$ {produto_formatado[6]:.2f}"
                tree.insert('', tk.END, values=produto_formatado)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Produtos (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar produtos: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_fornecedores_readonly(self):
        """Abrir cadastro de fornecedores em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Fornecedores (Apenas Visualização)")
            consulta_window.geometry("1000x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="🏢 Consulta de Fornecedores", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de fornecedores
            columns = ('Código', 'Nome', 'Telefone', 'Email', 'Cidade', 'UF')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column('Código', width=80)
            tree.column('Nome', width=250)
            tree.column('Telefone', width=120)
            tree.column('Email', width=200)
            tree.column('Cidade', width=150)
            tree.column('UF', width=50)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT codigo, nome, telefone, email, cidade, uf 
                FROM fornecedores 
                WHERE ativo = 1 
                ORDER BY nome
            """)
            fornecedores = cursor.fetchall()
            conn.close()
            
            for fornecedor in fornecedores:
                tree.insert('', tk.END, values=fornecedor)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Fornecedores (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar fornecedores: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_clientes_readonly(self):
        """Abrir cadastro de clientes em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Clientes (Apenas Visualização)")
            consulta_window.geometry("1000x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="👥 Consulta de Clientes", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de clientes
            columns = ('Nome', 'Telefone', 'Email', 'Cidade', 'UF')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column('Nome', width=250)
            tree.column('Telefone', width=120)
            tree.column('Email', width=200)
            tree.column('Cidade', width=150)
            tree.column('UF', width=50)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, telefone, email, cidade, uf 
                FROM clientes 
                WHERE ativo = 1 
                ORDER BY nome
            """)
            clientes = cursor.fetchall()
            conn.close()
            
            for cliente in clientes:
                tree.insert('', tk.END, values=cliente)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Clientes (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar clientes: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_funcionarios_readonly(self):
        """Abrir cadastro de funcionários em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Funcionários (Apenas Visualização)")
            consulta_window.geometry("1000x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="👤 Consulta de Funcionários", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de funcionários
            columns = ('Nome', 'Cargo', 'Email', 'Telefone', 'Cidade', 'Status')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column('Nome', width=200)
            tree.column('Cargo', width=150)
            tree.column('Email', width=200)
            tree.column('Telefone', width=120)
            tree.column('Cidade', width=120)
            tree.column('Status', width=80)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, cargo, email, telefone, cidade, ativo 
                FROM funcionarios 
                ORDER BY nome
            """)
            funcionarios = cursor.fetchall()
            conn.close()
            
            for funcionario in funcionarios:
                # Converter status para texto
                funcionario_formatado = list(funcionario)
                funcionario_formatado[5] = "Ativo" if funcionario_formatado[5] == 1 else "Inativo"
                tree.insert('', tk.END, values=funcionario_formatado)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Funcionários (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar funcionários: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_estoque_readonly(self):
        """Consultar estoque atual sem permissão de exportação"""
        try:
            # Criar janela de consulta simples sem botões de exportação
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Estoque (Apenas Visualização)")
            consulta_window.geometry("800x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="📊 Consulta de Estoque", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de produtos
            columns = ('Código', 'Produto', 'Estoque', 'Unidade', 'Categoria')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            tree.heading('Código', text='Código')
            tree.heading('Produto', text='Produto')
            tree.heading('Estoque', text='Estoque')
            tree.heading('Unidade', text='Unidade')
            tree.heading('Categoria', text='Categoria')
            
            tree.column('Código', width=80)
            tree.column('Produto', width=300)
            tree.column('Estoque', width=100)
            tree.column('Unidade', width=80)
            tree.column('Categoria', width=150)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT codigo, descricao, estoque_atual, unidade, categoria 
                FROM produtos 
                WHERE ativo = 1 
                ORDER BY descricao
            """)
            produtos = cursor.fetchall()
            conn.close()
            
            for produto in produtos:
                tree.insert('', tk.END, values=produto)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar (sem exportação)
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de estoque realizada (apenas visualização)")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {e}")
    
    def consultar_emprestimos_readonly(self):
        """Consultar empréstimos em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Empréstimos (Apenas Visualização)")
            consulta_window.geometry("1200x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="🔄 Consulta de Empréstimos", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Frame de filtros simples
            filter_frame = tk.Frame(main_frame, bg='#f8f9fa')
            filter_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(filter_frame, text="Status:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
            status_var = tk.StringVar()
            combo_status = ttk.Combobox(filter_frame, textvariable=status_var, width=15, state='readonly')
            combo_status['values'] = ('TODOS', 'EMPRESTADO', 'DEVOLVIDO')
            combo_status.set('TODOS')
            combo_status.pack(side=tk.LEFT, padx=5)
            
            # Tabela de empréstimos
            columns = ('Código', 'Data', 'Funcionário', 'Item', 'Status')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column('Código', width=80)
            tree.column('Data', width=100)
            tree.column('Funcionário', width=200)
            tree.column('Item', width=300)
            tree.column('Status', width=100)
            
            def carregar_emprestimos():
                # Limpar tabela
                for item in tree.get_children():
                    tree.delete(item)
                
                # Carregar dados dos empréstimos
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                filtro_status = status_var.get()
                
                if filtro_status == 'TODOS':
                    cursor.execute("""
                        SELECT codigo, data, funcionario, descricao_item, status 
                        FROM emprestimos 
                        ORDER BY data DESC
                    """)
                else:
                    cursor.execute("""
                        SELECT codigo, data, funcionario, descricao_item, status 
                        FROM emprestimos 
                        WHERE status = ?
                        ORDER BY data DESC
                    """, (filtro_status,))
                
                emprestimos = cursor.fetchall()
                conn.close()
                
                for emprestimo in emprestimos:
                    tree.insert('', tk.END, values=emprestimo)
                
                # Atualizar contador
                total = len(emprestimos)
                tk.Label(main_frame, text=f"Total de registros: {total}", 
                        font=('Arial', 10), fg='#2c3e50', bg='#f8f9fa').pack()
            
            # Bind do filtro
            combo_status.bind('<<ComboboxSelected>>', lambda e: carregar_emprestimos())
            
            # Carregar dados iniciais
            carregar_emprestimos()
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar (SEM botões de ação)
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Empréstimos (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar empréstimos: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_categoria_readonly(self):
        """Consultar categoria em modo apenas leitura"""
        try:
            # Criar janela de consulta simples
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Categorias (Apenas Visualização)")
            consulta_window.geometry("800x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="📂 Consulta de Categorias", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Tabela de categorias
            columns = ('ID', 'Nome da Categoria', 'Data Cadastro')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            tree.heading('ID', text='ID')
            tree.heading('Nome da Categoria', text='Nome da Categoria')
            tree.heading('Data Cadastro', text='Data Cadastro')
            
            tree.column('ID', width=50)
            tree.column('Nome da Categoria', width=300)
            tree.column('Data Cadastro', width=150)
            
            # Carregar dados
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, data_cadastro 
                FROM categorias_produtos 
                ORDER BY nome
            """)
            categorias = cursor.fetchall()
            conn.close()
            
            for categoria in categorias:
                tree.insert('', tk.END, values=categoria)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Informações adicionais
            info_frame = tk.Frame(main_frame, bg='#f8f9fa')
            info_frame.pack(fill=tk.X, pady=10)
            
            total_categorias = len(categorias)
            tk.Label(info_frame, text=f"Total de Categorias: {total_categorias}", 
                    font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack()
            
            # Apenas botão fechar (SEM botões de ação)
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de Categorias (Apenas Leitura)")
        except Exception as e:
            print(f"Erro detalhado ao consultar categorias: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao abrir consulta: {e}")
    
    def consultar_movimentacoes_readonly(self):
        """Consultar movimentações sem permissão de exportação"""
        try:
            # Criar janela de consulta simples sem botões de exportação
            consulta_window = tk.Toplevel(self.root)
            consulta_window.title("Consulta de Movimentações (Apenas Visualização)")
            consulta_window.geometry("1000x600")
            consulta_window.configure(bg='#f8f9fa')
            consulta_window.transient(self.root)
            consulta_window.grab_set()
            
            # Bind ESC para fechar apenas esta janela
            consulta_window.bind('<Escape>', lambda e: consulta_window.destroy())
            
            # Frame principal
            main_frame = tk.Frame(consulta_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="📋 Consulta de Movimentações", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=10)
            
            # Frame de filtros
            filter_frame = tk.Frame(main_frame, bg='#f8f9fa')
            filter_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(filter_frame, text="Tipo:", bg='#f8f9fa').pack(side=tk.LEFT, padx=5)
            tipo_var = tk.StringVar()
            combo_tipo = ttk.Combobox(filter_frame, textvariable=tipo_var, width=10)
            combo_tipo['values'] = ('TODOS', 'ENTRADA', 'SAÍDA')
            combo_tipo.set('TODOS')
            combo_tipo.pack(side=tk.LEFT, padx=5)
            
            # Tabela de movimentações
            columns = ('Data', 'Produto', 'Tipo', 'Quantidade', 'Usuário')
            tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
            
            # Configurar colunas
            tree.heading('Data', text='Data')
            tree.heading('Produto', text='Produto')
            tree.heading('Tipo', text='Tipo')
            tree.heading('Quantidade', text='Quantidade')
            tree.heading('Usuário', text='Usuário')
            
            tree.column('Data', width=120)
            tree.column('Produto', width=300)
            tree.column('Tipo', width=100)
            tree.column('Quantidade', width=100)
            tree.column('Usuário', width=150)
            
            def carregar_movimentacoes():
                # Limpar tabela
                for item in tree.get_children():
                    tree.delete(item)
                
                # Carregar dados
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                filtro_tipo = tipo_var.get()
                if filtro_tipo == 'TODOS':
                    cursor.execute("""
                        SELECT data_movimento, codigo_produto, tipo_movimento, quantidade_movimento, origem 
                        FROM log_movimentacoes 
                        ORDER BY data_movimento DESC 
                        LIMIT 1000
                    """)
                else:
                    cursor.execute("""
                        SELECT data_movimento, codigo_produto, tipo_movimento, quantidade_movimento, origem 
                        FROM log_movimentacoes 
                        WHERE tipo_movimento = ?
                        ORDER BY data_movimento DESC 
                        LIMIT 1000
                    """, (filtro_tipo,))
                
                movimentacoes = cursor.fetchall()
                conn.close()
                
                for mov in movimentacoes:
                    tree.insert('', tk.END, values=mov)
            
            # Bind do filtro
            combo_tipo.bind('<<ComboboxSelected>>', lambda e: carregar_movimentacoes())
            
            # Carregar dados iniciais
            carregar_movimentacoes()
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Apenas botão fechar (sem exportação)
            tk.Button(consulta_window, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=consulta_window.destroy).pack(pady=10)
                     
            self.status_bar.config(text="Consulta de movimentações realizada (apenas visualização)")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {e}")
    
    def alterar_senha(self):
        """Abrir tela de alterar senha"""
        self.sistema_login.tela_alterar_senha()
    
    def verificar_solicitacoes_senha_pendentes(self):
        """Verificar se há solicitações de senha pendentes (apenas para admin)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM solicitacoes_senha 
                WHERE status = 'PENDENTE' AND visualizado = 0
            ''')
            
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Buscar detalhes das solicitações
                cursor.execute('''
                    SELECT usuario, departamento, data_solicitacao 
                    FROM solicitacoes_senha 
                    WHERE status = 'PENDENTE' AND visualizado = 0
                    ORDER BY data_solicitacao DESC
                ''')
                
                solicitacoes = cursor.fetchall()
                
                # Marcar como visualizado
                cursor.execute('''
                    UPDATE solicitacoes_senha 
                    SET visualizado = 1 
                    WHERE status = 'PENDENTE' AND visualizado = 0
                ''')
                conn.commit()
                
                # Montar mensagem
                mensagem = f"🔔 Você tem {count} solicitação(ões) de recuperação de senha pendente(s):\n\n"
                
                for sol in solicitacoes:
                    usuario, depto, data = sol
                    data_formatada = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M')
                    mensagem += f"• {usuario} ({depto}) - {data_formatada}\n"
                
                mensagem += f"\n📋 Para resetar a senha:\n"
                mensagem += f"1. Vá em 'Usuários e Login' → 'Autorização de Senhas'\n"
                mensagem += f"2. Selecione o usuário\n"
                mensagem += f"3. Defina uma nova senha temporária\n"
                mensagem += f"4. Entre em contato com o usuário"
                
                messagebox.showwarning("Solicitações de Senha Pendentes", mensagem)
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro ao verificar solicitações: {e}")
    
    def fazer_logout(self):
        """Fazer logout do sistema"""
        if messagebox.askyesno("Logout", "Deseja realmente sair do sistema?\n\nVocê precisará fazer login novamente."):
            # Limpar dados do usuário
            self.usuario_logado = False
            self.usuario_admin = False
            self.permissoes_usuario = {}
            self.sistema_login.usuario_logado = None
            
            # Recriar menu sem acesso
            self.criar_menu()
            
            # Atualizar status
            self.status_bar.config(text="Sistema bloqueado - Faça login para acessar as funcionalidades")
            
            messagebox.showinfo("Logout", "Logout realizado com sucesso!\n\nFaça login para acessar o sistema.")
    
    def iniciar_timer_inatividade(self):
        """Iniciar timer de inatividade"""
        self.parar_timer_inatividade()  # Parar timer anterior se existir
        if self.usuario_logado:
            self.timer_inatividade = self.root.after(self.tempo_inatividade, self.logout_por_inatividade)
    
    def parar_timer_inatividade(self):
        """Parar timer de inatividade"""
        if self.timer_inatividade:
            self.root.after_cancel(self.timer_inatividade)
            self.timer_inatividade = None
    
    def resetar_timer_inatividade(self):
        """Resetar timer de inatividade (chamado em qualquer interação)"""
        if self.usuario_logado:
            self.iniciar_timer_inatividade()
    
    def logout_por_inatividade(self):
        """Fazer logout automático por inatividade"""
        if self.usuario_logado:
            # Limpar dados do usuário
            self.usuario_logado = False
            self.sistema_login.usuario_logado = None
            
            # Parar timer
            self.parar_timer_inatividade()
            
            # Recriar menu sem acesso
            self.criar_menu()
            
            # Atualizar status
            self.status_bar.config(text="Sistema bloqueado por inatividade - Faça login para acessar")
            
            # Mostrar aviso
            messagebox.showwarning("Sessão Expirada", 
                                 "Sua sessão expirou por inatividade (60 minutos).\n\n" +
                                 "Faça login novamente para continuar usando o sistema.")
    
    def configurar_eventos_atividade(self):
        """Configurar eventos para detectar atividade do usuário"""
        # Bind eventos de mouse e teclado na janela principal
        self.root.bind('<Motion>', lambda e: self.resetar_timer_inatividade())
        self.root.bind('<Button>', lambda e: self.resetar_timer_inatividade())
        self.root.bind('<Key>', lambda e: self.resetar_timer_inatividade())
        
        # Bind específico para ESC na janela principal - NÃO FECHAR O SISTEMA
        # ESC na janela principal não deve fazer nada
        self.root.bind('<Escape>', lambda e: self.resetar_timer_inatividade())
        
        # Bind recursivo para todos os widgets filhos
        def bind_recursivo(widget):
            # Pular se for uma janela Toplevel (deixar que ela gerencie seu próprio ESC)
            if isinstance(widget, tk.Toplevel):
                return
                
            widget.bind('<Motion>', lambda e: self.resetar_timer_inatividade(), add='+')
            widget.bind('<Button>', lambda e: self.resetar_timer_inatividade(), add='+')
            
            # Para teclas, resetar timer mas não interferir com ESC
            widget.bind('<KeyPress>', lambda e: self.resetar_timer_inatividade(), add='+')
            
            for child in widget.winfo_children():
                bind_recursivo(child)
        
        # Aplicar a todos os widgets
        bind_recursivo(self.root)
    
    def ativacao_sistema(self):
        """Abrir tela de ativação do sistema"""
        self.sistema_ativacao.tela_ativacao_manual()
    
    def status_licenca(self):
        """Mostrar status da licença do sistema"""
        try:
            # Verificar validade
            valido = self.sistema_ativacao.verificar_validade()
            
            # Criar janela de status
            status_window = tk.Toplevel(self.root)
            status_window.title("Status da Licença")
            status_window.geometry("500x350")
            status_window.configure(bg='#f8f9fa')
            status_window.resizable(False, False)
            
            # Centralizar janela
            status_window.update_idletasks()
            x = (status_window.winfo_screenwidth() // 2) - 250
            y = (status_window.winfo_screenheight() // 2) - 175
            status_window.geometry(f'500x350+{x}+{y}')
            
            status_window.transient(self.root)
            status_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(status_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            if valido:
                tk.Label(main_frame, text="✅ Sistema Ativado", 
                        font=('Arial', 16, 'bold'), fg='#28a745', bg='#f8f9fa').pack(pady=10)
            else:
                tk.Label(main_frame, text="❌ Sistema Vencido", 
                        font=('Arial', 16, 'bold'), fg='#dc3545', bg='#f8f9fa').pack(pady=10)
            
            # Informações da licença
            info_frame = tk.Frame(main_frame, bg='#fff', relief=tk.SUNKEN, bd=2)
            info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Obter informações do sistema de ativação
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT data_ativacao, data_vencimento FROM sistema_ativacao ORDER BY id DESC LIMIT 1")
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    data_ativacao, data_vencimento = result
                    
                    # Formatar datas
                    if data_ativacao:
                        data_ativ_formatada = datetime.strptime(data_ativacao, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                    else:
                        data_ativ_formatada = "Não ativado"
                    
                    if data_vencimento:
                        data_venc_formatada = datetime.strptime(data_vencimento, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                        data_venc_obj = datetime.strptime(data_vencimento, '%Y-%m-%d %H:%M:%S.%f')
                        dias_restantes = (data_venc_obj - datetime.now()).days
                    else:
                        data_venc_formatada = "N/A"
                        dias_restantes = 0
                    
                    tk.Label(info_frame, text=f"Data de Ativação: {data_ativ_formatada}", 
                            font=('Arial', 11), bg='#fff').pack(anchor='w', padx=15, pady=5)
                    tk.Label(info_frame, text=f"Data de Vencimento: {data_venc_formatada}", 
                            font=('Arial', 11), bg='#fff').pack(anchor='w', padx=15, pady=5)
                    
                    if dias_restantes > 0:
                        tk.Label(info_frame, text=f"Dias Restantes: {dias_restantes} dias", 
                                font=('Arial', 11, 'bold'), bg='#fff', fg='#28a745').pack(anchor='w', padx=15, pady=5)
                    else:
                        tk.Label(info_frame, text=f"Status: Vencido há {abs(dias_restantes)} dias", 
                                font=('Arial', 11, 'bold'), bg='#fff', fg='#dc3545').pack(anchor='w', padx=15, pady=5)
                else:
                    tk.Label(info_frame, text="Sistema não ativado", 
                            font=('Arial', 11), bg='#fff').pack(anchor='w', padx=15, pady=5)
                    
            except Exception as e:
                tk.Label(info_frame, text=f"Erro ao verificar licença: {e}", 
                        font=('Arial', 11), bg='#fff', fg='#dc3545').pack(anchor='w', padx=15, pady=5)
            
            # Botões
            btn_frame = tk.Frame(main_frame, bg='#f8f9fa')
            btn_frame.pack(pady=20)
            
            if not valido:
                tk.Button(btn_frame, text="🔑 Ativar Sistema", font=('Arial', 10, 'bold'),
                         bg='#28a745', fg='white', width=15,
                         command=lambda: [status_window.destroy(), self.ativacao_sistema()]).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="Fechar", font=('Arial', 10, 'bold'),
                     bg='#6c757d', fg='white', width=15,
                     command=status_window.destroy).pack(side=tk.RIGHT, padx=10)
                     
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar status da licença: {e}")
    
    def verificar_sistema_valido(self):
        """Verificar se o sistema é válido antes de iniciar"""
        if not self.sistema_ativacao.verificar_validade():
            # Sistema vencido - mostrar tela de bloqueio
            return self.sistema_ativacao.tela_sistema_bloqueado()
        return True
    
    def run(self):
        """Executar sistema"""
        self.root.mainloop()

    def mostrar_sobre(self):
        """Mostrar informações sobre o sistema"""
        sobre_window = tk.Toplevel(self.root)
        sobre_window.title("Sobre o Sistema")
        sobre_window.geometry("450x400")  # Aumentado para caber todas as informações
        sobre_window.resizable(False, False)
        sobre_window.configure(bg='#f8f9fa')
        
        # Centralizar janela corretamente
        sobre_window.update_idletasks()
        width = 450
        height = 400
        screen_width = sobre_window.winfo_screenwidth()
        screen_height = sobre_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        sobre_window.geometry(f'{width}x{height}+{x}+{y}')
        
        sobre_window.transient(self.root)
        sobre_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(sobre_window, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo/Título
        tk.Label(main_frame, text="📦", font=('Arial', 48), bg='#f8f9fa').pack(pady=10)
        
        tk.Label(main_frame, text="Sistema de Controle de Estoque", 
                font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=5)
        

        
        # Informações
        info_frame = tk.Frame(main_frame, bg='#f8f9fa')
        info_frame.pack(pady=20)
        
        tk.Label(info_frame, text="Versão: 2.0", 
                font=('Arial', 10), bg='#f8f9fa').pack(anchor='w')
        
        tk.Label(info_frame, text="Desenvolvido em: Python/Tkinter", 
                font=('Arial', 10), bg='#f8f9fa').pack(anchor='w')
        
        tk.Label(info_frame, text="Banco de Dados: SQLite", 
                font=('Arial', 10), bg='#f8f9fa').pack(anchor='w')
        
        tk.Label(info_frame, text="Data: Novembro 2025", 
                font=('Arial', 10), bg='#f8f9fa').pack(anchor='w')
        
        # Separador
        tk.Label(info_frame, text="", bg='#f8f9fa').pack(pady=5)
        
        # Informações do desenvolvedor
        tk.Label(info_frame, text="Desenvolvedor: Ervanio F Rodrigues", 
                font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        
        tk.Label(info_frame, text="Propriedade Intelectual (PI)", 
                font=('Arial', 10), bg='#f8f9fa').pack(anchor='w')
        
        tk.Label(info_frame, text="Contato: ervanio.rodrigues@gmail.com", 
                font=('Arial', 10), bg='#f8f9fa', fg='#007bff').pack(anchor='w')
        
        # Botão fechar
        tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                 bg='#6c757d', fg='white', width=15,
                 command=sobre_window.destroy).pack(pady=20)

    def zerar_tudo_completo(self):
        """Zerar completamente todo o sistema"""
        # Janela de confirmação detalhada
        janela_confirmacao = tk.Toplevel(self.root)
        janela_confirmacao.title("⚠️ ATENÇÃO - Zerar Tudo")
        janela_confirmacao.geometry("500x400")
        janela_confirmacao.resizable(False, False)
        janela_confirmacao.configure(bg='#f8f9fa')
        janela_confirmacao.transient(self.root)
        janela_confirmacao.grab_set()
        
        # Centralizar janela
        janela_confirmacao.update_idletasks()
        x = (janela_confirmacao.winfo_screenwidth() // 2) - (250)
        y = (janela_confirmacao.winfo_screenheight() // 2) - (200)
        janela_confirmacao.geometry(f'500x400+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(janela_confirmacao, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título de aviso
        tk.Label(main_frame, text="⚠️ ATENÇÃO", 
                font=('Arial', 18, 'bold'), fg='#dc3545', bg='#f8f9fa').pack(pady=10)
        
        tk.Label(main_frame, text="Esta operação irá APAGAR TODOS os dados:", 
                font=('Arial', 12, 'bold'), fg='#495057', bg='#f8f9fa').pack(pady=5)
        
        # Lista do que será apagado
        lista_frame = tk.Frame(main_frame, bg='#fff', relief=tk.SUNKEN, bd=2)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        itens = [
            "🗑️ Todos os estoques de produtos (zerados)",
            "📋 Todo histórico de movimentações",
            "🔄 Todos os empréstimos registrados",
            "📊 Todas as entradas e saídas",
            "⚠️ ESTA AÇÃO NÃO PODE SER DESFEITA!"
        ]
        
        for item in itens:
            tk.Label(lista_frame, text=item, font=('Arial', 10), 
                    fg='#495057', bg='#fff', anchor='w').pack(fill=tk.X, padx=10, pady=3)
        
        # Aviso final
        tk.Label(main_frame, text="Tem certeza que deseja continuar?", 
                font=('Arial', 12, 'bold'), fg='#dc3545', bg='#f8f9fa').pack(pady=10)
        
        # Botões
        botoes_frame = tk.Frame(main_frame, bg='#f8f9fa')
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="❌ Cancelar", font=('Arial', 11, 'bold'), 
                 bg='#6c757d', fg='white', width=15,
                 command=janela_confirmacao.destroy).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botoes_frame, text="🗑️ ZERAR TUDO", font=('Arial', 11, 'bold'), 
                 bg='#dc3545', fg='white', width=15,
                 command=lambda: self.executar_zerar_tudo(janela_confirmacao)).pack(side=tk.LEFT, padx=10)
    
    def executar_zerar_tudo(self, janela_confirmacao):
        """Executar limpeza completa de TODAS as tabelas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            print("🗑️ Iniciando limpeza completa de todas as tabelas...")
            
            # 1. Limpar Empréstimos
            try:
                cursor.execute("DELETE FROM emprestimos")
                print("✅ Empréstimos limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar empréstimos: {e}")
            
            # 2. Limpar Produtos
            try:
                cursor.execute("DELETE FROM produtos")
                print("✅ Produtos limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar produtos: {e}")
            
            # 3. Limpar Funcionários
            try:
                cursor.execute("DELETE FROM funcionarios")
                print("✅ Funcionários limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar funcionários: {e}")
            
            # 4. Limpar Fornecedores
            try:
                cursor.execute("DELETE FROM fornecedores")
                print("✅ Fornecedores limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar fornecedores: {e}")
            
            # 5. Limpar Clientes
            try:
                cursor.execute("DELETE FROM clientes")
                print("✅ Clientes limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar clientes: {e}")
            
            # 6. Limpar Cadastros Diversos (Unidades, Marcas, Categorias, Operações)
            try:
                cursor.execute("DELETE FROM unidades_div")
                cursor.execute("DELETE FROM marcas_div")
                cursor.execute("DELETE FROM categorias_div")
                cursor.execute("DELETE FROM operacoes_div")
                print("✅ Cadastros Diversos limpos")
            except Exception as e:
                print(f"⚠️ Erro ao limpar cadastros diversos: {e}")
            
            # 7. Limpar histórico de movimentações
            try:
                cursor.execute("DELETE FROM historico_estoque")
                print("✅ Histórico de estoque limpo")
            except Exception as e:
                print(f"⚠️ Erro ao limpar histórico: {e}")
            
            # 8. Limpar log de movimentações
            try:
                cursor.execute("DELETE FROM log_movimentacoes")
                print("✅ Log de movimentações limpo")
            except Exception as e:
                print(f"⚠️ Erro ao limpar log: {e}")
            
            # 9. Limpar entradas e saídas
            try:
                cursor.execute("DELETE FROM entradas_estoque")
                print("✅ Entradas limpas")
            except Exception as e:
                print(f"⚠️ Erro ao limpar entradas: {e}")
            
            try:
                cursor.execute("DELETE FROM saidas_estoque")
                print("✅ Saídas limpas")
            except Exception as e:
                print(f"⚠️ Erro ao limpar saídas: {e}")
            
            # 10. Limpar movimentações gerais
            try:
                cursor.execute("DELETE FROM movimentacoes")
                print("✅ Movimentações limpas")
            except Exception as e:
                print(f"⚠️ Erro ao limpar movimentações: {e}")
            
            conn.commit()
            janela_confirmacao.destroy()
            
            messagebox.showinfo("Sucesso", "✅ SISTEMA COMPLETAMENTE ZERADO!\n\n" +
                              "Todas as tabelas foram limpas:\n" +
                              "• Produtos\n" +
                              "• Funcionários\n" +
                              "• Fornecedores\n" +
                              "• Clientes\n" +
                              "• Cadastros Diversos\n" +
                              "• Empréstimos\n" +
                              "• Históricos e Logs\n\n" +
                              "Sistema pronto para novo controle!")
            self.status_bar.config(text="Sistema completamente zerado - Pronto para novo controle")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao zerar dados: {e}")
        finally:
            if conn:
                conn.close()
    
    def zerar_apenas_estoque(self):
        """Zerar apenas os estoques dos produtos"""
        if messagebox.askyesno("Confirmar", 
                              "Zerar apenas os estoques de todos os produtos?\n\n" +
                              "Os produtos permanecerão cadastrados, mas com estoque ZERO."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("UPDATE produtos SET estoque_atual = 0")
                conn.commit()
                
                messagebox.showinfo("Sucesso", "✅ Estoques zerados!\n\nTodos os produtos agora têm estoque ZERO.")
                self.status_bar.config(text="Estoques zerados")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao zerar estoque: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_historico(self):
        """Limpar apenas o histórico de movimentações"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar todo o histórico de movimentações?\n\n" +
                              "Isso inclui:\n• Entradas de estoque\n• Saídas de estoque\n• Histórico de movimentações"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Limpar histórico se a tabela existir
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historico_estoque'")
                if cursor.fetchone():
                    cursor.execute("DELETE FROM historico_estoque")
                
                # Limpar movimentações se a tabela existir
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movimentacoes'")
                if cursor.fetchone():
                    cursor.execute("DELETE FROM movimentacoes")
                
                conn.commit()
                
                messagebox.showinfo("Sucesso", "✅ Histórico limpo!\n\nTodas as movimentações foram removidas.")
                self.status_bar.config(text="Histórico de movimentações limpo")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar histórico: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_movimentacoes(self):
        """Limpar todas as entradas e saídas de estoque (movimentações)"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar todas as movimentações de estoque?\n\n" +
                              "Isso irá remover:\n• Todas as ENTRADAS de estoque\n• Todas as SAÍDAS de estoque\n• Histórico completo de movimentações\n• Log de movimentações\n\n" +
                              "⚠️ Esta ação não pode ser desfeita!\n⚠️ O estoque atual dos produtos será mantido."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                total_removidos = 0
                tabelas_limpas = []
                
                # Limpar tabela de entradas de estoque
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entradas_estoque'")
                if cursor.fetchone():
                    cursor.execute("SELECT COUNT(*) FROM entradas_estoque")
                    count_entradas = cursor.fetchone()[0]
                    cursor.execute("DELETE FROM entradas_estoque")
                    total_removidos += count_entradas
                    tabelas_limpas.append(f"entradas_estoque ({count_entradas} registros)")
                
                # Limpar tabela de saídas de estoque
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='saidas_estoque'")
                if cursor.fetchone():
                    cursor.execute("SELECT COUNT(*) FROM saidas_estoque")
                    count_saidas = cursor.fetchone()[0]
                    cursor.execute("DELETE FROM saidas_estoque")
                    total_removidos += count_saidas
                    tabelas_limpas.append(f"saidas_estoque ({count_saidas} registros)")
                
                # Limpar tabela log_movimentacoes
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='log_movimentacoes'")
                if cursor.fetchone():
                    cursor.execute("SELECT COUNT(*) FROM log_movimentacoes")
                    count_log = cursor.fetchone()[0]
                    cursor.execute("DELETE FROM log_movimentacoes")
                    total_removidos += count_log
                    tabelas_limpas.append(f"log_movimentacoes ({count_log} registros)")
                
                # Limpar outras tabelas relacionadas se existirem
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historico_estoque'")
                if cursor.fetchone():
                    cursor.execute("SELECT COUNT(*) FROM historico_estoque")
                    count_historico = cursor.fetchone()[0]
                    cursor.execute("DELETE FROM historico_estoque")
                    total_removidos += count_historico
                    tabelas_limpas.append(f"historico_estoque ({count_historico} registros)")
                
                conn.commit()
                
                # Mostrar resultado detalhado
                tabelas_texto = "\n• ".join(tabelas_limpas)
                messagebox.showinfo("Sucesso", 
                                  f"✅ Movimentações limpas com sucesso!\n\n" +
                                  f"📊 Total de registros removidos: {total_removidos}\n\n" +
                                  f"📋 Tabelas limpas:\n• {tabelas_texto}\n\n" +
                                  f"ℹ️ O estoque atual dos produtos foi mantido.")
                
                self.status_bar.config(text=f"Movimentações limpas: {total_removidos} registros removidos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar movimentações: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_emprestimos(self):
        """Limpar apenas os empréstimos"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar todos os empréstimos?\n\n" +
                              "Isso irá remover:\n• Todos os empréstimos registrados\n• Histórico de empréstimos"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM emprestimos")
                conn.commit()
                
                messagebox.showinfo("Sucesso", "✅ Empréstimos limpos!\n\nTodos os empréstimos foram removidos.")
                self.status_bar.config(text="Empréstimos limpos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar empréstimos: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_historico_emprestimos(self):
        """Limpar apenas o histórico de empréstimos"""
        if messagebox.askyesno("Confirmar", 
                              "Zerar Histórico de Empréstimo?\n\n" +
                              "Isso irá remover:\n• Todo o histórico de empréstimos\n• Registros de devoluções\n• Logs de movimentações de empréstimo"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Limpar empréstimos
                cursor.execute("DELETE FROM emprestimos")
                
                # Limpar logs de movimentações relacionados a empréstimos
                cursor.execute("DELETE FROM log_movimentacoes WHERE origem LIKE '%Empréstimo%'")
                
                conn.commit()
                
                messagebox.showinfo("Sucesso", "✅ Histórico de empréstimo zerado!\n\nTodo o histórico foi removido.")
                self.status_bar.config(text="Histórico de empréstimo zerado")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao zerar histórico: {e}")
            finally:
                if conn:
                    conn.close()

    def limpar_fornecedores(self):
        """Limpar todos os fornecedores cadastrados"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar TODOS os fornecedores cadastrados?\n\n" +
                              "⚠️ Esta ação NÃO PODE ser desfeita!\n\n" +
                              "Todos os fornecedores serão removidos permanentemente."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM fornecedores")
                total_antes = cursor.fetchone()[0]
                
                cursor.execute("DELETE FROM fornecedores")
                conn.commit()
                
                messagebox.showinfo("Sucesso", f"✅ {total_antes} fornecedores removidos com sucesso!")
                self.status_bar.config(text="Fornecedores limpos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar fornecedores: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_clientes(self):
        """Limpar todos os clientes cadastrados"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar TODOS os clientes cadastrados?\n\n" +
                              "⚠️ Esta ação NÃO PODE ser desfeita!\n\n" +
                              "Todos os clientes serão removidos permanentemente."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM clientes")
                total_antes = cursor.fetchone()[0]
                
                cursor.execute("DELETE FROM clientes")
                conn.commit()
                
                messagebox.showinfo("Sucesso", f"✅ {total_antes} clientes removidos com sucesso!")
                self.status_bar.config(text="Clientes limpos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar clientes: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_funcionarios(self):
        """Limpar todos os funcionários cadastrados"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar TODOS os funcionários cadastrados?\n\n" +
                              "⚠️ Esta ação NÃO PODE ser desfeita!\n\n" +
                              "Todos os funcionários serão removidos permanentemente."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM funcionarios")
                total_antes = cursor.fetchone()[0]
                
                cursor.execute("DELETE FROM funcionarios")
                conn.commit()
                
                messagebox.showinfo("Sucesso", f"✅ {total_antes} funcionários removidos com sucesso!")
                self.status_bar.config(text="Funcionários limpos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar funcionários: {e}")
            finally:
                if conn:
                    conn.close()
    
    def limpar_produtos(self):
        """Limpar todos os produtos cadastrados"""
        if messagebox.askyesno("Confirmar", 
                              "Limpar TODOS os produtos cadastrados?\n\n" +
                              "⚠️ Esta ação NÃO PODE ser desfeita!\n\n" +
                              "Todos os produtos serão removidos permanentemente.\n" +
                              "Isso também removerá todo histórico relacionado."):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM produtos")
                total_antes = cursor.fetchone()[0]
                
                # Limpar produtos e dados relacionados
                cursor.execute("DELETE FROM produtos")
                cursor.execute("DELETE FROM historico_estoque")
                cursor.execute("DELETE FROM emprestimos")
                
                try:
                    cursor.execute("DELETE FROM entradas_estoque")
                    cursor.execute("DELETE FROM saidas_estoque")
                except:
                    pass
                
                conn.commit()
                
                messagebox.showinfo("Sucesso", f"✅ {total_antes} produtos e dados relacionados removidos!")
                self.status_bar.config(text="Produtos limpos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar produtos: {e}")
            finally:
                if conn:
                    conn.close()
    
    def mostrar_status_protecao(self):
        """Mostrar status do sistema de proteção"""
        try:
            status = self.backup_manager.status_sistema()
            
            # Criar janela de status
            status_window = tk.Toplevel(self.root)
            status_window.title("Status do Sistema de Proteção")
            status_window.geometry("500x400")
            status_window.configure(bg='#f8f9fa')
            status_window.transient(self.root)
            status_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(status_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="🛡️ Status do Sistema de Proteção", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=(0, 20))
            
            # Informações do banco
            info_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
            info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            tk.Label(info_frame, text="📊 Dados do Sistema:", 
                    font=('Arial', 12, 'bold'), bg='#ffffff').pack(anchor='w', padx=10, pady=(10, 5))
            
            for chave, valor in status.items():
                if chave != 'erro':
                    tk.Label(info_frame, text=f"• {chave.replace('_', ' ').title()}: {valor}", 
                            font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=20, pady=2)
            
            # Botão fechar
            tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=status_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar status: {e}")
    
    def validar_banco_manual(self):
        """Validar banco de dados manualmente"""
        try:
            # Mostrar progresso
            self.status_bar.config(text="Validando banco de dados...")
            self.root.update()
            
            # Executar validação
            self.database_validator.validar_estrutura_completa()
            self.database_validator.corrigir_produtos_inativos()
            
            messagebox.showinfo("Validação", "Validação do banco concluída!\n\nVerifique o console para detalhes.")
            self.status_bar.config(text="Validação concluída")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na validação: {e}")
    
    def listar_backups(self):
        """Listar todos os backups disponíveis"""
        try:
            backups = self.backup_manager.listar_backups()
            
            # Criar janela de listagem
            backup_window = tk.Toplevel(self.root)
            backup_window.title("Lista de Backups")
            backup_window.geometry("700x500")
            backup_window.configure(bg='#f8f9fa')
            backup_window.transient(self.root)
            backup_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(backup_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text=f"💾 Backups Disponíveis ({len(backups)})", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=(0, 20))
            
            if not backups:
                tk.Label(main_frame, text="Nenhum backup encontrado", 
                        font=('Arial', 12), fg='#6c757d', bg='#f8f9fa').pack(expand=True)
            else:
                # Lista de backups
                lista_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.SUNKEN, bd=2)
                lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                
                # Scrollbar
                scrollbar = tk.Scrollbar(lista_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Listbox
                listbox = tk.Listbox(lista_frame, font=('Courier New', 9), 
                                   yscrollcommand=scrollbar.set)
                listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.config(command=listbox.yview)
                
                # Adicionar backups à lista
                for backup in backups:
                    tamanho_mb = backup['tamanho'] / (1024 * 1024)
                    linha = f"{backup['nome']:<30} | {backup['tipo']:<10} | {backup['data']:<20} | {tamanho_mb:.1f}MB"
                    listbox.insert(tk.END, linha)
            
            # Botão fechar
            tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=backup_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar backups: {e}")
            
            # Criar janela de status
            status_window = tk.Toplevel(self.root)
            status_window.title("Status do Sistema de Proteção")
            status_window.geometry("500x400")
            status_window.configure(bg='#f8f9fa')
            status_window.transient(self.root)
            status_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(status_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text="🛡️ Status do Sistema de Proteção", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=(0, 20))
            
            # Informações do banco
            info_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
            info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            tk.Label(info_frame, text="📊 Dados do Sistema:", 
                    font=('Arial', 12, 'bold'), bg='#ffffff').pack(anchor='w', padx=10, pady=(10, 5))
            
            for chave, valor in status.items():
                if chave != 'erro':
                    tk.Label(info_frame, text=f"• {chave.replace('_', ' ').title()}: {valor}", 
                            font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=20, pady=2)
            
            # Botão fechar
            tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=status_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar status: {e}")
    
    def validar_banco_manual(self):
        """Validar banco de dados manualmente"""
        try:
            # Mostrar progresso
            self.status_bar.config(text="Validando banco de dados...")
            self.root.update()
            
            # Executar validação
            self.database_validator.validar_estrutura_completa()
            self.database_validator.corrigir_produtos_inativos()
            
            messagebox.showinfo("Validação", "Validação do banco concluída!\n\nVerifique o console para detalhes.")
            self.status_bar.config(text="Validação concluída")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na validação: {e}")
    
    def listar_backups(self):
        """Listar todos os backups disponíveis"""
        try:
            backups = self.backup_manager.listar_backups()
            
            # Criar janela de listagem
            backup_window = tk.Toplevel(self.root)
            backup_window.title("Lista de Backups")
            backup_window.geometry("700x500")
            backup_window.configure(bg='#f8f9fa')
            backup_window.transient(self.root)
            backup_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(backup_window, bg='#f8f9fa')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_frame, text=f"💾 Backups Disponíveis ({len(backups)})", 
                    font=('Arial', 16, 'bold'), fg='#2c3e50', bg='#f8f9fa').pack(pady=(0, 20))
            
            if not backups:
                tk.Label(main_frame, text="Nenhum backup encontrado", 
                        font=('Arial', 12), fg='#6c757d', bg='#f8f9fa').pack(expand=True)
            else:
                # Lista de backups
                lista_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.SUNKEN, bd=2)
                lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                
                # Scrollbar
                scrollbar = tk.Scrollbar(lista_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Listbox
                listbox = tk.Listbox(lista_frame, font=('Courier New', 9), 
                                   yscrollcommand=scrollbar.set)
                listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.config(command=listbox.yview)
                
                # Adicionar backups à lista
                for backup in backups:
                    tamanho_mb = backup['tamanho'] / (1024 * 1024)
                    linha = f"{backup['nome']:<30} | {backup['tipo']:<10} | {backup['data']:<20} | {tamanho_mb:.1f}MB"
                    listbox.insert(tk.END, linha)
            
            # Botão fechar
            tk.Button(main_frame, text="Fechar", font=('Arial', 10, 'bold'), 
                     bg='#6c757d', fg='white', width=15,
                     command=backup_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar backups: {e}")
if __name__ == "__main__":
    app = SistemaEstoque()
    app.run()