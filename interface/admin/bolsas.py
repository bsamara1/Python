import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox

# IMPORTAR A CONEXÃO CENTRALIZADA DO TEU DATABASE.PY
try:
    from database.database import conectar
except ImportError:
    # Caso executes o ficheiro diretamente para testes
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(BASE_DIR)
    from database.database import conectar

class BolsasPage(ctk.CTkFrame):
    """Página de Gestão de Bolsas com layout moderno e atualizações em tempo real"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.bolsas = []
        self.bolsas_filtradas = []

        self.carregar_bolsas()
        self.criar_interface()

    def carregar_bolsas(self):
        """Carrega as bolsas ligando diretamente à base de dados central"""
        try:
            conn = conectar() # Usa a ligação oficial do teu projeto
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, tipo, valor, estado FROM bolsas")
            linhas = cursor.fetchall()
            
            self.bolsas = []
            for linha in linhas:
                self.bolsas.append({
                    'id': linha[0],
                    'nome': linha[1],
                    'tipo': linha[2],
                    'valor': linha[3],
                    'estado': linha[4]
                })
            self.bolsas_filtradas = self.bolsas.copy()
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar bolsas: {e}")
            self.bolsas = []
            self.bolsas_filtradas = []

    def filtrar_dados(self, *args):
        termo = self.entry_pesquisa.get().lower()
        filtro_estado = self.combo_filtro.get()

        self.bolsas_filtradas = []
        for b in self.bolsas:
            corresponde_termo = (termo in str(b['nome']).lower() or 
                                 termo in str(b['tipo']).lower() or 
                                 termo in str(b['id']).lower())
            
            corresponde_filtro = (filtro_estado == "Todos" or 
                                  str(b['estado']).lower() == filtro_estado.lower())

            if corresponde_termo and corresponde_filtro:
                self.bolsas_filtradas.append(b)
        
        self.atualizar_tabela()

    def criar_interface(self):
        # 1. CABEÇALHO
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(10, 20))

        frame_titulos = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_titulos.pack(side="left", anchor="w")
        
        lbl_titulo = ctk.CTkLabel(frame_titulos, text="Bolsas", font=("Segoe UI", 26, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_titulos, text="Gerir todas as bolsas e editais registados.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))

        btn_adicionar = ctk.CTkButton(
            frame_topo, text="+ Adicionar Bolsa", font=("Segoe UI", 13, "bold"),
            fg_color="#1A5CFF", hover_color="#0043E0", text_color="white",
            height=40, corner_radius=8, command=self.abrir_formulario_adicionar
        )
        btn_adicionar.pack(side="right", anchor="e")

        # 2. BARRA DE PESQUISA
        frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        frame_filtros.pack(fill="x", pady=(0, 15))

        self.entry_pesquisa = ctk.CTkEntry(
            frame_filtros, placeholder_text="🔍 Pesquisar por nome, ID ou tipo...",
            font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=40, corner_radius=8
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry_pesquisa.bind("<KeyRelease>", self.filtrar_dados)

        self.combo_filtro = ctk.CTkComboBox(
            frame_filtros, values=["Todos", "Ativo", "Inativo"], font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB",
            button_color="#F3F4F6", button_hover_color="#E5E7EB", height=40, width=150, corner_radius=8,
            command=self.filtrar_dados
        )
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="right")

        # 3. CARD DA TABELA
        self.card_conteudo = ctk.CTkFrame(self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        self.card_conteudo.pack(fill="both", expand=True)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.card_conteudo.winfo_children():
            widget.destroy()

        self.card_conteudo.grid_columnconfigure(0, weight=1)
        self.card_conteudo.grid_columnconfigure(1, weight=4)
        self.card_conteudo.grid_columnconfigure(2, weight=2)
        self.card_conteudo.grid_columnconfigure(3, weight=2)
        self.card_conteudo.grid_columnconfigure(4, weight=2)
        self.card_conteudo.grid_columnconfigure(5, weight=1)

        headers = ["ID", "Nome da Bolsa", "Tipo", "Valor Benefício", "Estado", "Ações"]
        for col_idx, texto in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.card_conteudo, text=texto, font=("Segoe UI", 12, "bold"), text_color="#4B5563",
                anchor="w" if col_idx != 5 else "center"
            )
            lbl.grid(row=0, column=col_idx, padx=20, pady=(15, 10), sticky="nsew")

        div = ctk.CTkFrame(self.card_conteudo, height=1, fg_color="#F3F4F6")
        div.grid(row=1, column=0, columnspan=6, sticky="ew", padx=10)

        if not self.bolsas_filtradas:
            lbl_vazio = ctk.CTkLabel(self.card_conteudo, text="Nenhuma bolsa ou edital encontrado.", font=("Segoe UI", 14), text_color="#9CA3AF")
            lbl_vazio.grid(row=2, column=0, columnspan=6, pady=40)
            return

        for row_idx, b in enumerate(self.bolsas_filtradas, start=2):
            padd_y = 12

            ctk.CTkLabel(self.card_conteudo, text=f"{b['id']}", font=("Segoe UI", 13), text_color="#6B7280", anchor="w").grid(row=row_idx*2, column=0, padx=20, pady=padd_y, sticky="w")
            ctk.CTkLabel(self.card_conteudo, text=b['nome'], font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w").grid(row=row_idx*2, column=1, padx=20, pady=padd_y, sticky="w")
            ctk.CTkLabel(self.card_conteudo, text=str(b['tipo'] or "N/A"), font=("Segoe UI", 13), text_color="#4B5563", anchor="w").grid(row=row_idx*2, column=2, padx=20, pady=padd_y, sticky="w")
            
            valor_formatado = f"{b['valor']:,}$".replace(",", ".") if isinstance(b['valor'], (int, float)) else f"{b['valor'] or 0}$"
            ctk.CTkLabel(self.card_conteudo, text=valor_formatado, font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w").grid(row=row_idx*2, column=3, padx=20, pady=padd_y, sticky="w")
            
            est = str(b['estado'] or "Ativo").capitalize()
            cor_estado = "#10B981" if est == "Ativo" else "#EF4444"
            ctk.CTkLabel(self.card_conteudo, text=est, font=("Segoe UI", 13, "bold"), text_color=cor_estado, anchor="w").grid(row=row_idx*2, column=4, padx=20, pady=padd_y, sticky="w")

            frame_acoes = ctk.CTkFrame(self.card_conteudo, fg_color="transparent")
            frame_acoes.grid(row=row_idx*2, column=5, padx=10, pady=padd_y)

            btn_edit = ctk.CTkButton(
                frame_acoes, text="Editar", width=30, height=30, fg_color="#F3F4F6",
                hover_color="#E5E7EB", text_color="#1A5CFF", corner_radius=6,
                command=lambda bls=b: self.editar_bolsa(bls)
            )
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                frame_acoes, text="Eliminar", width=30, height=30, fg_color="#FEE2E2",
                hover_color="#FCA5A5", text_color="#EF4444", corner_radius=6,
                command=lambda bls=b: self.eliminar_bolsa(bls)
            )
            btn_del.pack(side="left", padx=2)

            sub_div = ctk.CTkFrame(self.card_conteudo, height=1, fg_color="#F9FAFB")
            sub_div.grid(row=row_idx*2 + 1, column=0, columnspan=6, sticky="ew", padx=10)

    def abrir_formulario_adicionar(self):
        self.abrir_formulario_bolsa()

    def editar_bolsa(self, bolsa):
        self.abrir_formulario_bolsa(bolsa)

    def abrir_formulario_bolsa(self, dados_bolsa=None):
        janela_form = ctk.CTkToplevel(self)
        janela_form.title("Formulário de Bolsa")
        janela_form.geometry("450x550")
        janela_form.grab_set()

        titulo = "Editar Bolsa" if dados_bolsa else "Adicionar Nova Bolsa"
        ctk.CTkLabel(janela_form, text=titulo, font=("Segoe UI", 18, "bold"), text_color="#142850").pack(pady=15)

        form_container = ctk.CTkFrame(janela_form, fg_color="transparent")
        form_container.pack(padx=20, pady=5, fill="both", expand=True)

        ctk.CTkLabel(form_container, text="Nome da Bolsa", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 2))
        entry_nome = ctk.CTkEntry(form_container, width=380, height=35)
        entry_nome.pack(pady=(0, 10))

        ctk.CTkLabel(form_container, text="Tipo (ex: Mérito, Social, Cultural)", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 2))
        entry_tipo = ctk.CTkEntry(form_container, width=380, height=35)
        entry_tipo.pack(pady=(0, 10))

        ctk.CTkLabel(form_container, text="Valor do Benefício", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 2))
        entry_valor = ctk.CTkEntry(form_container, width=380, height=35, placeholder_text="Ex: 12000")
        entry_valor.pack(pady=(0, 10))

        ctk.CTkLabel(form_container, text="Estado", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 2))
        combo_estado = ctk.CTkComboBox(form_container, values=["Ativo", "Inativo"], width=380, height=35)
        combo_estado.set("Ativo")
        combo_estado.pack(pady=(0, 15))

        if dados_bolsa:
            entry_nome.insert(0, str(dados_bolsa['nome']))
            entry_tipo.insert(0, str(dados_bolsa['tipo'] or ""))
            entry_valor.insert(0, str(dados_bolsa['valor'] or ""))
            combo_estado.set(str(dados_bolsa['estado'] or "Ativo").capitalize())

        frame_botoes = ctk.CTkFrame(janela_form, fg_color="transparent")
        frame_botoes.pack(pady=20)

        id_bolsa = dados_bolsa['id'] if dados_bolsa else None
        texto_confirmar = "Atualizar" if dados_bolsa else "Guardar"

        btn_salvar = ctk.CTkButton(
            frame_botoes, text=texto_confirmar, fg_color="#1A5CFF", hover_color="#0043E0",
            font=("Segoe UI", 13, "bold"),
            command=lambda: self.salvar_dados(
                entry_nome.get(), entry_tipo.get(), entry_valor.get(), combo_estado.get(), janela_form, id_bolsa
            )
        )
        btn_salvar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(
            frame_botoes, text="Cancelar", fg_color="#E5E7EB", hover_color="#D1D5DB",
            text_color="#4B5563", font=("Segoe UI", 13, "bold"), command=janela_form.destroy
        )
        btn_cancelar.pack(side="left", padx=10)

    def salvar_dados(self, nome, tipo, valor, estado, janela, id_bolsa=None):
        if not (nome.strip() and tipo.strip() and valor.strip()):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios!")
            return

        try:
            valor_numerico = float(valor.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro de Validação", "O campo 'Valor' deve conter um número válido.")
            return

        try:
            conn = conectar() # LIGAÇÃO À BASE DE DADOS CENTRALIZADA
            cursor = conn.cursor()

            if id_bolsa is None:
                # INSERIR NOVA BOLSA
                cursor.execute("""
                    INSERT INTO bolsas (nome, tipo, valor, estado) 
                    VALUES (?, ?, ?, ?)
                """, (nome, tipo, valor_numerico, estado))
                messagebox.showinfo("Sucesso", "Nova bolsa adicionada com sucesso!")
            else:
                # ATUALIZAR BOLSA EXISTENTE
                cursor.execute("""
                    UPDATE bolsas 
                    SET nome=?, tipo=?, valor=?, estado=? 
                    WHERE id=?
                """, (nome, tipo, valor_numerico, estado, id_bolsa))
                messagebox.showinfo("Sucesso", "Bolsa atualizada com sucesso!")

            conn.commit()
            conn.close()

            # ESTE BLOCO ESTÁ CORRIGIDO PARA ATUALIZAR A INTERFACE EM TEMPO REAL
            janela.destroy()
            self.carregar_bolsas() # Recarrega os dados do SQLite
            self.filtrar_dados()   # Redesenha a tabela no ecrã

        except Exception as e:
            messagebox.showerror("Erro na Base de Dados", f"Não foi possível salvar os dados: {e}")

    def eliminar_bolsa(self, bolsa):
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente apagar a bolsa '{bolsa['nome']}'?"):
            try:
                conn = conectar() 
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bolsas WHERE id=?", (bolsa['id'],))
                conn.commit()
                conn.close()
                
                self.carregar_bolsas()
                self.filtrar_dados()
                messagebox.showinfo("Sucesso", "Bolsa eliminada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível eliminar a bolsa: {e}")