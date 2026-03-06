#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cadastro de Clientes - Layout conforme anexo
Com lista lateral e preenchimento dinâmico
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from limpeza_caracteres import limpar_caracteres_especiais

class CadastroClientes:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.window = None
        self.cliente_selecionado_id = None
        
        # Variáveis do formulário
        self.nome = tk.StringVar()
        self.codigo = tk.StringVar()
        self.email = tk.StringVar()
        self.telefone = tk.StringVar()
        self.celular = tk.StringVar()
        self.fax = tk.StringVar()
        self.endereco = tk.StringVar()
        self.cidade = tk.StringVar()
        self.uf = tk.StringVar()
        self.cep = tk.StringVar()
        self.anotacoes = tk.StringVar()
        self.ativo = tk.BooleanVar(value=True)
        
        # Variável de busca
        self.busca_rapida = tk.StringVar()
        
        # Controle de permissões
        self.permissoes = {'consulta': 1, 'inclusao': 1, 'alteracao': 1, 'exclusao': 1}  # Padrão
        self.usuario_admin = True  # Padrão
    
    def verificar_permissao(self, tipo_permissao):
        """Verificar se o usuário tem permissão para determinada ação"""
        if self.usuario_admin:
            return True  # Administrador tem todas as permissões
        return self.permissoes.get(tipo_permissao, 0) == 1
    
    def bloquear_acao_sem_permissao(self, tipo_permissao, acao="esta ação"):
        """Bloquear ação se usuário não tiver permissão"""
        if not self.verificar_permissao(tipo_permissao):
            messagebox.showwarning("Acesso Negado", 
                                 f"Você não tem permissão para {acao}.\n\n" +
                                 f"Permissão necessária: {tipo_permissao.upper()}\n" +
                                 f"Entre em contato com o administrador.")
            return True
        return False
    
    def controlar_interface_por_permissoes(self):
        """Controlar interface baseado nas permissões do usuário"""
        # Se usuário só tem permissão de consulta, desabilitar campos e botões de ação
        if not self.verificar_permissao('inclusao') and not self.verificar_permissao('alteracao'):
            # Desabilitar todos os campos de entrada
            for widget in self.window.winfo_children():
                self.desabilitar_campos_recursivo(widget)
            
            # Alterar título da janela para indicar modo apenas leitura
            self.window.title("Consulta de Clientes (Apenas Leitura)")
    
    def desabilitar_campos_recursivo(self, widget):
        """Desabilitar campos de entrada recursivamente"""
        try:
            # Se for Entry ou Text, tornar apenas leitura
            if isinstance(widget, tk.Entry):
                widget.config(state='readonly', bg='#f0f0f0')
            elif isinstance(widget, tk.Text):
                widget.config(state='disabled', bg='#f0f0f0')
            # Se for Button de ação, ocultar
            elif isinstance(widget, tk.Button):
                texto = widget.cget('text')
                if any(palavra in texto.lower() for palavra in ['salvar', 'cadastrar', 'alterar', 'excluir', 'novo', 'limpar', 'inativar', 'ativar']):
                    widget.pack_forget()  # Ocultar botão
            # Se for Label clicável de ação, desabilitar
            elif isinstance(widget, tk.Label):
                texto = widget.cget('text')
                if any(palavra in texto.lower() for palavra in ['salvar', 'cadastrar', 'alterar', 'excluir', 'novo', 'limpar', 'inativar', 'ativar']):
                    widget.config(state='disabled', fg='#cccccc')
            
            # Recursão para widgets filhos
            for child in widget.winfo_children():
                self.desabilitar_campos_recursivo(child)
        except:
            pass
        
    def abrir(self):
        """Abrir janela de cadastro de clientes"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Cadastro de Clientes")
        self.window.geometry("800x450")
        
        # Bind da tecla ESC para fechar apenas esta janela
        self.window.bind('<Escape>', lambda e: self.fechar_janela())
        
        # Garantir que a janela tenha foco para capturar ESC
        self.window.focus_force()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 400
        y = (self.window.winfo_screenheight() // 2) - 225
        self.window.geometry(f'800x450+{x}+{y}')
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(True, True)
        self.window.minsize(800, 450)
        
        self.criar_interface()
        self.carregar_clientes()
        self.gerar_proximo_codigo()
        self.controlar_interface_por_permissoes()  # Mover para o final
        
        # Garantir que apenas o botão NOVO esteja visível no início
        self.controlar_botoes()
        self.controlar_botao_exportar_inativos()
        
    def criar_interface(self):
        """Criar interface conforme anexo"""
        
        # =================== BARRA DE BOTÕES SUPERIOR ===================
        toolbar_frame = tk.Frame(self.window, bg='#e0e0e0', height=35)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        toolbar_frame.pack_propagate(False)
        
        # Labels clicáveis da toolbar (todos na mesma linha, cor uniforme)
        btn_frame = tk.Frame(toolbar_frame, bg='#e0e0e0')
        btn_frame.pack(expand=True, fill=tk.X, padx=10, pady=3)
        
        # Função para criar efeito hover uniforme
        def criar_hover_effect(label):
            def on_enter(e):
                label.config(fg='#000000', font=('Arial', 9, 'bold', 'underline'))
            def on_leave(e):
                label.config(fg='#333333', font=('Arial', 9, 'bold'))
            label.bind('<Enter>', on_enter)
            label.bind('<Leave>', on_leave)
        
        # Label Salvar (armazenar referência para controle)
        self.btn_salvar = tk.Label(btn_frame, text="💾 Salvar", font=('Arial', 9, 'bold'), 
                                  bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_salvar.pack(side=tk.LEFT, padx=8)
        self.btn_salvar.bind('<Button-1>', lambda e: self.salvar_cliente())
        criar_hover_effect(self.btn_salvar)
        
        # Label Alterar (inicialmente oculto)
        self.btn_alterar = tk.Label(btn_frame, text="✏️ Alterar", font=('Arial', 9, 'bold'), 
                                   bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_alterar.bind('<Button-1>', lambda e: self.salvar_cliente())
        criar_hover_effect(self.btn_alterar)
        
        # Label Ativar/Inativar (dinâmico)
        self.btn_ativar_inativar = tk.Label(btn_frame, text="🔴 Inativar", font=('Arial', 9, 'bold'), 
                                           bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_ativar_inativar.pack(side=tk.LEFT, padx=8)
        self.btn_ativar_inativar.bind('<Button-1>', lambda e: self.ativar_inativar_cliente())
        criar_hover_effect(self.btn_ativar_inativar)
        
        # Label Excluir (armazenar referência para controle)
        self.btn_excluir = tk.Label(btn_frame, text="🗑️ Excluir", font=('Arial', 9, 'bold'), 
                                   bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_excluir.bind('<Button-1>', lambda e: self.excluir_cliente())
        criar_hover_effect(self.btn_excluir)
        
        # Label Exportar Inativos (inicialmente oculto)
        self.btn_exportar_inativos = tk.Label(btn_frame, text="📊 Excel Inativos", font=('Arial', 9, 'bold'), 
                                             bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_exportar_inativos.bind('<Button-1>', lambda e: self.exportar_inativos_excel())
        criar_hover_effect(self.btn_exportar_inativos)
        
        # Label Exportar Ativos (inicialmente oculto)
        self.btn_exportar_ativos = tk.Label(btn_frame, text="📊 Excel Ativos", font=('Arial', 9, 'bold'), 
                                           bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_exportar_ativos.bind('<Button-1>', lambda e: self.exportar_ativos_excel())
        criar_hover_effect(self.btn_exportar_ativos)
        
        # Label NOVO
        self.btn_novo = tk.Label(btn_frame, text="📄 NOVO", font=('Arial', 9, 'bold'), 
                                bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_novo.pack(side=tk.LEFT, padx=8)
        self.btn_novo.bind('<Button-1>', lambda e: self.novo_cliente())
        criar_hover_effect(self.btn_novo)
        
        # Label LIMPAR
        self.btn_limpar = tk.Label(btn_frame, text="🧹 Limpar", font=('Arial', 9, 'bold'), 
                                  bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_limpar.pack(side=tk.LEFT, padx=8)
        self.btn_limpar.bind('<Button-1>', lambda e: self.novo_cliente())
        criar_hover_effect(self.btn_limpar)
        
        # Botões antigos removidos - agora usando labels clicáveis acima
        
        # =================== ÁREA PRINCIPAL ===================
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # =================== LADO ESQUERDO - LISTA ===================
        left_frame = tk.Frame(main_frame, bg='#f0f0f0', width=320)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Busca Rápida
        busca_frame = tk.Frame(left_frame, bg='#f0f0f0')
        busca_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(busca_frame, text="🔍 Busca Rápida", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        
        self.entry_busca = tk.Entry(busca_frame, textvariable=self.busca_rapida, 
                                   font=('Arial', 10), width=25)
        self.entry_busca.pack(anchor='w', pady=5)
        self.entry_busca.bind('<KeyRelease>', self.filtrar_lista)
        
        # Filtro de Status
        filtro_frame = tk.Frame(busca_frame, bg='#f0f0f0')
        filtro_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(filtro_frame, text="📊 Mostrar:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.filtro_status = tk.StringVar(value="ativos")
        
        tk.Radiobutton(filtro_frame, text="Ativos", variable=self.filtro_status, 
                      value="ativos", bg='#f0f0f0', font=('Arial', 9),
                      command=self.filtrar_lista_e_controlar_exportacao).pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Radiobutton(filtro_frame, text="Inativos", variable=self.filtro_status, 
                      value="inativos", bg='#f0f0f0', font=('Arial', 9),
                      command=self.filtrar_lista_e_controlar_exportacao).pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Radiobutton(filtro_frame, text="Todos", variable=self.filtro_status, 
                      value="todos", bg='#f0f0f0', font=('Arial', 9),
                      command=self.filtrar_lista_e_controlar_exportacao).pack(side=tk.LEFT, padx=(5, 0))
        
        # Frame para total de clientes cadastrados
        total_frame = tk.Frame(left_frame, bg='#f0f0f0')
        total_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        tk.Label(total_frame, text="Total de Cadastrados:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(side=tk.LEFT)
        self.label_total_clientes = tk.Label(total_frame, text="0", font=('Arial', 10, 'bold'), 
                                            bg='#e9ecef', fg='#2c3e50', width=8, relief=tk.SUNKEN)
        self.label_total_clientes.pack(side=tk.LEFT, padx=(5, 0))
        
        # Lista de funcionários
        lista_frame = tk.Frame(left_frame, bg='#f0f0f0')
        lista_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox com scrollbar
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(lista_frame, font=('Arial', 10), 
                                 yscrollcommand=scrollbar.set,
                                 selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind para seleção
        self.listbox.bind('<<ListboxSelect>>', self.cliente_selecionado)
        
        # =================== LADO DIREITO - FORMULÁRIO ===================
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frame do formulário
        form_frame = tk.Frame(right_frame, bg='#f0f0f0')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # LINHA 1: Nome e Código
        linha1 = tk.Frame(form_frame, bg='#f0f0f0')
        linha1.pack(fill=tk.X, pady=5)
        
        tk.Label(linha1, text="Nome Completo", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        entry_nome = tk.Entry(linha1, textvariable=self.nome, font=('Arial', 10), 
                             width=25)
        entry_nome.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        entry_nome.bind('<KeyRelease>', self.monitorar_campos)
        
        tk.Label(linha1, text="ID", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(side=tk.RIGHT, anchor='e')
        self.entry_codigo = tk.Entry(linha1, textvariable=self.codigo, font=('Arial', 10), 
                                    width=10, state='readonly', bg='#ffe6e6')
        self.entry_codigo.pack(side=tk.RIGHT)
        
        # LINHA 2: E-mail
        linha2 = tk.Frame(form_frame, bg='#f0f0f0')
        linha2.pack(fill=tk.X, pady=5)
        
        tk.Label(linha2, text="E-mail", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(linha2, textvariable=self.email, font=('Arial', 10), 
                width=25).pack(anchor='w')
        
        # LINHA 3: Telefones (Comercial, Celular, Fax)
        linha3 = tk.Frame(form_frame, bg='#f0f0f0')
        linha3.pack(fill=tk.X, pady=5)
        
        # Telefone Comercial
        tel_frame = tk.Frame(linha3, bg='#f0f0f0')
        tel_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(tel_frame, text="Fone Comercial", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_telefone = tk.Entry(tel_frame, textvariable=self.telefone, font=('Arial', 10), 
                width=20)
        self.entry_telefone.pack(fill=tk.X)
        self.entry_telefone.bind('<KeyRelease>', self.formatar_telefone)
        
        # Celular
        cel_frame = tk.Frame(linha3, bg='#f0f0f0')
        cel_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(cel_frame, text="Fone Celular", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_celular = tk.Entry(cel_frame, textvariable=self.celular, font=('Arial', 10), 
                width=20)
        self.entry_celular.pack(fill=tk.X)
        self.entry_celular.bind('<KeyRelease>', self.formatar_celular)
        
        # Fax
        fax_frame = tk.Frame(linha3, bg='#f0f0f0')
        fax_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(fax_frame, text="Fone Fax", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_fax = tk.Entry(fax_frame, textvariable=self.fax, font=('Arial', 10), 
                width=20)
        self.entry_fax.pack(fill=tk.X)
        self.entry_fax.bind('<KeyRelease>', self.formatar_fax)
        
        # LINHA 5: Endereço
        linha5 = tk.Frame(form_frame, bg='#f0f0f0')
        linha5.pack(fill=tk.X, pady=5)
        
        tk.Label(linha5, text="Endereço", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(linha5, textvariable=self.endereco, font=('Arial', 10), 
                width=25).pack(anchor='w')
        
        # LINHA 6: Cidade, UF, CEP
        linha6 = tk.Frame(form_frame, bg='#f0f0f0')
        linha6.pack(fill=tk.X, pady=5)
        
        # Cidade
        cidade_frame = tk.Frame(linha6, bg='#f0f0f0')
        cidade_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(cidade_frame, text="Cidade", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(cidade_frame, textvariable=self.cidade, font=('Arial', 10), 
                width=25).pack()
        
        # UF
        uf_frame = tk.Frame(linha6, bg='#f0f0f0')
        uf_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(uf_frame, text="UF", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(uf_frame, textvariable=self.uf, font=('Arial', 10), 
                width=5).pack()
        
        # CEP
        cep_frame = tk.Frame(linha6, bg='#f0f0f0')
        cep_frame.pack(side=tk.LEFT)
        tk.Label(cep_frame, text="CEP", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_cep = tk.Entry(cep_frame, textvariable=self.cep, font=('Arial', 10), 
                width=15)
        self.entry_cep.pack()
        self.entry_cep.bind('<KeyRelease>', self.formatar_cep)
        self.entry_cep.bind('<FocusOut>', self.buscar_endereco_por_cep)
        
        # LINHA 7: Anotações
        linha7 = tk.Frame(form_frame, bg='#f0f0f0')
        linha7.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(linha7, text="Anotações", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        text_anotacoes = tk.Text(linha7, font=('Arial', 10), height=3, width=25)
        text_anotacoes.pack(fill=tk.X, pady=(2, 0))
        
        # Bind para sincronizar com variável
        def atualizar_anotacoes(event=None):
            self.anotacoes.set(text_anotacoes.get("1.0", tk.END).strip())
        
        text_anotacoes.bind('<KeyRelease>', atualizar_anotacoes)
        self.text_anotacoes = text_anotacoes
        
        # LINHA 8: Status Ativo
        # Checkbox Cliente Ativo removido conforme solicitado
        
    def controlar_botoes(self):
        """4 REGRAS SIMPLES E DIRETAS - COM BOTÃO LIMPAR"""
        filtro = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
        
        # Ocultar TODOS os botões
        self.btn_salvar.pack_forget()
        self.btn_novo.pack_forget()
        self.btn_limpar.pack_forget()
        self.btn_alterar.pack_forget()
        self.btn_excluir.pack_forget()
        self.btn_ativar_inativar.pack_forget()
        self.btn_exportar_ativos.pack_forget()
        self.btn_exportar_inativos.pack_forget()
        
        # APLICAR AS 4 REGRAS EXATAS
        if filtro == "todos":
            # 1ª REGRA: TODOS → APENAS NOVO + LIMPAR (como outras tabelas)
            self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_limpar.pack(side=tk.LEFT, padx=2, pady=10)
            print("✅ Filtro TODOS: Apenas NOVO e LIMPAR visíveis")
            
        elif filtro == "ativos":
            # 3ª REGRA: ATIVO → NOVO, LIMPAR, Alterar, Excluir, Inativar, Excel Ativos
            self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_limpar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_alterar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_excluir.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_ativar_inativar.config(text="🔴 Inativar", bg='#e0e0e0', fg='#333333')
            self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_exportar_ativos.pack(side=tk.LEFT, padx=2, pady=10)
            
        elif filtro == "inativos":
            # 4ª REGRA: INATIVO → NOVO, LIMPAR, Alterar, Excluir, ATIVAR, Excel Inativos (se houver)
            self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_limpar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_alterar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_excluir.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_ativar_inativar.config(text="✅ Ativar", bg='#e0e0e0', fg='#333333')
            self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
            # Controlar Excel Inativos baseado na existência de registros inativos
            self.controlar_botao_exportar_inativos()
            print("✅ Filtro INATIVOS: Botão Ativar configurado e Excel Inativos controlado")


    def tem_dados_digitados(self):
        """Verificar se há dados digitados nos campos principais"""
        # Verificar campos obrigatórios/principais
        campos_principais = [
            self.nome.get().strip(),
            self.email.get().strip()
        ]
        
        # Se qualquer campo principal tem dados, considerar como "dados digitados"
        return any(campo for campo in campos_principais)
    
    def aplicar_regras_botoes_sem_dados(self):
        """REGRA GERAL SIMPLES: ATIVO = APENAS BOTÃO NOVO"""
        filtro = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
        
        # Ocultar todos os botões primeiro
        self.btn_novo.pack_forget()
        self.btn_alterar.pack_forget()
        self.btn_excluir.pack_forget()
        self.btn_ativar_inativar.pack_forget()
        self.btn_exportar_ativos.pack_forget()
        self.btn_exportar_inativos.pack_forget()
        
        if filtro == "ativos":
            # REGRA GERAL: ATIVO = APENAS BOTÃO NOVO
            self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
            
        elif filtro == "todos":
            # TODOS - Somente botão NOVO visível
            self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
            
        elif filtro == "inativos":
            # INATIVOS - Verificar se há registros inativos
            if self.tem_registros_inativos():
                # HÁ INATIVOS: NOVO, Alterar, Excluir, ATIVAR, Excel Inativos
                self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_alterar.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_excluir.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_ativar_inativar.config(text="✅ Ativar", bg='#e0e0e0', fg='#333333')
                self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_exportar_inativos.pack(side=tk.LEFT, padx=2, pady=10)
            else:
                # NÃO HÁ INATIVOS: Voltar automaticamente para ATIVOS
                self.filtro_status.set("ativos")
                self.carregar_clientes()
                # Aplicar REGRA GERAL (ATIVO = APENAS NOVO)
                self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
    
    def carregar_clientes(self):
        """Carregar lista de funcionários baseado no filtro de status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Determinar filtro baseado na seleção
            filtro = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
            
            if filtro == "ativos":
                where_clause = "WHERE ativo = 1"
            elif filtro == "inativos":
                where_clause = "WHERE ativo = 0"
            else:  # todos
                where_clause = ""
            
            cursor.execute(f"""
                SELECT id, nome, ativo FROM clientes 
                {where_clause}
                ORDER BY nome
            """)
            
            clientes = cursor.fetchall()
            
            # Limpar listbox
            self.listbox.delete(0, tk.END)
            
            # Adicionar clientes à lista
            self.clientes_ids = []
            for cliente in clientes:
                nome = cliente[1]
                ativo = cliente[2]
                
                # Indicador visual para status
                status_icon = "✅" if ativo else "❌"
                display_text = f"{status_icon} {nome}"
                
                self.listbox.insert(tk.END, display_text)
                self.clientes_ids.append(cliente[0])
            
            # Atualizar total de clientes exibidos
            self.atualizar_total_clientes(len(clientes))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar funcionários: {e}", parent=self.window)
            self.atualizar_total_clientes(0)
        finally:
            if conn:
                conn.close()
    
    def filtrar_lista(self, event=None):
        """Filtrar lista baseado na busca rápida e status"""
        termo = self.busca_rapida.get().lower() if hasattr(self, 'busca_rapida') else ""
        filtro = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Construir WHERE clause
            where_conditions = []
            params = []
            
            # Filtro de status
            if filtro == "ativos":
                where_conditions.append("ativo = 1")
            elif filtro == "inativos":
                where_conditions.append("ativo = 0")
            # Se "todos", não adiciona condição de ativo
            
            # Filtro de busca
            if termo:
                where_conditions.append("(LOWER(nome) LIKE ? OR LOWER(email) LIKE ?)")
                params.extend([f"%{termo}%", f"%{termo}%"])
            
            # Montar query
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            cursor.execute(f"""
                SELECT id, nome, ativo FROM clientes 
                {where_clause}
                ORDER BY nome
            """, params)
            
            clientes = cursor.fetchall()
            
            # Limpar e recarregar listbox
            self.listbox.delete(0, tk.END)
            self.clientes_ids = []
            
            for cliente in clientes:
                nome = cliente[1]
                ativo = cliente[2]
                
                # Indicador visual para status
                status_icon = "✅" if ativo else "❌"
                display_text = f"{status_icon} {nome}"
                
                self.listbox.insert(tk.END, display_text)
                self.clientes_ids.append(cliente[0])
            
            # Atualizar total de clientes exibidos
            self.atualizar_total_clientes(len(clientes))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar: {e}", parent=self.window)
            self.atualizar_total_clientes(0)
        finally:
            if conn:
                conn.close()
    
    def cliente_selecionado(self, event=None):
        """Quando um funcionário é selecionado na lista"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index >= len(self.clientes_ids):
            return
        
        cliente_id = self.clientes_ids[index]
        self.cliente_selecionado_id = cliente_id
        
        # Carregar dados do funcionário
        self.carregar_dados_cliente(cliente_id)
        
        # Controlar botões (mostrar Alterar/Excluir/Inativar quando selecionado)
        self.controlar_botoes()
    
    def carregar_dados_cliente(self, cliente_id):
        """Carregar dados do funcionário selecionado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT nome, ativo, email, telefone, celular, fax, endereco, cidade, uf, cep, anotacoes FROM clientes 
                WHERE id = ?
            """, (cliente_id,))
            
            result = cursor.fetchone()
            
            if result:
                # Preencher campos
                self.nome.set(result[0] or "")
                self.ativo.set(bool(result[1]))
                self.email.set(result[2] or "")
                self.telefone.set(result[3] or "")
                self.celular.set(result[4] or "")
                self.fax.set(result[5] or "")
                self.endereco.set(result[6] or "")
                self.cidade.set(result[7] or "")
                self.uf.set(result[8] or "")
                self.cep.set(result[9] or "")
                self.anotacoes.set(result[10] or "")
                self.codigo.set(str(cliente_id))
                
                # Carregar anotações no widget Text
                if hasattr(self, 'text_anotacoes'):
                    self.text_anotacoes.delete("1.0", tk.END)
                    self.text_anotacoes.insert("1.0", result[10] or "")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def novo_cliente(self):
        """Limpar campos para novo cliente"""
        self.cliente_selecionado_id = None
        
        # Limpar todos os campos
        self.nome.set("")
        self.email.set("")
        self.telefone.set("")
        self.celular.set("")
        self.fax.set("")
        self.endereco.set("")
        self.cidade.set("")
        self.uf.set("")
        self.cep.set("")
        self.anotacoes.set("")
        self.ativo.set(True)
        
        # Limpar text widget de anotações
        if hasattr(self, 'text_anotacoes'):
            self.text_anotacoes.delete("1.0", tk.END)
        
        # Gerar novo código
        self.gerar_proximo_codigo()
        
        # Limpar seleção da lista
        self.listbox.selection_clear(0, tk.END)
        
        # Controlar botões (resetar para estado inicial - apenas NOVO visível)
        self.controlar_botoes()
        
        # FOCO NO PRIMEIRO CAMPO
        if hasattr(self, 'entry_nome'):
            self.entry_nome.focus_set()
    
    def gerar_proximo_codigo(self):
        """Gerar próximo código disponível"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(id) FROM clientes")
            result = cursor.fetchone()
            proximo_codigo = (result[0] or 0) + 1
            
            self.codigo.set(str(proximo_codigo))
            
        except Exception as e:
            self.codigo.set("1")
        finally:
            if conn:
                conn.close()
    
    def salvar_cliente(self):
        """Salvar ou atualizar cliente"""
        # Verificar permissões
        if self.cliente_selecionado_id:
            # Alteração
            if self.bloquear_acao_sem_permissao('alteracao', 'alterar clientes'):
                return
        else:
            # Inclusão
            if self.bloquear_acao_sem_permissao('inclusao', 'cadastrar novos clientes'):
                return
        
        # Validações
        if not self.nome.get().strip():
            messagebox.showerror("Erro", "Nome é obrigatório", parent=self.window)
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Capturar anotações do widget Text
            anotacoes_texto = ""
            if hasattr(self, 'text_anotacoes'):
                anotacoes_texto = self.text_anotacoes.get("1.0", tk.END).strip()
            
            if self.cliente_selecionado_id:
                # Atualizar cliente existente - COM LIMPEZA DE CARACTERES ESPECIAIS
                cursor.execute("""
                    UPDATE clientes SET
                    nome = ?, ativo = ?, email = ?, telefone = ?, celular = ?, fax = ?, endereco = ?, cidade = ?, uf = ?, cep = ?, anotacoes = ?
                    WHERE id = ?
                """, (
                    limpar_caracteres_especiais(self.nome.get()),
                    1 if self.ativo.get() else 0,
                    limpar_caracteres_especiais(self.email.get()),
                    limpar_caracteres_especiais(self.telefone.get()),
                    limpar_caracteres_especiais(self.celular.get()),
                    limpar_caracteres_especiais(self.fax.get()),
                    limpar_caracteres_especiais(self.endereco.get()),
                    limpar_caracteres_especiais(self.cidade.get()),
                    limpar_caracteres_especiais(self.uf.get()),
                    limpar_caracteres_especiais(self.cep.get()),
                    limpar_caracteres_especiais(anotacoes_texto),
                    self.cliente_selecionado_id
                ))
                
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!", parent=self.window)
            else:
                # Inserir novo cliente - COM LIMPEZA DE CARACTERES ESPECIAIS
                cursor.execute("""
                    INSERT INTO clientes (nome, ativo, email, telefone, celular, fax, endereco, cidade, uf, cep, anotacoes, data_cadastro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    limpar_caracteres_especiais(self.nome.get()),
                    1 if self.ativo.get() else 0,
                    limpar_caracteres_especiais(self.email.get()),
                    limpar_caracteres_especiais(self.telefone.get()),
                    limpar_caracteres_especiais(self.celular.get()),
                    limpar_caracteres_especiais(self.fax.get()),
                    limpar_caracteres_especiais(self.endereco.get()),
                    limpar_caracteres_especiais(self.cidade.get()),
                    limpar_caracteres_especiais(self.uf.get()),
                    limpar_caracteres_especiais(self.cep.get()),
                    limpar_caracteres_especiais(anotacoes_texto)
                ))
                
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!", parent=self.window)
            
            conn.commit()
            
            # Recarregar lista
            self.carregar_clientes()
            
            # Limpar campos automaticamente após salvar
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def excluir_cliente(self):
        """Excluir funcionário selecionado"""
        # Verificar permissão de exclusão
        if self.bloquear_acao_sem_permissao('exclusao', 'excluir clientes'):
            return
            
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir", parent=self.window)
            return
        
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este funcionário?", parent=self.window):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM clientes WHERE id = ?", 
                              (self.cliente_selecionado_id,))
                conn.commit()
                
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!", parent=self.window)
                
                # Limpar campos e recarregar lista
                self.novo_cliente()
                self.carregar_clientes()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir funcionário: {e}", parent=self.window)
            finally:
                if conn:
                    conn.close()
    
    def formatar_telefone(self, event=None):
        """Formatar telefone no padrão (11) 2554-3990"""
        widget = event.widget
        texto = widget.get()
        
        # Remover caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Aplicar formatação
        if len(numeros) <= 10:
            if len(numeros) >= 6:
                formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
            elif len(numeros) >= 2:
                formatado = f"({numeros[:2]}) {numeros[2:]}"
            else:
                formatado = numeros
        else:
            formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:10]}"
        
        # Atualizar campo sem triggerar evento novamente
        widget.delete(0, tk.END)
        widget.insert(0, formatado)
        
        # Posicionar cursor no final
        widget.icursor(tk.END)
    
    def formatar_celular(self, event=None):
        """Formatar celular no padrão (11) 9-4576-0912"""
        widget = event.widget
        texto = widget.get()
        
        # Remover caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Aplicar formatação para celular
        if len(numeros) <= 11:
            if len(numeros) >= 7:
                if len(numeros) == 11:  # Celular com 9 dígitos
                    formatado = f"({numeros[:2]}) {numeros[2]}-{numeros[3:7]}-{numeros[7:]}"
                else:
                    formatado = f"({numeros[:2]}) {numeros[2:3]}-{numeros[3:7]}-{numeros[7:]}"
            elif len(numeros) >= 3:
                formatado = f"({numeros[:2]}) {numeros[2:]}"
            elif len(numeros) >= 2:
                formatado = f"({numeros[:2]}) {numeros[2:]}"
            else:
                formatado = numeros
        else:
            formatado = f"({numeros[:2]}) {numeros[2]}-{numeros[3:7]}-{numeros[7:11]}"
        
        # Atualizar campo
        widget.delete(0, tk.END)
        widget.insert(0, formatado)
        widget.icursor(tk.END)
    
    def formatar_fax(self, event=None):
        """Formatar fax no padrão (11) 2554-3990"""
        widget = event.widget
        texto = widget.get()
        
        # Remover caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Aplicar formatação (mesmo padrão do telefone)
        if len(numeros) <= 10:
            if len(numeros) >= 6:
                formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
            elif len(numeros) >= 2:
                formatado = f"({numeros[:2]}) {numeros[2:]}"
            else:
                formatado = numeros
        else:
            formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:10]}"
        
        # Atualizar campo sem triggerar evento novamente
        widget.delete(0, tk.END)
        widget.insert(0, formatado)
        
        # Posicionar cursor no final
        widget.icursor(tk.END)
    
    def formatar_cep(self, event=None):
        """Formatar CEP no padrão 08.460-526"""
        widget = event.widget
        texto = widget.get()
        
        # Remover caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Aplicar formatação
        if len(numeros) >= 5:
            formatado = f"{numeros[:2]}.{numeros[2:5]}-{numeros[5:8]}"
        elif len(numeros) >= 2:
            formatado = f"{numeros[:2]}.{numeros[2:]}"
        else:
            formatado = numeros
        
        # Atualizar campo
        widget.delete(0, tk.END)
        widget.insert(0, formatado)
        widget.icursor(tk.END)
    
    def buscar_endereco_por_cep(self, event=None):
        """Buscar endereço automaticamente pelo CEP"""
        cep = self.cep.get()
        
        # Remover formatação do CEP
        cep_numeros = ''.join(filter(str.isdigit, cep))
        
        if len(cep_numeros) != 8:
            return
        
        try:
            import requests
            
            # Fazer requisição para API do ViaCEP com timeout maior
            url = f"https://viacep.com.br/ws/{cep_numeros}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                
                if 'erro' not in dados:
                    # Preencher campos automaticamente
                    if dados.get('logradouro'):
                        self.endereco.set(f"{dados['logradouro']}, ")
                    
                    if dados.get('localidade'):
                        self.cidade.set(dados['localidade'])
                    
                    if dados.get('uf'):
                        self.uf.set(dados['uf'])
                    
                    messagebox.showinfo("CEP", "Endereço encontrado e preenchido automaticamente!", parent=self.window)
                else:
                    self.mostrar_imagem_nao_localizado()
            else:
                self.mostrar_imagem_nao_localizado()
            
        except ImportError:
            messagebox.showwarning("Aviso", "Biblioteca 'requests' não encontrada. Instale com: pip install requests", parent=self.window)
        except Exception as e:
            self.mostrar_imagem_nao_localizado()
    
    def mostrar_imagem_nao_localizado(self):
        """Mostrar mensagem de CEP não localizado"""
        from tkinter import messagebox
        messagebox.showwarning("CEP", "CEP não localizado", parent=self.window)
    
    def limpar_campos(self):
        """Limpar todos os campos para novo cadastro"""
        self.cliente_selecionado_id = None
        self.nome.set("")
        self.codigo.set("")
        self.email.set("")
        self.telefone.set("")
        self.celular.set("")
        self.fax.set("")
        self.endereco.set("")
        self.cidade.set("")
        self.uf.set("")
        self.cep.set("")
        self.anotacoes.set("")
        self.ativo.set(True)
        
        # Limpar text widget de anotações
        if hasattr(self, 'text_anotacoes'):
            self.text_anotacoes.delete("1.0", tk.END)
        
        # REGRA 2: Quando NOVO clicado, mudar automaticamente para "ATIVO"
        if hasattr(self, 'filtro_status'):
            self.filtro_status.set("ativos")
            # Recarregar lista com filtro ativo
            self.carregar_clientes()
            # APLICAR REGRA 3 DIRETAMENTE
            self.aplicar_regra_3_ativos()
        
        # Controlar botões
        self.controlar_botoes()
        
        # Limpar seleção da lista
        if hasattr(self, 'listbox'):
            self.listbox.selection_clear(0, tk.END)
        
        # Gerar próximo código
        self.gerar_proximo_codigo()
    
    def aplicar_regra_3_ativos(self):
        """REGRA GERAL: ATIVO = APENAS BOTÃO NOVO"""
        # Ocultar todos os botões primeiro
        self.btn_novo.pack_forget()
        self.btn_alterar.pack_forget()
        self.btn_excluir.pack_forget()
        self.btn_ativar_inativar.pack_forget()
        self.btn_exportar_ativos.pack_forget()
        self.btn_exportar_inativos.pack_forget()
        self.btn_salvar.pack_forget()
        
        # Aplicar REGRA GERAL: ATIVO = APENAS NOVO
        self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
    
    def exportar_excel(self):
        """Exportar funcionários para Excel"""
        # Verificar permissão de exportação
        if self.bloquear_acao_sem_permissao('controle_especial_2', 'exportar para Excel'):
            return
            
        try:
            from exportacao_excel_formatada import ExportacaoExcelFormatada
            
            conn = sqlite3.connect(self.db_path)
            
            # Query para buscar todos os funcionários
            query = '''
                SELECT 
                    codigo as "ID",
                    nome as "Nome",
                    cpf as "CPF",
                    cargo as "Cargo",
                    setor as "Setor",
                    email as "E-mail",
                    fone_comercial as "Fone Comercial",
                    fone_celular as "Celular",
                    endereco as "Endereço",
                    cidade as "Cidade",
                    uf as "UF",
                    cep as "CEP",
                    CASE WHEN ativo = 1 THEN 'Ativo' ELSE 'Inativo' END as "Status"
                FROM clientes 
                ORDER BY nome
            '''
            
            # Usar a classe de exportação formatada
            exportador = ExportacaoExcelFormatada()
            arquivo = exportador.exportar_consulta_sql(
                conn, 
                query, 
                nome_arquivo="clientes_cadastrados",
                titulo_relatorio="RELATÓRIO DE FUNCIONÁRIOS CADASTRADOS"
            )
            
            conn.close()
            
            if arquivo:
                messagebox.showinfo("Sucesso", f"Funcionários exportados para:\n{arquivo}", parent=self.window)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def controlar_botao_ativar_inativar(self):
        """Controlar aparência do botão Ativar/Inativar baseado no status do funcionário"""
        if not self.cliente_selecionado_id:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT ativo FROM clientes WHERE id = ?", (self.cliente_selecionado_id,))
            result = cursor.fetchone()
            
            if result:
                ativo = result[0]
                
                if ativo:
                    # Funcionário ativo - mostrar botão para inativar
                    self.btn_ativar_inativar.config(
                        text="🔴 Inativar",
                        bg='#e0e0e0',  # Fundo padrão
                        fg='#333333'
                    )
                else:
                    # Funcionário inativo - mostrar botão para ativar
                    self.btn_ativar_inativar.config(
                        text="✅ Ativar",
                        bg='#e0e0e0',  # Fundo padrão
                        fg='#333333'
                    )
                
                # Mostrar o botão alinhado
                self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
            
        except Exception as e:
            print(f"Erro ao controlar botão ativar/inativar: {e}")
        finally:
            if conn:
                conn.close()
    
    def ativar_inativar_cliente(self):
        """Ativar ou inativar funcionário selecionado"""
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para ativar/inativar", parent=self.window)
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar status atual
            cursor.execute("SELECT ativo, nome FROM clientes WHERE id = ?", (self.cliente_selecionado_id,))
            result = cursor.fetchone()
            
            if result:
                ativo_atual = result[0]
                nome = result[1]
                
                # Inverter status
                novo_status = 0 if ativo_atual else 1
                acao = "ativar" if novo_status else "inativar"
                
                if messagebox.askyesno("Confirmação", f"Deseja realmente {acao} o funcionário '{nome}'?", parent=self.window):
                    cursor.execute("UPDATE clientes SET ativo = ? WHERE id = ?", 
                                 (novo_status, self.cliente_selecionado_id))
                    conn.commit()
                    
                    # Registrar no histórico
                    acao_historico = "ATIVADO" if novo_status else "INATIVADO"
                    self.registrar_historico_ativacao(
                        self.cliente_selecionado_id, 
                        nome, 
                        acao_historico, 
                        ativo_atual, 
                        novo_status
                    )
                    
                    status_msg = "ativado" if novo_status else "inativado"
                    messagebox.showinfo("Sucesso", f"Funcionário {status_msg} com sucesso!\nRegistro salvo no histórico.", parent=self.window)
                    
                    # Recarregar lista e controlar botões
                    self.carregar_clientes()
                    self.controlar_botoes()
                    self.controlar_botao_exportar_inativos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar/inativar funcionário: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def registrar_historico_ativacao(self, cliente_id, nome, acao, status_anterior, status_novo):
        """Registrar ação no histórico de ativação"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO historico_ativacao 
                (tabela, registro_id, registro_nome, acao, status_anterior, status_novo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("clientes", str(cliente_id), nome, acao, status_anterior, status_novo))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao registrar histórico: {e}")
        finally:
            if conn:
                conn.close()
    
    def filtrar_lista_e_controlar_exportacao(self):
        """Filtrar clientes e controlar botão de exportação"""
        self.filtrar_lista()
        # IMPORTANTE: Sempre chamar controlar_botoes quando filtro muda
        self.controlar_botoes()
    
    def controlar_botao_exportar_inativos(self):
        """Controlar visibilidade dos botões de exportação"""
        filtro = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
        
        if filtro == "inativos":
            # Mostrar botão Excel Inativos (roxo)
            self.btn_exportar_inativos.pack(side=tk.LEFT, padx=1, pady=10)
            # Ocultar botão Excel Ativos
            self.btn_exportar_ativos.pack_forget()
        elif filtro == "ativos":
            # Mostrar botão Excel Ativos (verde)
            self.btn_exportar_ativos.pack(side=tk.LEFT, padx=1, pady=10)
            # Ocultar botão Excel Inativos
            self.btn_exportar_inativos.pack_forget()
        else:
            # Ocultar ambos os botões quando visualizando "todos"
            self.btn_exportar_inativos.pack_forget()
            self.btn_exportar_ativos.pack_forget()
    
    def exportar_inativos_excel(self):
        """Exportar clientes inativos para Excel com formatação profissional"""
        # Verificar permissão de exportação
        if self.bloquear_acao_sem_permissao('controle_especial_2', 'exportar para Excel'):
            return
            
        try:
            from datetime import datetime
            from tkinter import filedialog
            from formatacao_relatorios_universal import FormatacaoUniversal
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query para buscar clientes inativos
            query = """
                SELECT 
                    id,
                    nome,
                    email,
                    telefone,
                    celular,
                    fax,
                    endereco,
                    cidade,
                    uf,
                    cep,
                    anotacoes
                FROM clientes 
                WHERE ativo = 0
                ORDER BY nome
            """
            
            cursor.execute(query)
            dados = cursor.fetchall()
            
            if not dados:
                messagebox.showinfo("Aviso", "Não há clientes inativos para exportar", parent=self.window)
                conn.close()
                return
            
            # Nome do arquivo com data/hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Clientes Inativos",
                initialfile=f"clientes_inativos_{timestamp}.xlsx"
            )
            
            if not nome_arquivo:
                conn.close()
                return
            
            # Usar formatação universal
            colunas = ["ID", "Nome", "E-mail", "Telefone", "Celular", "Fax",
                      "Endereço", "Cidade", "UF", "CEP", "Anotações"]
            
            sucesso = FormatacaoUniversal.criar_excel_profissional(
                dados, 
                colunas, 
                nome_arquivo, 
                self.db_path, 
                "Clientes Inativos"
            )
            
            conn.close()
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"✅ RELATÓRIO PROFISSIONAL CRIADO!\n\nArquivo: {nome_arquivo}\nTotal de clientes: {len(dados, parent=self.window)}\n\n🎨 Formatação padrão aplicada!\n📋 Logo incluído!\n✍️ Campo de assinatura adicionado!")
            else:
                messagebox.showerror("Erro", "Erro ao criar relatório profissional!", parent=self.window)
            
        except ImportError:
            messagebox.showerror("Erro", "Módulo de formatação não encontrado!", parent=self.window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def exportar_ativos_excel(self):
        """Exportar clientes ativos para Excel com formatação profissional"""
        # Verificar permissão de exportação
        if self.bloquear_acao_sem_permissao('controle_especial_2', 'exportar para Excel'):
            return
            
        try:
            from datetime import datetime
            from tkinter import filedialog
            from formatacao_relatorios_universal import FormatacaoUniversal
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query para buscar clientes ativos
            query = """
                SELECT 
                    id,
                    nome,
                    email,
                    telefone,
                    celular,
                    fax,
                    endereco,
                    cidade,
                    uf,
                    cep,
                    anotacoes
                FROM clientes 
                WHERE ativo = 1
                ORDER BY nome
            """
            
            cursor.execute(query)
            dados = cursor.fetchall()
            
            if not dados:
                messagebox.showinfo("Aviso", "Não há clientes ativos para exportar", parent=self.window)
                conn.close()
                return
            
            # Nome do arquivo com data/hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Clientes Ativos",
                initialfile=f"clientes_ativos_{timestamp}.xlsx"
            )
            
            if not nome_arquivo:
                conn.close()
                return
            
            # Usar formatação universal
            colunas = ["ID", "Nome", "E-mail", "Telefone", "Celular", "Fax",
                      "Endereço", "Cidade", "UF", "CEP", "Anotações"]
            
            sucesso = FormatacaoUniversal.criar_excel_profissional(
                dados, 
                colunas, 
                nome_arquivo, 
                self.db_path, 
                "Clientes Ativos"
            )
            
            conn.close()
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"✅ RELATÓRIO PROFISSIONAL CRIADO!\n\nArquivo: {nome_arquivo}\nTotal de clientes: {len(dados, parent=self.window)}\n\n🎨 Formatação padrão aplicada!\n📋 Logo incluído!\n✍️ Campo de assinatura adicionado!")
            else:
                messagebox.showerror("Erro", "Erro ao criar relatório profissional!", parent=self.window)
            
        except ImportError:
            messagebox.showerror("Erro", "Módulo de formatação não encontrado!", parent=self.window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def monitorar_campos(self, event=None):
        """Monitorar mudanças nos campos - LIMPAR SEMPRE VISÍVEL"""
        if self.tem_dados_digitados():
            # ALGO DIGITADO: Salvar + LIMPAR (sempre visível)
            self.btn_novo.pack_forget()
            self.btn_alterar.pack_forget()
            self.btn_excluir.pack_forget()
            self.btn_ativar_inativar.pack_forget()
            self.btn_exportar_ativos.pack_forget()
            self.btn_exportar_inativos.pack_forget()
            self.btn_salvar.pack(side=tk.LEFT, padx=2, pady=10)
            self.btn_limpar.pack(side=tk.LEFT, padx=2, pady=10)  # LIMPAR SEMPRE VISÍVEL
        else:
            # NADA DIGITADO: Aplicar regras dos botões
            self.btn_salvar.pack_forget()
            self.controlar_botoes()
    
    def tem_registros_inativos(self):
        """Verificar se há registros inativos na tabela"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE ativo = 0")
            count = cursor.fetchone()[0]
            return count > 0
        except:
            return False
        finally:
            if conn:
                conn.close()
    
    def atualizar_total_clientes(self, total=None):
        """Atualizar o total de clientes cadastrados"""
        try:
            if total is None:
                # Contar baseado no filtro atual
                filtro_status = self.filtro_status.get() if hasattr(self, 'filtro_status') else "ativos"
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                if filtro_status == "ativos":
                    cursor.execute("SELECT COUNT(*) FROM clientes WHERE ativo = 1")
                elif filtro_status == "inativos":
                    cursor.execute("SELECT COUNT(*) FROM clientes WHERE ativo = 0")
                else:  # todos
                    cursor.execute("SELECT COUNT(*) FROM clientes")
                
                total = cursor.fetchone()[0]
                conn.close()
            
            self.label_total_clientes.config(text=str(total))
        except Exception as e:
            print(f"Erro ao contar clientes: {e}")
            self.label_total_clientes.config(text="0")
    
    def fechar_janela(self):
        """Fechar janela e mostrar principal"""
        if self.window:
            self.window.destroy()
            self.window = None
        if self.parent:
            self.parent.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    cadastro = CadastroClientes(root, "estoque.db")
    cadastro.abrir()
    
    root.mainloop()
