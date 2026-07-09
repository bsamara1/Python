# avaliacao.py
import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox

class AvaliacaoPage(ctk.CTkFrame):
    """Página de Avaliação com layout de duas colunas (Estudante e Bolsa) idêntica à imagem"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.caminho_db = self.obter_caminho_db()
        self.lista_estudantes = []
        self.lista_bolsas = []
        
        self.criar_interface()
        self.carregar_dados_combos()

    def obter_caminho_db(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'database', 'sibes.db')

    def carregar_dados_combos(self):
        """Carrega os dados dos estudantes e bolsas disponíveis no sistema"""
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            
            # 1. Carrega dados dos estudantes
            cursor.execute("SELECT nome, media, rendimento FROM estudantes")
            self.lista_estudantes = cursor.fetchall()
            
            # 2. Carrega as bolsas registadas
            cursor.execute("SELECT nome FROM bolsas")
            self.lista_bolsas = [linha[0] for linha in cursor.fetchall()]
            
            conn.close()

            # Popula o ComboBox de Estudantes
            nomes_estudantes = [est[0] for est in self.lista_estudantes]
            if nomes_estudantes:
                self.combo_estudante.configure(values=nomes_estudantes)
                self.combo_estudante.set(nomes_estudantes[0])
            else:
                self.lista_estudantes = [("Ana", 16.5, 30000), ("Maria", 15.0, 40000), ("Pedro", 12.0, 20000)]
                self.combo_estudante.configure(values=["Ana", "Maria", "Pedro"])
                self.combo_estudante.set("Ana")

            # Popula o ComboBox de Bolsas
            if self.lista_bolsas:
                self.combo_bolsa.configure(values=self.lista_bolsas)
                self.combo_bolsa.set(self.lista_bolsas[0])
            else:
                self.lista_bolsas = ["Bolsa de Estudo Integral", "Bolsa de Mérito", "Bolsa Social"]
                self.combo_bolsa.configure(values=self.lista_bolsas)
                self.combo_bolsa.set(self.lista_bolsas[0])

        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def avaliar_candidatura(self):
        """Recolhe os parâmetros para a avaliação (Pronto para chamar o teu Prolog separado)"""
        estudante_sel = self.combo_estudante.get()
        bolsa_sel = self.combo_bolsa.get()

        if not estudante_sel or not bolsa_sel:
            return

        # Busca os dados académicos do estudante selecionado na interface
        dados_est = next((item for item in self.lista_estudantes if item[0] == estudante_sel), None)
        if not dados_est:
            return

        nome, media, renda = dados_est[0], dados_est[1] if dados_est[1] else 0, dados_est[2] if dados_est[2] else 0

        # -------------------------------------------------------------------------
        # ESPAÇO RESERVADO PARA FAZERES O IMPORT OU CHAMADA AO TEU PROLOG SEPARADO
        # Exemplo: resultado = TeuModuloProlog.verificar(nome, media, renda)
        # -------------------------------------------------------------------------
        
        # Por enquanto, exibe os dados recolhidos no painel à direita
        self.lbl_res_nome.configure(text=nome)
        self.lbl_res_bolsa.configure(text=bolsa_sel)
        self.lbl_res_media.configure(text=f"{media} valores")
        self.lbl_res_renda.configure(text=f"{renda:,}$".replace(",", "."))
        
        # Modifica o Badge para indicar que os dados foram processados
        self.badge_resultado.configure(fg_color="#EFF6FF") # Cor Azul clara informativa
        self.lbl_badge_status.configure(text="Dados Enviados para Análise", text_color="#1D4ED8")

    def criar_interface(self):
        # TÍTULO PRINCIPAL DA JANELA
        lbl_titulo = ctk.CTkLabel(self, text="Avaliação Inteligente", font=("Segoe UI", 26, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w", pady=(10, 5))
        
        lbl_subtitulo = ctk.CTkLabel(self, text="Selecione os parâmetros abaixo para processamento dos critérios.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(0, 20))

        # CONTAINER SPLIT LAYOUT (Duas Colunas Perfeitas)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1, uniform="col")
        container.grid_columnconfigure(1, weight=1, uniform="col")
        container.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # COLUNA ESQUERDA: DOIS COMBO BOXES E BOTÃO
        # ----------------------------------------------------
        card_esquerdo = ctk.CTkFrame(container, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        ctk.CTkLabel(card_esquerdo, text="Selecionar Candidatura", font=("Segoe UI", 16, "bold"), text_color="#111827").pack(pady=(25, 15))
        
        # 1. Combo do Estudante
        ctk.CTkLabel(card_esquerdo, text="Selecionar Estudante:", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=40, pady=(10, 2))
        self.combo_estudante = ctk.CTkComboBox(
            card_esquerdo, values=[], width=320, height=42,
            font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13),
            fg_color="white", border_color="#E5E7EB", button_color="#F3F4F6"
        )
        self.combo_estudante.pack(pady=(0, 15))

        # 2. Combo da Bolsa
        ctk.CTkLabel(card_esquerdo, text="Selecionar Bolsa de Estudo:", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=40, pady=(10, 2))
        self.combo_bolsa = ctk.CTkComboBox(
            card_esquerdo, values=[], width=320, height=42,
            font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13),
            fg_color="white", border_color="#E5E7EB", button_color="#F3F4F6"
        )
        self.combo_bolsa.pack(pady=(0, 25))

        # Botão Azul de Avaliação
        btn_avaliar = ctk.CTkButton(
            card_esquerdo, text="Avaliar Elegibilidade", font=("Segoe UI", 13, "bold"),
            fg_color="#1A5CFF", hover_color="#0043E0", text_color="white",
            width=320, height=42, corner_radius=8, command=self.avaliar_candidatura
        )
        btn_avaliar.pack(pady=10)

        # ----------------------------------------------------
        # COLUNA DIREITA: CARD DO RESULTADO
        # ----------------------------------------------------
        card_direito = ctk.CTkFrame(container, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_direito.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        ctk.CTkLabel(card_direito, text="Resultado da Avaliação", font=("Segoe UI", 16, "bold"), text_color="#111827").pack(pady=(25, 15))

        # Painel Grid Interno para as Informações do Aluno
        grid_dados = ctk.CTkFrame(card_direito, fg_color="transparent")
        grid_dados.pack(fill="x", padx=40, pady=10)
        grid_dados.grid_columnconfigure(1, weight=1)

        chaves = ["Candidato:", "Bolsa Alvo:", "Média Académica:", "Rendimento Familiar:"]
        self.lbl_res_nome = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w")
        self.lbl_res_bolsa = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13), text_color="#4B5563", anchor="w")
        self.lbl_res_media = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13), text_color="#111827", anchor="w")
        self.lbl_res_renda = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13), text_color="#111827", anchor="w")
        
        valores = [self.lbl_res_nome, self.lbl_res_bolsa, self.lbl_res_media, self.lbl_res_renda]

        for idx, t_chave in enumerate(chaves):
            ctk.CTkLabel(grid_dados, text=t_chave, font=("Segoe UI", 13), text_color="#6B7280", anchor="w").grid(row=idx, column=0, pady=8, sticky="w", padx=(0, 20))
            valores[idx].grid(row=idx, column=1, pady=8, sticky="ew")

        # Badge Grande para o Estado Atual da Avaliação
        self.badge_resultado = ctk.CTkFrame(card_direito, fg_color="#F3F4F6", corner_radius=8, height=50)
        self.badge_resultado.pack(fill="x", padx=40, pady=(35, 0))
        self.badge_resultado.pack_propagate(False)

        self.lbl_badge_status = ctk.CTkLabel(
            self.badge_resultado, text="Aguardando Seleção", 
            font=("Segoe UI", 14, "bold"), text_color="#9CA3AF"
        )
        self.lbl_badge_status.place(relx=0.5, rely=0.5, anchor="center")