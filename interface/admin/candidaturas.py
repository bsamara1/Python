# candidaturas.py
import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox

class Candidaturas(ctk.CTkFrame):
    """Página de Gestão de Candidaturas com layout idêntico ao dashboard moderno e campos para regras Prolog"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.caminho_db = self.obter_caminho_db()
        self.candidaturas = []
        self.candidaturas_filtradas = []

        self.carregar_candidaturas()
        self.criar_interface()

    def obter_caminho_db(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'database', 'sibes.db')

    def carregar_candidaturas(self):
        """Carrega dados incluindo colunas estruturadas para processamento de regras Prolog"""
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            
            # Executa query trazendo as informações completas incluindo a Data
            cursor.execute("SELECT id, estudante, bolsa, estado, data_candidatura FROM candidaturas")
            linhas = cursor.fetchall()
            
            self.candidaturas = []
            for linha in linhas:
                self.candidaturas.append({
                    "id": linha[0],
                    "estudante": linha[1],
                    "bolsa": linha[2],
                    "estado": linha[3],
                    "data": linha[4] if linha[4] else "N/A"
                })
            self.candidaturas_filtradas = self.candidaturas.copy()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar candidaturas: {e}")

    def filtrar_dados(self, *args):
        """Filtro dinâmico em tempo real para Pesquisa e Combobox de Estados"""
        termo = self.entry_pesquisa.get().lower()
        filtro_estado = self.combo_filtro.get()

        self.candidaturas_filtradas = []
        for c in self.candidaturas:
            corresponde_termo = (termo in str(c['estudante']).lower() or 
                                 termo in str(c['bolsa']).lower() or 
                                 termo in str(c['id']).lower() or
                                 termo in str(c['data']).lower())
            
            corresponde_filtro = (filtro_estado == "Todos" or 
                                  str(c['estado']).lower() == filtro_estado.lower())

            if corresponde_termo and corresponde_filtro:
                self.candidaturas_filtradas.append(c)
        
        self.atualizar_tabela()

    def criar_interface(self):
        # 1. CABEÇALHO (Título e Descrição do Objetivo Geral)
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(20, 10))

        frame_titulos = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_titulos.pack(side="left", anchor="w")
        
        lbl_titulo = ctk.CTkLabel(frame_titulos, text="Candidaturas", font=("Segoe UI", 26, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_titulos, text="Sistema Inteligente: Processamento e Elegibilidade de Candidatos.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))
        
        self.divisoria_topo = ctk.CTkFrame(self, height=1, fg_color="#E5E7EB")
        self.divisoria_topo.pack(fill="x", pady=(10, 20))

        # 2. BARRA DE FILTROS E PESQUISA MODERNIZADA
        frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        frame_filtros.pack(fill="x", pady=(0, 15))

        self.entry_pesquisa = ctk.CTkEntry(
            frame_filtros, placeholder_text="🔍 Pesquisar por estudante, bolsa, data ou ID...",
            font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=40, corner_radius=8
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry_pesquisa.bind("<KeyRelease>", self.filtrar_dados)

        self.combo_filtro = ctk.CTkComboBox(
            frame_filtros, values=["Todos", "Pendente", "Aprovada", "Rejeitada"], font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB",
            button_color="#F3F4F6", button_hover_color="#E5E7EB", height=40, width=150, corner_radius=8,
            command=self.filtrar_dados
        )
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="right")

        # 3. CARD CONTAINER BRANCO (Fundo arredondado para a Tabela)
        self.card_conteudo = ctk.CTkFrame(self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        self.card_conteudo.pack(fill="both", expand=True)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.card_conteudo.winfo_children():
            widget.destroy()

        # Alinhamento Milimétrico das 6 Colunas da Grelha
        self.card_conteudo.grid_columnconfigure(0, weight=1)  # ID
        self.card_conteudo.grid_columnconfigure(1, weight=3)  # Estudante
        self.card_conteudo.grid_columnconfigure(2, weight=3)  # Bolsa / Edital
        self.card_conteudo.grid_columnconfigure(3, weight=2)  # Data Submissão
        self.card_conteudo.grid_columnconfigure(4, weight=2)  # Estado
        self.card_conteudo.grid_columnconfigure(5, weight=2)  # Ações

        # Cabeçalhos Cinzentos Profissionais
        headers = ["ID", "Estudante", "Bolsa ", "Data Submissão", "Estado", "Ações"]
        for col_idx, texto in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.card_conteudo, text=texto, font=("Segoe UI", 12, "bold"), text_color="#4B5563",
                anchor="w" if col_idx != 5 else "center"
            )
            lbl.grid(row=0, column=col_idx, padx=20, pady=(15, 10), sticky="nsew")

        # Linha Divisória Superior
        div = ctk.CTkFrame(self.card_conteudo, height=1, fg_color="#F3F4F6")
        div.grid(row=1, column=0, columnspan=6, sticky="ew", padx=10)

        if not self.candidaturas_filtradas:
            lbl_vazio = ctk.CTkLabel(self.card_conteudo, text="Nenhuma candidatura registada no sistema.", font=("Segoe UI", 14), text_color="#9CA3AF")
            lbl_vazio.grid(row=2, column=0, columnspan=6, pady=40)
            return

        # População Dinâmica das Linhas
        for row_idx, cand in enumerate(self.candidaturas_filtradas, start=2):
            padd_y = 12

            # Dados das Colunas
            ctk.CTkLabel(self.card_conteudo, text=f"{cand['id']}", font=("Segoe UI", 13), text_color="#6B7280", anchor="w").grid(row=row_idx*2, column=0, padx=20, pady=padd_y, sticky="w")
            ctk.CTkLabel(self.card_conteudo, text=cand['estudante'], font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w").grid(row=row_idx*2, column=1, padx=20, pady=padd_y, sticky="w")
            ctk.CTkLabel(self.card_conteudo, text=cand['bolsa'], font=("Segoe UI", 13), text_color="#4B5563", anchor="w").grid(row=row_idx*2, column=2, padx=20, pady=padd_y, sticky="w")
            ctk.CTkLabel(self.card_conteudo, text=cand['data'], font=("Segoe UI", 13), text_color="#4B5563", anchor="w").grid(row=row_idx*2, column=3, padx=20, pady=padd_y, sticky="w")
            
            # Formatação de Cores Baseada nos Estados do Fluxo
            est = str(cand['estado']).capitalize()
            if est == "Aprovada":
                cor_estado = "#10B981"  # Verde para Aceite
            elif est == "Rejeitada":
                cor_estado = "#EF4444"  # Vermelho para Não Elegível
            else:
                cor_estado = "#F59E0B"  # Laranja para Avaliação Pendente

            ctk.CTkLabel(self.card_conteudo, text=est, font=("Segoe UI", 13, "bold"), text_color=cor_estado, anchor="w").grid(row=row_idx*2, column=4, padx=20, pady=padd_y, sticky="w")

            # Botões de Ação à Direita (Administração)
            frame_acoes = ctk.CTkFrame(self.card_conteudo, fg_color="transparent")
            frame_acoes.grid(row=row_idx*2, column=5, padx=10, pady=padd_y)

            btn_aprovar = ctk.CTkButton(
                frame_acoes, text="Aprovar", font=("Segoe UI", 11, "bold"), width=70, height=28, 
                fg_color="#ECFDF5", hover_color="#D1FAE5", text_color="#10B981", corner_radius=6,
                command=lambda c=cand: self.atualizar_estado(c['id'], "Aprovada")
            )
            btn_aprovar.pack(side="left", padx=2)

            btn_rejeitar = ctk.CTkButton(
                frame_acoes, text="Rejeitar", font=("Segoe UI", 11, "bold"), width=70, height=28, 
                fg_color="#FEE2E2", hover_color="#FCA5A5", text_color="#EF4444", corner_radius=6,
                command=lambda c=cand: self.atualizar_estado(c['id'], "Rejeitada")
            )
            btn_rejeitar.pack(side="left", padx=2)

            # Sub-divisória suave entre registos
            sub_div = ctk.CTkFrame(self.card_conteudo, height=1, fg_color="#F9FAFB")
            sub_div.grid(row=row_idx*2 + 1, column=0, columnspan=6, sticky="ew", padx=10)

    def atualizar_estado(self, candidatura_id, novo_estado):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("UPDATE candidaturas SET estado = ? WHERE id = ?", (novo_estado, candidatura_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", f"Candidatura atualizada para {novo_estado}!")
            self.carregar_candidaturas()
            self.filtrar_dados()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", str(e))