#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cadastro de Funcionários - Layout conforme anexo
Com lista lateral e preenchimento dinâmico
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from limpeza_caracteres import limpar_caracteres_especiais

class CadastroFuncionarios:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.window = None
        self.funcionario_selecionado_id = None
        
        # Variáveis do formulário
        self.nome = tk.StringVar()
        self.codigo = tk.StringVar()
        self.cargo = tk.StringVar()
        self.email = tk.StringVar()
        self.telefone = tk.StringVar()
        self.celular = tk.StringVar()
        self.endereco = tk.StringVar()
        self.cidade = tk.StringVar()
        self.uf = tk.StringVar()
        self.cep = tk.StringVar()
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
        
    def abrir(self):
        """Abrir janela de cadastro de funcionários"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("Cadastro de Funcionários")
        self.window.geometry("750x450")
        
        # Bind da tecla ESC para fechar apenas esta janela
        self.window.bind('<Escape>', lambda e: self.fechar_janela())
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 375
        y = (self.window.winfo_screenheight() // 2) - 225
        self.window.geometry(f'750x450+{x}+{y}')
        self.window.configure(bg='#f0f0f0')
        
        # Garantir que a janela tenha foco para capturar ESC
        self.window.focus_force()
        self.window.resizable(True, True)
        self.window.minsize(800, 500)
        
        self.criar_interface()
        self.carregar_funcionarios()
        self.gerar_proximo_codigo()
        
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
        self.btn_salvar.bind('<Button-1>', lambda e: self.salvar_funcionario())
        criar_hover_effect(self.btn_salvar)
        
        # Label Alterar (inicialmente oculto)
        self.btn_alterar = tk.Label(btn_frame, text="✏️ Alterar", font=('Arial', 9, 'bold'), 
                                   bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_alterar.bind('<Button-1>', lambda e: self.salvar_funcionario())
        criar_hover_effect(self.btn_alterar)
        
        # Label Ativar/Inativar (dinâmico)
        self.btn_ativar_inativar = tk.Label(btn_frame, text="🔴 Inativar", font=('Arial', 9, 'bold'), 
                                           bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_ativar_inativar.pack(side=tk.LEFT, padx=8)
        self.btn_ativar_inativar.bind('<Button-1>', lambda e: self.ativar_inativar_funcionario())
        criar_hover_effect(self.btn_ativar_inativar)
        
        # Label Excluir (armazenar referência para controle)
        self.btn_excluir = tk.Label(btn_frame, text="🗑️ Excluir", font=('Arial', 9, 'bold'), 
                                   bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_excluir.bind('<Button-1>', lambda e: self.excluir_funcionario())
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
        self.btn_novo.bind('<Button-1>', lambda e: self.novo_funcionario())
        criar_hover_effect(self.btn_novo)
        
        # Label LIMPAR
        self.btn_limpar = tk.Label(btn_frame, text="🧹 Limpar", font=('Arial', 9, 'bold'), 
                                  bg='#e0e0e0', fg='#333333', cursor='hand2')
        self.btn_limpar.pack(side=tk.LEFT, padx=8)
        self.btn_limpar.bind('<Button-1>', lambda e: self.novo_funcionario())
        criar_hover_effect(self.btn_limpar)
        
        # =================== ÁREA PRINCIPAL ===================
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # =================== LADO ESQUERDO - LISTA ===================
        left_frame = tk.Frame(main_frame, bg='#f0f0f0', width=380)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Busca Rápida
        busca_frame = tk.Frame(left_frame, bg='#f0f0f0')
        busca_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(busca_frame, text="🔍 Busca Rápida", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        
        self.entry_busca = tk.Entry(busca_frame, textvariable=self.busca_rapida, 
                                   font=('Arial', 10), width=25)
        self.entry_busca.pack(fill=tk.X, pady=5)
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
        
        # Campo Total de Cadastrados
        total_frame = tk.Frame(busca_frame, bg='#f0f0f0')
        total_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(total_frame, text="Total de Cadastrados:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(side=tk.LEFT)
        self.label_total_cadastrados = tk.Label(total_frame, text="0", font=('Arial', 10, 'bold'), 
                                               bg='#e9ecef', fg='#2c3e50', width=8, relief=tk.SUNKEN)
        self.label_total_cadastrados.pack(side=tk.LEFT, padx=(5, 0))
        
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
        self.listbox.bind('<<ListboxSelect>>', self.funcionario_selecionado)
        
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
                             width=22)
        entry_nome.pack(side=tk.LEFT, padx=(0, 20))
        entry_nome.bind('<KeyRelease>', self.monitorar_campos)
        
        tk.Label(linha1, text="ID", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(side=tk.RIGHT, anchor='e')
        self.entry_codigo = tk.Entry(linha1, textvariable=self.codigo, font=('Arial', 10), 
                                    width=10, state='readonly', bg='#ffe6e6')
        self.entry_codigo.pack(side=tk.RIGHT)
        
        # LINHA 2: Cargo
        linha2 = tk.Frame(form_frame, bg='#f0f0f0')
        linha2.pack(fill=tk.X, pady=5)
        
        tk.Label(linha2, text="Cargo", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        
        # Combobox com cargos predefinidos
        cargos_predefinidos = ["Técnico", "Analista", "Supervisor", "Assistente", 
                              "Coordenador", "Gerente", "Operador", "Auxiliar"]
        self.combo_cargo = ttk.Combobox(linha2, textvariable=self.cargo, 
                                       values=cargos_predefinidos, font=('Arial', 10), width=22)
        self.combo_cargo.pack(anchor='w')
        self.combo_cargo.bind('<KeyRelease>', self.monitorar_campos)
        
        # LINHA 3: E-mail
        linha3 = tk.Frame(form_frame, bg='#f0f0f0')
        linha3.pack(fill=tk.X, pady=5)
        
        tk.Label(linha3, text="E-mail", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        entry_email = tk.Entry(linha3, textvariable=self.email, font=('Arial', 10), 
                width=22)
        entry_email.pack(anchor='w')
        entry_email.bind('<KeyRelease>', self.monitorar_campos)
        
        # LINHA 4: Telefones
        linha4 = tk.Frame(form_frame, bg='#f0f0f0')
        linha4.pack(fill=tk.X, pady=5)
        
        # Telefone
        tel_frame = tk.Frame(linha4, bg='#f0f0f0')
        tel_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(tel_frame, text="Telefone", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_telefone = tk.Entry(tel_frame, textvariable=self.telefone, font=('Arial', 10), 
                width=18)
        self.entry_telefone.pack()
        self.entry_telefone.bind('<KeyRelease>', self.formatar_telefone)
        
        # Celular
        cel_frame = tk.Frame(linha4, bg='#f0f0f0')
        cel_frame.pack(side=tk.LEFT)
        tk.Label(cel_frame, text="Celular", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.entry_celular = tk.Entry(cel_frame, textvariable=self.celular, font=('Arial', 10), 
                width=18)
        self.entry_celular.pack()
        self.entry_celular.bind('<KeyRelease>', self.formatar_celular)
        
        # LINHA 5: Endereço
        linha5 = tk.Frame(form_frame, bg='#f0f0f0')
        linha5.pack(fill=tk.X, pady=5)
        
        tk.Label(linha5, text="Endereço", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(linha5, textvariable=self.endereco, font=('Arial', 10), 
                width=22).pack(anchor='w')
        
        # LINHA 6: Cidade, UF, CEP
        linha6 = tk.Frame(form_frame, bg='#f0f0f0')
        linha6.pack(fill=tk.X, pady=5)
        
        # Cidade
        cidade_frame = tk.Frame(linha6, bg='#f0f0f0')
        cidade_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(cidade_frame, text="Cidade", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        tk.Entry(cidade_frame, textvariable=self.cidade, font=('Arial', 10), 
                width=20).pack()
        
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
                width=12)
        self.entry_cep.pack()
        self.entry_cep.bind('<KeyRelease>', self.formatar_cep)
        self.entry_cep.bind('<FocusOut>', self.buscar_endereco_por_cep)
        
        # LINHA 7: Status Ativo

        
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
            self.btn_ativar_inativar.pack(side=tk.LEFT, padx=8)
            self.btn_exportar_ativos.pack(side=tk.LEFT, padx=8)
            
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
            self.cargo.get().strip(),
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
                self.btn_ativar_inativar.config(text="✅ Ativar", bg='#28a745', fg='white')
                self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_exportar_inativos.pack(side=tk.LEFT, padx=2, pady=10)
            else:
                # NÃO HÁ INATIVOS: Voltar automaticamente para ATIVOS
                self.filtro_status.set("ativos")
                self.carregar_funcionarios()
                # Aplicar REGRA GERAL (ATIVO = APENAS NOVO)
                self.btn_novo.pack(side=tk.LEFT, padx=2, pady=10)
    
    def carregar_funcionarios(self):
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
                SELECT id, nome, cargo, ativo FROM funcionarios 
                {where_clause}
                ORDER BY nome
            """)
            
            funcionarios = cursor.fetchall()
            
            # Limpar listbox
            self.listbox.delete(0, tk.END)
            
            # Adicionar funcionários à lista
            self.funcionarios_ids = []
            for func in funcionarios:
                nome = func[1]
                ativo = func[3]
                
                # Indicador visual para status
                status_icon = "✅" if ativo else "❌"
                display_text = f"{status_icon} {nome}"
                
                self.listbox.insert(tk.END, display_text)
                self.funcionarios_ids.append(func[0])
            
            # Atualizar total de cadastrados
            total = len(funcionarios)
            if hasattr(self, 'label_total_cadastrados'):
                self.label_total_cadastrados.config(text=str(total))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar funcionários: {e}", parent=self.window)
            # Em caso de erro, zerar o total
            if hasattr(self, 'label_total_cadastrados'):
                self.label_total_cadastrados.config(text="0")
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
                where_conditions.append("(LOWER(nome) LIKE ? OR LOWER(cargo) LIKE ?)")
                params.extend([f"%{termo}%", f"%{termo}%"])
            
            # Montar query
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            cursor.execute(f"""
                SELECT id, nome, cargo, ativo FROM funcionarios 
                {where_clause}
                ORDER BY nome
            """, params)
            
            funcionarios = cursor.fetchall()
            
            # Limpar e recarregar listbox
            self.listbox.delete(0, tk.END)
            self.funcionarios_ids = []
            
            for func in funcionarios:
                nome = func[1]
                ativo = func[3]
                
                # Indicador visual para status
                status_icon = "✅" if ativo else "❌"
                display_text = f"{status_icon} {nome}"
                
                self.listbox.insert(tk.END, display_text)
                self.funcionarios_ids.append(func[0])
            
            # Atualizar total de cadastrados
            total = len(funcionarios)
            if hasattr(self, 'label_total_cadastrados'):
                self.label_total_cadastrados.config(text=str(total))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar: {e}", parent=self.window)
            # Em caso de erro, zerar o total
            if hasattr(self, 'label_total_cadastrados'):
                self.label_total_cadastrados.config(text="0")
        finally:
            if conn:
                conn.close()
    
    def funcionario_selecionado(self, event=None):
        """Quando um funcionário é selecionado na lista"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index >= len(self.funcionarios_ids):
            return
        
        funcionario_id = self.funcionarios_ids[index]
        self.funcionario_selecionado_id = funcionario_id
        
        # Carregar dados do funcionário
        self.carregar_dados_funcionario(funcionario_id)
        
        # Controlar botões (mostrar Alterar/Excluir/Inativar quando selecionado)
        self.controlar_botoes()
    
    def carregar_dados_funcionario(self, funcionario_id):
        """Carregar dados do funcionário selecionado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT nome, cargo, ativo, email, telefone, celular, endereco, cidade, uf, cep FROM funcionarios 
                WHERE id = ?
            """, (funcionario_id,))
            
            result = cursor.fetchone()
            
            if result:
                # Preencher campos
                self.nome.set(result[0] or "")
                self.cargo.set(result[1] or "")
                self.ativo.set(bool(result[2]))
                self.email.set(result[3] or "")
                self.telefone.set(result[4] or "")
                self.celular.set(result[5] or "")
                self.endereco.set(result[6] or "")
                self.cidade.set(result[7] or "")
                self.uf.set(result[8] or "")
                self.cep.set(result[9] or "")
                self.codigo.set(str(funcionario_id))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def novo_funcionario(self):
        """Limpar campos para novo funcionário"""
        self.funcionario_selecionado_id = None
        
        # Limpar todos os campos
        self.nome.set("")
        self.cargo.set("")
        self.email.set("")
        self.telefone.set("")
        self.celular.set("")
        self.endereco.set("")
        self.cidade.set("")
        self.uf.set("")
        self.cep.set("")
        self.ativo.set(True)
        
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
            
            cursor.execute("SELECT MAX(id) FROM funcionarios")
            result = cursor.fetchone()
            proximo_codigo = (result[0] or 0) + 1
            
            self.codigo.set(str(proximo_codigo))
            
        except Exception as e:
            self.codigo.set("1")
        finally:
            if conn:
                conn.close()
    
    def salvar_funcionario(self):
        """Salvar ou atualizar funcionário"""
        # Validações
        if not self.nome.get().strip():
            messagebox.showerror("Erro", "Nome é obrigatório", parent=self.window)
            return
        
        if not self.cargo.get().strip():
            messagebox.showerror("Erro", "Cargo é obrigatório", parent=self.window)
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if self.funcionario_selecionado_id:
                # Atualizar funcionário existente - COM LIMPEZA DE CARACTERES ESPECIAIS
                cursor.execute("""
                    UPDATE funcionarios SET
                    nome = ?, cargo = ?, ativo = ?, email = ?, telefone = ?, celular = ?, endereco = ?, cidade = ?, uf = ?, cep = ?
                    WHERE id = ?
                """, (
                    limpar_caracteres_especiais(self.nome.get()),
                    limpar_caracteres_especiais(self.cargo.get()),
                    1 if self.ativo.get() else 0,
                    limpar_caracteres_especiais(self.email.get()),
                    limpar_caracteres_especiais(self.telefone.get()),
                    limpar_caracteres_especiais(self.celular.get()),
                    limpar_caracteres_especiais(self.endereco.get()),
                    limpar_caracteres_especiais(self.cidade.get()),
                    limpar_caracteres_especiais(self.uf.get()),
                    limpar_caracteres_especiais(self.cep.get()),
                    self.funcionario_selecionado_id
                ))
                
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!", parent=self.window)
            else:
                # Inserir novo funcionário - COM LIMPEZA DE CARACTERES ESPECIAIS
                cursor.execute("""
                    INSERT INTO funcionarios (nome, cargo, ativo, email, telefone, celular, endereco, cidade, uf, cep, data_cadastro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    limpar_caracteres_especiais(self.nome.get()),
                    limpar_caracteres_especiais(self.cargo.get()),
                    1 if self.ativo.get() else 0,
                    limpar_caracteres_especiais(self.email.get()),
                    limpar_caracteres_especiais(self.telefone.get()),
                    limpar_caracteres_especiais(self.celular.get()),
                    limpar_caracteres_especiais(self.endereco.get()),
                    limpar_caracteres_especiais(self.cidade.get()),
                    limpar_caracteres_especiais(self.uf.get()),
                    limpar_caracteres_especiais(self.cep.get())
                ))
                
                messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!", parent=self.window)
            
            conn.commit()
            
            # Recarregar lista
            self.carregar_funcionarios()
            
            # Limpar campos automaticamente após salvar
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar funcionário: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def excluir_funcionario(self):
        """Excluir funcionário selecionado"""
        if not self.funcionario_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir", parent=self.window)
            return
        
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este funcionário?", parent=self.window):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM funcionarios WHERE id = ?", 
                              (self.funcionario_selecionado_id,))
                conn.commit()
                
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!", parent=self.window)
                
                # Limpar campos e recarregar lista
                self.novo_funcionario()
                self.carregar_funcionarios()
                
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
        self.funcionario_selecionado_id = None
        self.nome.set("")
        self.codigo.set("")
        self.cargo.set("")
        self.email.set("")
        self.telefone.set("")
        self.celular.set("")
        self.endereco.set("")
        self.cidade.set("")
        self.uf.set("")
        self.cep.set("")
        self.ativo.set(True)
        
        # REGRA 2: Quando NOVO clicado, mudar automaticamente para "ATIVO"
        if hasattr(self, 'filtro_status'):
            self.filtro_status.set("ativos")
            # Recarregar lista com filtro ativo
            self.carregar_funcionarios()
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
                FROM funcionarios 
                ORDER BY nome
            '''
            
            # Usar a classe de exportação formatada
            exportador = ExportacaoExcelFormatada()
            arquivo = exportador.exportar_consulta_sql(
                conn, 
                query, 
                nome_arquivo="funcionarios_cadastrados",
                titulo_relatorio="RELATÓRIO DE FUNCIONÁRIOS CADASTRADOS"
            )
            
            conn.close()
            
            if arquivo:
                messagebox.showinfo("Sucesso", f"Funcionários exportados para:\n{arquivo}", parent=self.window)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def controlar_botao_ativar_inativar(self):
        """Controlar aparência do botão Ativar/Inativar baseado no status do funcionário"""
        if not hasattr(self, 'funcionario_selecionado_id') or not self.funcionario_selecionado_id:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT ativo FROM funcionarios WHERE id = ?", (self.funcionario_selecionado_id,))
            result = cursor.fetchone()
            
            if result:
                ativo = result[0]
                
                if ativo:
                    # Funcionário ativo - mostrar texto para inativar (mantém padrão de label)
                    self.btn_ativar_inativar.config(
                        text="🔴 Inativar",
                        bg='#e0e0e0',  # Mantém fundo padrão
                        fg='#333333'   # Mantém cor padrão
                    )
                else:
                    # Funcionário inativo - mostrar texto para ativar (mantém padrão de label)
                    self.btn_ativar_inativar.config(
                        text="✅ Ativar",
                        bg='#e0e0e0',  # Mantém fundo padrão
                        fg='#333333'   # Mantém cor padrão
                    )
                
                # Mostrar o botão alinhado (verificar se já não está empacotado)
                try:
                    self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
                except tk.TclError:
                    # Botão já empacotado, apenas reconfigurar
                    pass
            
        except Exception as e:
            print(f"Erro ao controlar botão ativar/inativar: {e}")
        finally:
            if conn:
                conn.close()
    
    def ativar_inativar_funcionario(self):
        """Ativar ou inativar funcionário selecionado"""
        if not self.funcionario_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para ativar/inativar", parent=self.window)
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar status atual
            cursor.execute("SELECT ativo, nome FROM funcionarios WHERE id = ?", (self.funcionario_selecionado_id,))
            result = cursor.fetchone()
            
            if result:
                ativo_atual = result[0]
                nome = result[1]
                
                # Inverter status
                novo_status = 0 if ativo_atual else 1
                acao = "ativar" if novo_status else "inativar"
                
                if messagebox.askyesno("Confirmação", f"Deseja realmente {acao} o funcionário '{nome}'?", parent=self.window):
                    cursor.execute("UPDATE funcionarios SET ativo = ? WHERE id = ?", 
                                 (novo_status, self.funcionario_selecionado_id))
                    conn.commit()
                    
                    # Registrar no histórico
                    acao_historico = "ATIVADO" if novo_status else "INATIVADO"
                    self.registrar_historico_ativacao(
                        self.funcionario_selecionado_id, 
                        nome, 
                        acao_historico, 
                        ativo_atual, 
                        novo_status
                    )
                    
                    status_msg = "ativado" if novo_status else "inativado"
                    messagebox.showinfo("Sucesso", f"Funcionário {status_msg} com sucesso!\nRegistro salvo no histórico.", parent=self.window)
                    
                    # Recarregar lista e controlar botões
                    self.carregar_funcionarios()
                    self.controlar_botoes()
                    self.controlar_botao_exportar_inativos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar/inativar funcionário: {e}", parent=self.window)
        finally:
            if conn:
                conn.close()
    
    def registrar_historico_ativacao(self, funcionario_id, nome, acao, status_anterior, status_novo):
        """Registrar ação no histórico de ativação"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO historico_ativacao 
                (tabela, registro_id, registro_nome, acao, status_anterior, status_novo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("funcionarios", str(funcionario_id), nome, acao, status_anterior, status_novo))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao registrar histórico: {e}")
        finally:
            if conn:
                conn.close()
    
    def filtrar_lista_e_controlar_exportacao(self):
        """Filtrar funcionários e controlar botão de exportação"""
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
        """Exportar funcionários inativos para Excel com formatação profissional"""
        try:
            from datetime import datetime
            from tkinter import filedialog
            from formatacao_relatorios_universal import FormatacaoUniversal
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query para buscar funcionários inativos
            query = """
                SELECT 
                    id,
                    nome,
                    cargo,
                    email,
                    telefone,
                    celular,
                    endereco,
                    cidade,
                    uf,
                    cep
                FROM funcionarios 
                WHERE ativo = 0
                ORDER BY nome
            """
            
            cursor.execute(query)
            dados = cursor.fetchall()
            
            if not dados:
                messagebox.showinfo("Aviso", "Não há funcionários inativos para exportar", parent=self.window)
                conn.close()
                return
            
            # Solicitar local para salvar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Funcionários Inativos",
                initialfile=f"funcionarios_inativos_{timestamp}.xlsx"
            )
            
            if not nome_arquivo:
                conn.close()
                return
            
            # Usar formatação universal
            colunas = ["ID", "Nome", "Cargo", "E-mail", "Telefone", "Celular", 
                      "Endereço", "Cidade", "UF", "CEP"]
            
            sucesso = FormatacaoUniversal.criar_excel_profissional(
                dados, 
                colunas, 
                nome_arquivo, 
                self.db_path, 
                "Funcionários Inativos"
            )
            
            conn.close()
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"✅ RELATÓRIO PROFISSIONAL CRIADO!\n\nArquivo: {nome_arquivo}\nTotal de funcionários: {len(dados, parent=self.window)}\n\n🎨 Formatação padrão aplicada!\n📋 Logo incluído!\n✍️ Campo de assinatura adicionado!")
            else:
                messagebox.showerror("Erro", "Erro ao criar relatório profissional!", parent=self.window)
            
        except ImportError:
            messagebox.showerror("Erro", "Módulo de formatação não encontrado!", parent=self.window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def exportar_ativos_excel(self):
        """Exportar funcionários ativos para Excel com formatação profissional"""
        try:
            from datetime import datetime
            from tkinter import filedialog
            from formatacao_relatorios_universal import FormatacaoUniversal
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query para buscar funcionários ativos
            query = """
                SELECT 
                    id,
                    nome,
                    cargo,
                    email,
                    telefone,
                    celular,
                    endereco,
                    cidade,
                    uf,
                    cep
                FROM funcionarios 
                WHERE ativo = 1
                ORDER BY nome
            """
            
            cursor.execute(query)
            dados = cursor.fetchall()
            
            if not dados:
                messagebox.showinfo("Aviso", "Não há funcionários ativos para exportar", parent=self.window)
                conn.close()
                return
            
            # Solicitar local para salvar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Funcionários Ativos",
                initialfile=f"funcionarios_ativos_{timestamp}.xlsx"
            )
            
            if not nome_arquivo:
                conn.close()
                return
            
            # Usar formatação universal
            colunas = ["ID", "Nome", "Cargo", "E-mail", "Telefone", "Celular", 
                      "Endereço", "Cidade", "UF", "CEP"]
            
            sucesso = FormatacaoUniversal.criar_excel_profissional(
                dados, 
                colunas, 
                nome_arquivo, 
                self.db_path, 
                "Funcionários Ativos"
            )
            
            conn.close()
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"✅ RELATÓRIO PROFISSIONAL CRIADO!\n\nArquivo: {nome_arquivo}\nTotal de funcionários: {len(dados, parent=self.window)}\n\n🎨 Formatação padrão aplicada!\n📋 Logo incluído!\n✍️ Campo de assinatura adicionado!")
            else:
                messagebox.showerror("Erro", "Erro ao criar relatório profissional!", parent=self.window)
            
        except ImportError:
            messagebox.showerror("Erro", "Módulo de formatação não encontrado!", parent=self.window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}", parent=self.window)
    
    def monitorar_campos(self, event=None):
        """Monitorar mudanças nos campos - CORRIGIDO PARA MOSTRAR BOTÕES DE ALTERAÇÃO"""
        if self.tem_dados_digitados():
            # ALGO DIGITADO
            if hasattr(self, 'funcionario_selecionado_id') and self.funcionario_selecionado_id:
                # FUNCIONÁRIO SELECIONADO + DADOS DIGITADOS = BOTÕES DE ALTERAÇÃO
                self.btn_novo.pack_forget()
                self.btn_salvar.pack_forget()
                self.btn_exportar_ativos.pack_forget()
                self.btn_exportar_inativos.pack_forget()
                
                # Mostrar botões de alteração
                self.btn_limpar.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_alterar.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_excluir.pack(side=tk.LEFT, padx=2, pady=10)
                self.btn_ativar_inativar.pack(side=tk.LEFT, padx=2, pady=10)
                
                # Configurar botão Ativar/Inativar baseado no status
                self.controlar_botao_ativar_inativar()
            else:
                # SEM FUNCIONÁRIO SELECIONADO + DADOS DIGITADOS = SALVAR + LIMPAR
                self.btn_novo.pack_forget()
                self.btn_alterar.pack_forget()
                self.btn_excluir.pack_forget()
                self.btn_ativar_inativar.pack_forget()
                self.btn_exportar_ativos.pack_forget()
                self.btn_exportar_inativos.pack_forget()
                self.btn_salvar.pack(side=tk.LEFT, padx=8)
                self.btn_limpar.pack(side=tk.LEFT, padx=8)
        else:
            # NADA DIGITADO: Aplicar regras dos botões
            self.btn_salvar.pack_forget()
            self.controlar_botoes()
    
    def tem_registros_inativos(self):
        """Verificar se há registros inativos na tabela"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM funcionarios WHERE ativo = 0")
            count = cursor.fetchone()[0]
            return count > 0
        except:
            return False
        finally:
            if conn:
                conn.close()
    
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
    
    cadastro = CadastroFuncionarios(root, "estoque.db")
    cadastro.abrir()
    
    root.mainloop()