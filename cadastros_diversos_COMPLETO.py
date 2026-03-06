import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class CadastrosDiversos:
    def __init__(self, parent, db_path, callback_sincronizacao=None):
        self.parent = parent
        self.db_path = db_path
        self.window = None
        self.callback_sincronizacao = callback_sincronizacao
        
    def abrir(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("CADASTROS DIVERSOS")
        self.window.geometry("800x500")
        
        # Bind da tecla ESC para fechar apenas esta janela
        self.window.bind('<Escape>', lambda e: self.fechar_janela())
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 400
        y = (self.window.winfo_screenheight() // 2) - 250
        self.window.geometry(f'800x500+{x}+{y}')
        self.window.configure(bg='#e8e8e8')
        self.window.resizable(True, True)
        self.window.minsize(700, 400)
        
        self.window.focus_set()
        
        # =================== BARRA DE LABELS CLICÁVEIS ===================
        toolbar_frame = tk.Frame(self.window, bg='#e0e0e0', height=30)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        toolbar_frame.pack_propagate(False)
        
        # Labels clicáveis removidos conforme solicitado
        
        # SEÇÃO UNIDADES
        tk.Label(self.window, text="Cadastro de Unidades", font=('Arial', 12, 'bold'),
                bg='#e8e8e8').place(x=20, y=30)
        
        self.entry1 = tk.Entry(self.window, font=('Arial', 11), bg='white')
        self.entry1.place(x=20, y=60, width=200, height=25)
        
        tk.Button(self.window, text="📋 Vários", font=('Arial', 9, 'bold'),
                 bg='#90EE90', width=10, command=lambda: self.cadastrar_varios(1)).place(x=240, y=58)
        
        tk.Button(self.window, text="📝 Cadastrar", font=('Arial', 10, 'bold'),
                 bg='#ffff80', width=10, command=lambda: self.cadastrar(1)).place(x=240, y=85)
        
        self.lista1 = tk.Listbox(self.window, font=('Arial', 10))
        self.lista1.place(x=20, y=120, width=320, height=120)
        self.lista1.bind('<Double-Button-1>', lambda e: self.duplo_clique(1))
        
        # SEÇÃO MARCAS
        tk.Label(self.window, text="Cadastro de Marcas", font=('Arial', 12, 'bold'),
                bg='#e8e8e8').place(x=420, y=30)
        
        self.entry2 = tk.Entry(self.window, font=('Arial', 11), bg='white')
        self.entry2.place(x=420, y=60, width=200, height=25)
        
        tk.Button(self.window, text="📋 Vários", font=('Arial', 9, 'bold'),
                 bg='#90EE90', width=10, command=lambda: self.cadastrar_varios(2)).place(x=640, y=58)
        
        tk.Button(self.window, text="📝 Cadastrar", font=('Arial', 10, 'bold'),
                 bg='#ffff80', width=10, command=lambda: self.cadastrar(2)).place(x=640, y=85)
        
        self.lista2 = tk.Listbox(self.window, font=('Arial', 10))
        self.lista2.place(x=420, y=120, width=320, height=120)
        self.lista2.bind('<Double-Button-1>', lambda e: self.duplo_clique(2))
        
        # SEÇÃO CATEGORIAS
        tk.Label(self.window, text="Cadastro de Categorias", font=('Arial', 12, 'bold'),
                bg='#e8e8e8').place(x=20, y=260)
        
        self.entry3 = tk.Entry(self.window, font=('Arial', 11), bg='white')
        self.entry3.place(x=20, y=290, width=200, height=25)
        
        tk.Button(self.window, text="📋 Vários", font=('Arial', 9, 'bold'),
                 bg='#90EE90', width=10, command=lambda: self.cadastrar_varios(3)).place(x=240, y=288)
        
        tk.Button(self.window, text="📝 Cadastrar", font=('Arial', 10, 'bold'),
                 bg='#ffff80', width=10, command=lambda: self.cadastrar(3)).place(x=240, y=315)
        
        self.lista3 = tk.Listbox(self.window, font=('Arial', 10))
        self.lista3.place(x=20, y=350, width=320, height=120)
        self.lista3.bind('<Double-Button-1>', lambda e: self.duplo_clique(3))
        
        # SEÇÃO OPERAÇÕES
        tk.Label(self.window, text="Cadastro de Operações", font=('Arial', 12, 'bold'),
                bg='#e8e8e8').place(x=420, y=260)
        
        self.entry4 = tk.Entry(self.window, font=('Arial', 11), bg='white')
        self.entry4.place(x=420, y=290, width=200, height=25)
        
        tk.Button(self.window, text="📋 Vários", font=('Arial', 9, 'bold'),
                 bg='#90EE90', width=10, command=lambda: self.cadastrar_varios(4)).place(x=640, y=288)
        
        tk.Button(self.window, text="📝 Cadastrar", font=('Arial', 10, 'bold'),
                 bg='#ffff80', width=10, command=lambda: self.cadastrar(4)).place(x=640, y=315)
        
        self.lista4 = tk.Listbox(self.window, font=('Arial', 10))
        self.lista4.place(x=420, y=350, width=320, height=120)
        self.lista4.bind('<Double-Button-1>', lambda e: self.duplo_clique(4))
        
        self.window.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
        # Carregar listas APÓS todos os widgets serem criados
        self.window.after(100, lambda: self.carregar_lista(1))
        self.window.after(100, lambda: self.carregar_lista(2))
        self.window.after(100, lambda: self.carregar_lista(3))
        self.window.after(100, lambda: self.carregar_lista(4))
    
    def focar_secao(self, secao):
        """Focar no campo de entrada da seção selecionada"""
        entries = [None, self.entry1, self.entry2, self.entry3, self.entry4]
        if secao <= len(entries) - 1:
            entries[secao].focus_set()
    
    def limpar_tudo(self):
        """Limpar todos os campos de entrada"""
        if messagebox.askyesno("Confirmação", "Deseja limpar todos os campos?", parent=self.window):
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry4.delete(0, tk.END)
    
    def cadastrar(self, secao):
        entries = [None, self.entry1, self.entry2, self.entry3, self.entry4]
        listas = [None, self.lista1, self.lista2, self.lista3, self.lista4]
        nomes = [None, "Unidades", "Marcas", "Categorias", "Operações"]
        
        texto = entries[secao].get().strip()
        if texto:
            # SALVAR NO BANCO PRIMEIRO
            if self.salvar_banco(secao, texto):
                listas[secao].insert(tk.END, texto)
                entries[secao].delete(0, tk.END)
                messagebox.showinfo("✅ Sucesso", f"{nomes[secao]}: '{texto}' cadastrado e salvo!", parent=self.window)
                
                # Chamar callback de sincronização
                if self.callback_sincronizacao:
                    self.callback_sincronizacao('inserir', secao, item_novo=texto)
            else:
                messagebox.showwarning("⚠️ Aviso", f"'{texto}' já existe!", parent=self.window)
        else:
            messagebox.showwarning("Atenção", "Digite um valor!", parent=self.window)
    
    def cadastrar_varios(self, secao):
        """Abrir janela para cadastrar vários itens de uma vez"""
        nomes = [None, "Unidades", "Marcas", "Categorias", "Operações"]
        
        # Criar janela de cadastro em lote
        lote_window = tk.Toplevel(self.window)
        lote_window.title(f"Cadastrar Vários - {nomes[secao]}")
        lote_window.geometry("600x500")
        lote_window.configure(bg='#f0f0f0')
        lote_window.transient(self.window)
        lote_window.grab_set()
        
        # Centralizar
        lote_window.update_idletasks()
        x = (lote_window.winfo_screenwidth() // 2) - (300)
        y = (lote_window.winfo_screenheight() // 2) - (250)
        lote_window.geometry(f"600x500+{x}+{y}")
        
        # Título
        tk.Label(lote_window, text=f"Cadastrar Vários {nomes[secao]}", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        # Instruções
        tk.Label(lote_window, text="Digite um item por linha (pressione Enter para nova linha):", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        # Text widget para entrada de múltiplos itens
        text_frame = tk.Frame(lote_window, bg='#f0f0f0')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, font=('Arial', 11), height=15, width=60,
                             yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Frame de botões
        btn_frame = tk.Frame(lote_window, bg='#f0f0f0')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def salvar_lote():
            """Salvar todos os itens do text widget"""
            texto = text_widget.get("1.0", tk.END).strip()
            if not texto:
                messagebox.showwarning("Aviso", "Digite pelo menos um item!", parent=self.window)
                return
            
            # Separar por linhas e remover vazias
            itens = [item.strip() for item in texto.split('\n') if item.strip()]
            
            if not itens:
                messagebox.showwarning("Aviso", "Nenhum item válido encontrado!", parent=self.window)
                return
            
            # Cadastrar cada item
            sucesso = 0
            duplicados = 0
            
            for item in itens:
                if self.salvar_banco(secao, item):
                    sucesso += 1
                    # Chamar callback para cada item inserido
                    if self.callback_sincronizacao:
                        self.callback_sincronizacao('inserir', secao, item_novo=item)
                else:
                    duplicados += 1
            
            # Atualizar lista
            self.carregar_lista(secao)
            
            # Mensagem de resultado
            msg = f"✅ {sucesso} item(ns) cadastrado(s) com sucesso!"
            if duplicados > 0:
                msg += f"\n⚠️ {duplicados} item(ns) já existiam e foram ignorados."
            
            messagebox.showinfo("Resultado", msg, parent=self.window)
            lote_window.destroy()
        
        tk.Button(btn_frame, text="✅ Salvar Todos", font=('Arial', 11, 'bold'),
                 bg='#90EE90', width=15, command=salvar_lote).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar", font=('Arial', 11, 'bold'),
                 bg='#FFB6C1', width=15, command=lote_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def duplo_clique(self, secao):
        listas = [None, self.lista1, self.lista2, self.lista3, self.lista4]
        entries = [None, self.entry1, self.entry2, self.entry3, self.entry4]
        nomes = [None, "Unidades", "Marcas", "Categorias", "Operações"]
        
        selection = listas[secao].curselection()
        if selection:
            item = listas[secao].get(selection[0])
            entries[secao].delete(0, tk.END)
            entries[secao].insert(0, item)
            self.mostrar_opcoes_item(secao, item, listas, entries, nomes)
    
    def mostrar_opcoes_item(self, secao, item, listas, entries, nomes):
        opcoes_window = tk.Toplevel(self.window)
        opcoes_window.title(f"{nomes[secao]} - Opções")
        opcoes_window.geometry("400x300")
        opcoes_window.configure(bg='#f0f0f0')
        opcoes_window.transient(self.window)
        opcoes_window.grab_set()
        
        opcoes_window.update_idletasks()
        x = (opcoes_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (opcoes_window.winfo_screenheight() // 2) - (300 // 2)
        opcoes_window.geometry(f"400x300+{x}+{y}")
        
        tk.Label(opcoes_window, text=f"{nomes[secao]}", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        tk.Label(opcoes_window, text=f"Item selecionado: '{item}'", 
                font=('Arial', 11), bg='#f0f0f0').pack(pady=5)
        
        tk.Label(opcoes_window, text="Escolha uma opção:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=15)
        
        tk.Button(opcoes_window, text="✏️ ALTERAR ITEM", 
                 font=('Arial', 11, 'bold'), bg='#87CEEB', width=25, height=2,
                 command=lambda: self.alterar_item(opcoes_window, secao, item, listas, entries, nomes)).pack(pady=5)
        
        tk.Button(opcoes_window, text="🗑️ EXCLUIR ITEM", 
                 font=('Arial', 11, 'bold'), bg='#FFB6C1', width=25, height=2,
                 command=lambda: self.excluir_item(opcoes_window, secao, item, listas, entries, nomes)).pack(pady=5)
        
        tk.Button(opcoes_window, text="🧹 LIMPAR GERAL", 
                 font=('Arial', 11, 'bold'), bg='#FFA500', width=25, height=2,
                 command=lambda: self.limpar_geral(opcoes_window, secao, listas, entries, nomes)).pack(pady=5)
        
        tk.Button(opcoes_window, text="❌ CANCELAR", 
                 font=('Arial', 11, 'bold'), bg='#D3D3D3', width=25, height=2,
                 command=opcoes_window.destroy).pack(pady=5)
    
    def alterar_item(self, opcoes_window, secao, item, listas, entries, nomes):
        opcoes_window.destroy()
        novo = simpledialog.askstring(f"Alterar {nomes[secao]}", 
                                    f"Alterar '{item}' para:", 
                                    initialvalue=item)
        if novo and novo.strip() and novo.strip() != item:
            if self.alterar_banco(secao, item, novo.strip()):
                for i in range(listas[secao].size()):
                    if listas[secao].get(i) == item:
                        listas[secao].delete(i)
                        listas[secao].insert(i, novo.strip())
                        entries[secao].delete(0, tk.END)
                        entries[secao].insert(0, novo.strip())
                        messagebox.showinfo("✅ Sucesso", f"Item alterado para: {novo.strip()}", parent=self.window)
                        
                        # Chamar callback de sincronização
                        if self.callback_sincronizacao:
                            self.callback_sincronizacao('alterar', secao, item_antigo=item, item_novo=novo.strip())
                        break
            else:
                messagebox.showwarning("⚠️ Erro", "Falha ao alterar no banco!", parent=self.window)
    
    def excluir_item(self, opcoes_window, secao, item, listas, entries, nomes):
        opcoes_window.destroy()
        if messagebox.askyesno("Excluir Item", f"Excluir '{item}'?", parent=self.window):
            if self.excluir_banco(secao, item):
                for i in range(listas[secao].size()):
                    if listas[secao].get(i) == item:
                        listas[secao].delete(i)
                        entries[secao].delete(0, tk.END)
                        messagebox.showinfo("✅ Sucesso", f"Item '{item}' excluído!", parent=self.window)
                        
                        # Chamar callback de sincronização
                        if self.callback_sincronizacao:
                            self.callback_sincronizacao('excluir', secao, item_antigo=item)
                        break
            else:
                messagebox.showwarning("⚠️ Erro", "Falha ao excluir do banco!", parent=self.window)
    
    def limpar_geral(self, opcoes_window, secao, listas, entries, nomes):
        opcoes_window.destroy()
        total_itens = listas[secao].size()
        
        if total_itens == 0:
            messagebox.showinfo("Aviso", f"A lista de {nomes[secao]} já está vazia!", parent=self.window)
            return
        
        if messagebox.askyesno("⚠️ LIMPAR GERAL", 
                              f"🧹 ATENÇÃO!\n\nEsta ação irá EXCLUIR TODOS os {total_itens} itens!\n\nDeseja continuar?", parent=self.window):
            
            if messagebox.askyesno("⚠️ CONFIRMAÇÃO FINAL", 
                                  f"🚨 ÚLTIMA CONFIRMAÇÃO!\n\nTem certeza?\n\nEsta ação é IRREVERSÍVEL!", parent=self.window):
                
                if self.limpar_banco(secao):
                    listas[secao].delete(0, tk.END)
                    entries[secao].delete(0, tk.END)
                    messagebox.showinfo("✅ Limpeza Concluída", 
                                       f"🧹 {total_itens} itens removidos!", parent=self.window)
                    
                    # Chamar callback de sincronização
                    if self.callback_sincronizacao:
                        self.callback_sincronizacao('limpar_geral', secao)
                else:
                    messagebox.showwarning("⚠️ Erro", "Falha ao limpar o banco!", parent=self.window)
    
    def salvar_banco(self, secao, item):
        """Salvar item no banco - retorna True se sucesso"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tabelas = {1: 'unidades_div', 2: 'marcas_div', 3: 'categorias_div', 4: 'operacoes_div'}
            tabela = tabelas[secao]
            
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {tabela} (id INTEGER PRIMARY KEY, nome TEXT UNIQUE NOT NULL)')
            cursor.execute(f'INSERT INTO {tabela} (nome) VALUES (?)', (item,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def alterar_banco(self, secao, item_antigo, item_novo):
        """Alterar item no banco - retorna True se sucesso"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tabelas = {1: 'unidades_div', 2: 'marcas_div', 3: 'categorias_div', 4: 'operacoes_div'}
            tabela = tabelas[secao]
            
            cursor.execute(f'UPDATE {tabela} SET nome = ? WHERE nome = ?', (item_novo, item_antigo))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao alterar: {e}")
            return False
    
    def excluir_banco(self, secao, item):
        """Excluir item do banco - retorna True se sucesso"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tabelas = {1: 'unidades_div', 2: 'marcas_div', 3: 'categorias_div', 4: 'operacoes_div'}
            tabela = tabelas[secao]
            
            cursor.execute(f'DELETE FROM {tabela} WHERE nome = ?', (item,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao excluir: {e}")
            return False
    
    def limpar_banco(self, secao):
        """Limpar tabela do banco - retorna True se sucesso"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tabelas = {1: 'unidades_div', 2: 'marcas_div', 3: 'categorias_div', 4: 'operacoes_div'}
            tabela = tabelas[secao]
            
            # Deletar todos os registros
            cursor.execute(f'DELETE FROM {tabela}')
            
            # Criar tabela de controle se não existir
            cursor.execute('CREATE TABLE IF NOT EXISTS secoes_limpas (secao INTEGER PRIMARY KEY)')
            
            # Marcar esta seção como limpa
            cursor.execute('INSERT OR REPLACE INTO secoes_limpas (secao) VALUES (?)', (secao,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao limpar: {e}")
            return False
    
    def carregar_lista(self, secao):
        """Carregar lista do banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tabelas = {1: 'unidades_div', 2: 'marcas_div', 3: 'categorias_div', 4: 'operacoes_div'}
            listas = [None, self.lista1, self.lista2, self.lista3, self.lista4]
            dados_padrao = {
                1: ["UNID", "CX", "PC", "MT", "KIT", "RL", "POTE", "GALÃO"],
                2: ["Amanco", "Tigre", "Suvinil", "Coral", "OSRAM", "SUNFOR LED COB", "INFOVANIO", "LAFONTE"],
                3: ["Hidráulica", "Civil", "Mecânica", "Elétrica", "Limpeza", "Ferramentas"],
                4: ["ENTRADA NO ESTOQUE", "SAÍDA DO ESTOQUE", "ESTORNO DE COMPRA", "ESTORNO DE VENDA", "DOAÇÃO", "EMPRESTIMO", "USO OPERACIONAL", "CONTAGEM NO ESTOQUE"]
            }
            
            tabela = tabelas[secao]
            
            # Criar tabela se não existir
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {tabela} (id INTEGER PRIMARY KEY, nome TEXT UNIQUE NOT NULL)')
            
            # Criar tabela de controle de limpeza
            cursor.execute('CREATE TABLE IF NOT EXISTS secoes_limpas (secao INTEGER PRIMARY KEY)')
            
            # Verificar se esta seção foi limpa
            cursor.execute('SELECT COUNT(*) FROM secoes_limpas WHERE secao = ?', (secao,))
            foi_limpa = cursor.fetchone()[0] > 0
            
            # Contar registros na tabela
            cursor.execute(f'SELECT COUNT(*) FROM {tabela}')
            total = cursor.fetchone()[0]
            
            # Se a tabela está vazia E não foi limpa, inserir dados padrão
            if total == 0 and not foi_limpa:
                for item in dados_padrao[secao]:
                    try:
                        cursor.execute(f'INSERT INTO {tabela} (nome) VALUES (?)', (item,))
                    except sqlite3.IntegrityError:
                        pass
                conn.commit()
            
            # Carregar dados da tabela
            cursor.execute(f'SELECT nome FROM {tabela} ORDER BY nome')
            dados = [row[0] for row in cursor.fetchall()]
            
            for item in dados:
                listas[secao].insert(tk.END, item)
            
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar lista: {e}")
    
    def fechar_janela(self):
        if self.window:
            self.window.destroy()
            self.window = None
