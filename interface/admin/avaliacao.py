# interface/admin/avaliacao.py
import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox
from PIL import Image

class AvaliacaoPage(ctk.CTkFrame):
    """Página de Avaliação com layout moderno, limpo e idêntico à referência"""

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
        # Garante o fallback se não encontrar na pasta acima
        caminho = os.path.join(base_dir, 'database', 'sibes.db')
        if not os.path.exists(caminho):
            # Fallback para execução local padrão
            base_dir = os.path.dirname(os.path.abspath(__file__))
            caminho = os.path.join(base_dir, '..', '..', 'database', 'sibes.db')
        return os.path.abspath(caminho)

    def carregar_dados_combos(self):
        """Carrega os dados dos estudantes e bolsas do SQLite"""
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT nome, media, rendimento FROM estudantes")
            self.lista_estudantes = cursor.fetchall()
            
            cursor.execute("SELECT nome, tipo, valor FROM bolsas")
            self.lista_bolsas = cursor.fetchall()
            
            conn.close()
            
            # Atualiza os comboboxes com os nomes reais
            nomes_estudantes = [est[0] for est in self.lista_estudantes]
            if nomes_estudantes:
                self.combo_estudante.configure(values=nomes_estudantes)
                self.combo_estudante.set("Selecione um Estudante")
                
            nomes_bolsas = [b[0] for b in self.lista_bolsas]
            if nomes_bolsas:
                self.combo_bolsa.configure(values=nomes_bolsas)
                self.combo_bolsa.set("Selecione uma Bolsa")
                
        except Exception as e:
            print(f"Aviso ao carregar dados dos combos: {e}")

    def avaliar_candidatura(self):
        """Executa a lógica de simulação/avaliação baseada nos critérios da imagem"""
        estudante_sel = self.combo_estudante.get()
        bolsa_sel = self.combo_bolsa.get()

        if estudante_sel in ["Selecione um Estudante", ""] or bolsa_sel in ["Selecione uma Bolsa", ""]:
            messagebox.showwarning("Campos Incompletos", "Por favor, selecione um estudante e uma bolsa para avaliar.")
            return

        # Encontra os dados do estudante selecionado
        estudante_dados = next((e for e in self.lista_estudantes if e[0] == estudiante_sel), None)
        bolsa_dados = next((b for b in self.lista_bolsas if b[0] == bolsa_sel), None)

        if not estudante_dados or not bolsa_dados:
            messagebox.showerror("Erro", "Erro ao recuperar dados para avaliação.")
            return

        nome, media, renda = estudante_dados
        nome_bolsa, tipo_bolsa, valor_bolsa = bolsa_dados

        # Lógica de Avaliação Moderna baseada nas regras de negócio
        if media >= 14.0 and renda < 50000:
            resultado_estado = "Aprovado"
            cor_badge = "#DEF7EC"
            cor_texto_badge = "#03543F"
        elif media >= 10.0 and renda < 80000:
            resultado_estado = "Pendente"
            cor_badge = "#FEF3C7"
            cor_texto_badge = "#92400E"
        else:
            resultado_estado = "Rejeitado"
            cor_badge = "#FDE8E8"
            cor_texto_badge = "#9B1C1C"

        # Atualiza a interface gráfica dinamicamente
        self.lbl_res_nome.configure(text=str(nome))
        self.lbl_res_bolsa.configure(text=f"{nome_bolsa} ({tipo_bolsa})")
        self.lbl_res_media.configure(text=f"{media:.2f}v / 20v")
        self.lbl_res_renda.configure(text=f"{renda:,.2f} CVE")

        # Atualiza o Badge de Status
        self.badge_status.configure(fg_color=cor_badge)
        self.lbl_status.configure(text=resultado_estado.upper(), text_color=cor_texto_badge)

    def criar_interface(self):
        """Gera a interface pixel-perfect baseada no layout moderno fornecido"""
        
        # 1. CABEÇALHO DA PÁGINA
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=30, pady=(25, 20))

        lbl_titulo = ctk.CTkLabel(frame_topo, text="Avaliação Inteligente", font=("Segoe UI", 24, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_topo, text="Simule e analise a elegibilidade de estudantes para bolsas de estudo instantaneamente.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(4, 0))

        # 2. CONTAINER DAS DUAS COLUNAS PRINCIPAIS
        container_colunas = ctk.CTkFrame(self, fg_color="transparent")
        container_colunas.pack(fill="both", expand=True, padx=20, pady=5)
        container_colunas.grid_columnconfigure(0, weight=4, uniform="coluna_av") # Coluna de seleção (Esquerda)
        container_colunas.grid_columnconfigure(1, weight=5, uniform="coluna_av") # Coluna de resultados (Direita)
        container_colunas.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # COLUNA ESQUERDA: ENTRADA DE DADOS E FORMULÁRIO
        # ----------------------------------------------------
        card_esquerdo = ctk.CTkFrame(container_colunas, fg_color="white", corner_radius=14, border_width=1, border_color="#E5E7EB")
        card_esquerdo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Secção Superior Interna - Título
        ctk.CTkLabel(card_esquerdo, text="Configuração da Análise", font=("Segoe UI", 17, "bold"), text_color="#111827").pack(anchor="w", padx=25, pady=(25, 15))

        # Input 1: Selecionar Estudante
        ctk.CTkLabel(card_esquerdo, text="Estudante em Causa", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 4))
        self.combo_estudante = ctk.CTkComboBox(
            card_esquerdo, font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13),
            fg_color="white", border_color="#D1D5DB", button_color="#F3F4F6", button_hover_color="#E5E7EB",
            height=45, corner_radius=8, values=["Nenhum estudante carregado"]
        )
        self.combo_estudante.pack(fill="x", padx=25, pady=(0, 18))

        # Input 2: Selecionar Bolsa
        ctk.CTkLabel(card_esquerdo, text="Bolsa de Estudo Alvo", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 4))
        self.combo_bolsa = ctk.CTkComboBox(
            card_esquerdo, font=("Segoe UI", 13), dropdown_font=("Segoe UI", 13),
            fg_color="white", border_color="#D1D5DB", button_color="#F3F4F6", button_hover_color="#E5E7EB",
            height=45, corner_radius=8, values=["Nenhuma bolsa carregada"]
        )
        self.combo_bolsa.pack(fill="x", padx=25, pady=(0, 25))

        # Banner Técnico/Informativo Embutido no Card Esquerdo (Igual ao da Imagem)
        banner_ia = ctk.CTkFrame(card_esquerdo, fg_color="#F8FAFC", corner_radius=10, border_width=1, border_color="#E2E8F0")
        banner_ia.pack(fill="x", padx=25, pady=(5, 25))
        
        lbl_ia_tit = ctk.CTkLabel(banner_ia, text="✨ Motor de Decisão Ativo", font=("Segoe UI", 13, "bold"), text_color="#1E3A8A")
        lbl_ia_tit.pack(anchor="w", padx=15, pady=(12, 4))
        
        lbl_ia_desc = ctk.CTkLabel(
            banner_ia, text="O sistema valida automaticamente as condições socioeconómicas cruzando a média obtida com o teto de rendimento familiar.",
            font=("Segoe UI", 11), text_color="#475569", justify="left", wraplength=260
        )
        lbl_ia_desc.pack(anchor="w", padx=15, pady=(0, 12))

        # Espaçador automático para colar o botão perfeitamente ao fundo do card
        frame_espaco = ctk.CTkFrame(card_esquerdo, fg_color="transparent", height=1)
        frame_espaco.pack(fill="both", expand=True)

        # Botão Principal de Processamento (Largo e com 45px de altura)
        btn_processar = ctk.CTkButton(
            card_esquerdo, text="Processar Avaliação", font=("Segoe UI", 14, "bold"),
            fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white",
            height=46, corner_radius=8, command=self.avaliar_candidatura
        )
        btn_processar.pack(fill="x", padx=25, pady=(0, 25))


        # ----------------------------------------------------
        # COLUNA DIREITA: CARD DE RESULTADOS E STATUS DELUXE
        # ----------------------------------------------------
        card_direito = ctk.CTkFrame(container_colunas, fg_color="white", corner_radius=14, border_width=1, border_color="#E5E7EB")
        card_direito.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(card_direito, text="Relatório Técnico Prévio", font=("Segoe UI", 17, "bold"), text_color="#111827").pack(anchor="w", padx=30, pady=(25, 20))

        # Painel centralizador das tabelas de dados
        grid_dados = ctk.CTkFrame(card_direito, fg_color="transparent")
        grid_dados.pack(fill="x", padx=30, pady=5)
        grid_dados.grid_columnconfigure(0, weight=1)
        grid_dados.grid_columnconfigure(1, weight=2)

        # Configuração das linhas de dados formatados com divisórias discretas
        chaves = ["Nome do Candidato:", "Bolsa Pretendida:", "Mérito Académico:", "Rendimento Anual:"]
        
        self.lbl_res_nome = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w")
        self.lbl_res_bolsa = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13), text_color="#4B5563", anchor="w")
        self.lbl_res_media = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13, "bold"), text_color="#111827", anchor="w")
        self.lbl_res_renda = ctk.CTkLabel(grid_dados, text="-", font=("Segoe UI", 13), text_color="#111827", anchor="w")
        
        valores = [self.lbl_res_nome, self.lbl_res_bolsa, self.lbl_res_media, self.lbl_res_renda]

        for idx, t_chave in enumerate(chaves):
            # Label da esquerda (Chave)
            lbl_c = ctk.CTkLabel(grid_dados, text=t_chave, font=("Segoe UI", 13), text_color="#6B7280", anchor="w")
            lbl_c.grid(row=idx*2, column=0, pady=(12, 12), sticky="w")
            
            # Label da direita (Valor Real)
            valores[idx].grid(row=idx*2, column=1, pady=(12, 12), sticky="ew", padx=(10, 0))
            
            # Linha separadora entre itens do relatório (exceto no último)
            if idx < len(chaves) - 1:
                sep = ctk.CTkFrame(grid_dados, height=1, fg_color="#F3F4F6")
                sep.grid(row=idx*2 + 1, column=0, columnspan=2, sticky="ew")

        # Container do Status de Aprovação (Fundo Inferior)
        ctk.CTkLabel(card_direito, text="Estado da Elegibilidade", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(30, 6))
        
        # Badge de Status Retangular Expandido
        self.badge_status = ctk.CTkFrame(card_direito, fg_color="#F3F4F6", height=65, corner_radius=10)
        self.badge_status.pack(fill="x", padx=30, pady=(0, 25))
        self.badge_status.pack_propagate(False)

        self.lbl_status = ctk.CTkLabel(
            self.badge_status, text="AGUARDANDO SIMULAÇÃO", 
            font=("Segoe UI", 15, "bold"), text_color="#4B5563"
        )
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")