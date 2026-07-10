import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox

class Candidaturas(ctk.CTkFrame):
    """Página de Gestão de Candidaturas com layout idêntico ao de Bolsas Disponíveis"""

    def __init__(self, master, id_utilizador_logado=1):
        super().__init__(master, fg_color="#F4F6FB")

        self.id_utilizador_logado = id_utilizador_logado
        self.caminho_db = self.obter_caminho_db()
        self.candidaturas = []
        self.candidaturas_filtradas = []

        self.carregar_candidaturas()
        self.criar_interface()

    def obter_caminho_db(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
            return os.path.join(base_dir, 'database', 'sibes.db')
        else:
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, "..", ".."))
            return os.path.join(raiz_projeto, 'database', 'sibes.db')

    def carregar_candidaturas(self):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            
            # 🔥 Obtém o ID real do estudante logado antes de listar
            cursor.execute("SELECT LOWER(email) FROM utilizadores WHERE id = ?", (self.id_utilizador_logado,))
            user_res = cursor.fetchone()
            if not user_res or not user_res[0]:
                conn.close()
                return
            
            cursor.execute("SELECT id FROM estudantes WHERE LOWER(email) = ?", (user_res[0],))
            estudante_res = cursor.fetchone()
            if not estudante_res:
                conn.close()
                return
            id_estudante_real = estudante_res[0]

            cursor.execute("""
                            SELECT 
                                c.id, 
                                e.nome AS estudante_nome, 
                                b.nome AS bolsa_nome, 
                                c.data_candidatura, 
                                c.estado,
                                e.media,
                                e.rendimento
                            FROM candidaturas c
                            JOIN estudantes e ON c.estudante_id = e.id
                            JOIN bolsas b ON c.bolsa_id = b.id
                            WHERE c.estudante_id = ?
                            ORDER BY c.data_candidatura DESC
                           """, (id_estudante_real,))
            
            linhas = cursor.fetchall()
            self.candidaturas = []
            
            for linha in linhas:
                self.candidaturas.append({
                    "id": linha[0],
                    "estudante": linha[1],
                    "bolsa": linha[2],
                    "data": linha[3],
                    "estado": linha[4],
                    "media": linha[5],
                    "rendimento": linha[6]
                })
                
            conn.close()
            self.candidaturas_filtradas = self.candidaturas.copy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar candidaturas:\n{e}")
            self.candidaturas = []
            self.candidaturas_filtradas = []

    def criar_interface(self):
        # =========================================================================
        # 1. CABEÇALHO
        # =========================================================================
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(20, 10))

        frame_titulos = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_titulos.pack(side="left", fill="y", anchor="w")

        ctk.CTkLabel(frame_titulos, text="Minhas Candidaturas", font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(frame_titulos, text="Acompanhe o estado de validação das suas candidaturas submetidas.", font=("Segoe UI", 13), text_color="#6B7280").pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(self, height=1, fg_color="#E5E7EB").pack(fill="x", pady=(10, 20))

        # =========================================================================
        # 2. FILTROS
        # =========================================================================
        filtros = ctk.CTkFrame(self, fg_color="transparent")
        filtros.pack(fill="x", pady=(0, 15))

        self.entry_pesquisa = ctk.CTkEntry(
            filtros, placeholder_text="🔍 Pesquisar por bolsa...", height=38,
            fg_color="white", border_color="#E5E7EB"
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<KeyRelease>", self.filtrar_candidaturas)

        ctk.CTkLabel(filtros, text="Estado:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(5, 5))
        self.combo_estado = ctk.CTkComboBox(
            filtros, values=["Todos", "Pendente", "Aprovada", "Rejeitada"],
            height=35, fg_color="white", width=150, command=self.filtrar_candidaturas
        )
        self.combo_estado.pack(side="left", padx=(0, 10))
        self.combo_estado.set("Todos")

        # =========================================================================
        # 3. CONTAINER DA TABELA (Estilo Card Branco)
        # =========================================================================
        self.tabela_container = ctk.CTkScrollableFrame(
            self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB"
        )
        self.tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.desenhar_tabela()

    def desenhar_tabela(self):
        for widget in self.tabela_container.winfo_children():
            widget.destroy()

        colunas = ["ID", "Estudante", "Bolsa de Estudo", "Data Submissão", "Estado"]
        
        for i in range(len(colunas)):
            self.tabela_container.grid_columnconfigure(i, weight=1)

        for i, col in enumerate(colunas):
            ctk.CTkButton(
                self.tabela_container, text=col, font=("Segoe UI", 12, "bold"),
                fg_color="#F4F6FB", text_color="#6B7280", hover=False,
                height=35, border_width=1, border_color="#E5E7EB"
            ).grid(row=0, column=i, padx=15, pady=15, sticky="ew")

        if not self.candidaturas_filtradas:
            ctk.CTkLabel(
                self.tabela_container, text="Nenhuma candidatura encontrada.",
                font=("Segoe UI", 13), text_color="#9CA3AF"
            ).grid(row=1, column=0, columnspan=len(colunas), padx=15, pady=30)
            return

        for row_idx, cand in enumerate(self.candidaturas_filtradas, start=1):
            estado = cand['estado']
            cor_estado = "#10B981" if estado == "Aprovada" else "#F59E0B" if estado == "Pendente" else "#EF4444"

            ctk.CTkLabel(self.tabela_container, text=f"#{cand['id']}", font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=cand['estudante'], font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=cand['bolsa'], font=("Segoe UI", 13)).grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=cand['data'], font=("Segoe UI", 13)).grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=estado, font=("Segoe UI", 13, "bold"), text_color=cor_estado).grid(row=row_idx, column=4, padx=15, pady=10, sticky="w")

    def filtrar_candidaturas(self, *args):
        termo = self.entry_pesquisa.get().lower().strip()
        filtro_estado = self.combo_estado.get()

        self.candidaturas_filtradas = []
        for cand in self.candidaturas:
            corresponde_termo = termo in cand['estudante'].lower() or termo in cand['bolsa'].lower()
            corresponde_estado = filtro_estado == "Todos" or cand['estado'] == filtro_estado

            if corresponde_termo and corresponde_estado:
                self.candidaturas_filtradas.append(cand)

        self.desenhar_tabela()