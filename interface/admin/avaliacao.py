import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox
from PIL import Image
import datetime
import subprocess
import tempfile
from database.database import conectar

# Tentar importar pyswip
try:
    from pyswip import Prolog
    PROLOG_DISPONIVEL = True
except ImportError:
    PROLOG_DISPONIVEL = False

class AvaliacaoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        # Se não houver uma lógica complexa para obter o caminho, 
        # pode definir diretamente ou implementar o método correspondente.
        self.caminho_db = "database.db" 
        self.lista_estudantes = []
        self.lista_bolsas = []

        # --- INICIALIZAÇÃO DO PROLOG UNIFICADA ---
        self.prolog = self.inicializar_prolog()
        # -------------------------------------

        self.criar_interface()
        self.carregar_dados_combos()

    def inicializar_prolog(self):
        """Inicializa o motor Prolog corretamente"""
        if not PROLOG_DISPONIVEL:
            print("⚠️  SWI-Prolog não disponível. Instale de: https://www.swi-prolog.org/Download.html")
            return None

        try:
            prolog = Prolog()
            # Ajuste o caminho conforme a estrutura real das suas pastas:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            regras_path = os.path.join(base_dir, 'regras.pl').replace("\\", "/")

            if os.path.exists(regras_path):
                prolog.consult(regras_path)
                print(f"✓ Regras Prolog carregadas de: {regras_path}")
            else:
                print(f"⚠️  Arquivo de regras não encontrado: {regras_path}")
            return prolog
        except Exception as e:
            print(f"Erro ao inicializar Prolog: {e}")
            return None

    def avaliar_com_prolog(self, tipo_bolsa, media, rendimento):
        """Avalia elegibilidade isolando o motor Prolog por chamada para evitar falhas de thread"""
        if not PROLOG_DISPONIVEL:
            return False, ["❌ Motor Prolog não disponível"]

        try:
            # Criamos uma instância local e isolada para esta consulta específica
            prolog_local = Prolog()
            
            # Localiza e carrega as regras estritamente para esta execução
            base_dir = os.path.dirname(os.path.abspath(__file__))
            caminho_regras = os.path.join(base_dir, 'regras.pl').replace("\\", "/")
            prolog_local.consult(caminho_regras)

            query_str = f'elegivel("{tipo_bolsa}", {media}, {rendimento})'
            
            # Executa e consome imediatamente os dados
            with prolog_local.query(query_str) as q:
                resultado = list(q)

            # Limpa referências locais para forçar o coletor do Python a liberar a interface C
            del prolog_local

            if resultado:
                motivos = [
                    f"✓ Aprovado pela regra: elegivel('{tipo_bolsa}', {media}, {rendimento})",
                    f"✓ Média: {media:.1f}v",
                    f"✓ Rendimento: {rendimento:,.0f}v"
                ]
                return True, motivos
            else:
                motivos = [
                    f"✗ Não elegível para '{tipo_bolsa}'",
                    f"✗ Critérios não cumpridos",
                    f"  Média: {media:.1f}v",
                    f"  Rendimento: {rendimento:,.0f}v"
                ]
                return False, motivos

        except Exception as e:
            return False, [f"❌ Erro ao executar Prolog: {str(e)}"]
        
    def avaliar_candidatura(self):
        """Executa a avaliação com Prolog"""
        estudante_sel = self.combo_estudante.get()
        bolsa_sel = self.combo_bolsa.get()

        if estudante_sel in ["Selecione um Estudante", ""] or bolsa_sel in ["Selecione uma Bolsa", ""]:
            messagebox.showwarning("Campos Incompletos", "Por favor, selecione um estudante e uma bolsa para avaliar.")
            return

        # Encontra os dados
        estudante_dados = next((e for e in self.lista_estudantes if e[1] == estudante_sel), None)
        bolsa_dados = next((b for b in self.lista_bolsas if b[1] == bolsa_sel), None)

        if not estudante_dados or not bolsa_dados:
            messagebox.showerror("Erro", "Erro ao recuperar dados para avaliação.")
            return

        id_est, nome, media, rendimento = estudante_dados
        id_bolsa, nome_bolsa, tipo_bolsa = bolsa_dados

        # Aplicar regras Prolog
        elegivel, motivos = self.avaliar_com_prolog(tipo_bolsa, media or 0, rendimento or 0)

        # Atualizar interface
        self.lbl_res_nome.configure(text=str(nome))
        self.lbl_res_bolsa.configure(text=f"{nome_bolsa} ({tipo_bolsa})")
        self.lbl_res_media.configure(text=f"{media:.1f}v / 20v" if media else "0.0v / 20v")
        self.lbl_res_renda.configure(text=f"{rendimento:,.0f} CVE" if rendimento else "0 CVE")

        # Atualizar status
        if elegivel:
            self.badge_status.configure(fg_color="#DEF7EC")
            self.lbl_status.configure(text="✓ APROVADO", text_color="#03543F")
            cor_motivos = "#10B981"
        else:
            self.badge_status.configure(fg_color="#FDE8E8")
            self.lbl_status.configure(text="✗ REJEITADO", text_color="#9B1C1C")
            cor_motivos = "#EF4444"

        # Atualizar motivos
        self.atualizar_motivos(motivos, cor_motivos)

        # Guardar histórico
        self.salvar_avaliacao(id_est, id_bolsa, elegivel, "\n".join(motivos))

    def atualizar_motivos(self, motivos, cor):
        """Atualiza a lista de motivos visualmente"""
        for widget in self.frame_motivos.winfo_children():
            widget.destroy()

        for motivo in motivos:
            lbl = ctk.CTkLabel(
                self.frame_motivos, text=motivo, font=("Segoe UI", 11),
                text_color=cor, justify="left", wraplength=400
            )
            lbl.pack(anchor="w", padx=5, pady=2)

    def salvar_avaliacao(self, id_est, id_bolsa, aprovado, motivos):
        """Salva a avaliação no histórico"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_avaliacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estudante_id INTEGER,
                    bolsa_id INTEGER,
                    resultado TEXT,
                    motivos TEXT,
                    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            resultado = "Aprovado" if aprovado else "Rejeitado"
            cursor.execute("""
                INSERT INTO historico_avaliacoes (estudante_id, bolsa_id, resultado, motivos)
                VALUES (?, ?, ?, ?)
            """, (id_est, id_bolsa, resultado, motivos))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar avaliação: {e}")

    def carregar_dados_combos(self):
        """Carrega os dados das bolsas e dos estudantes do Banco de Dados para os Comboboxes"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            # 1. Carregar Estudantes (guardando ID e Nome)
            cursor.execute("SELECT id, nome FROM estudantes ORDER BY nome ASC")
            dados_estudantes = cursor.fetchall()
            self.lista_estudantes = dados_estudantes # Salva a tupla (id, nome)
            
            # Gera a lista de strings para exibir no Combobox (Ex: "1 - João Silva")
            nomes_estudantes = [f"{id_est} - {nome}" for id_est, nome in dados_estudantes]
            if hasattr(self, 'combo_estudante'):  # Verifica se o componente existe na UI
                if nomes_estudantes:
                    self.combo_estudante.configure(values=nomes_estudantes)
                    self.combo_estudante.set(nomes_estudantes[0])
                else:
                    self.combo_estudante.configure(values=["Nenhum estudante cadastrado"])
                    self.combo_estudante.set("Nenhum estudante cadastrado")

            # 2. Carregar Bolsas
            cursor.execute("SELECT id, nome FROM bolsas WHERE estado = 'Ativa' ORDER BY nome ASC")
            dados_bolsas = cursor.fetchall()
            self.lista_bolsas = dados_bolsas # Salva a tupla (id, nome)
            
            # Gera a lista de strings para exibir no Combobox (Ex: "Merito")
            nomes_bolsas = [nome for _, nome in dados_bolsas]
            if hasattr(self, 'combo_bolsa'):  # Verifica se o componente existe na UI
                if nomes_bolsas:
                    self.combo_bolsa.configure(values=nomes_bolsas)
                    self.combo_bolsa.set(nomes_bolsas[0])
                else:
                    self.combo_bolsa.configure(values=["Nenhuma bolsa ativa"])
                    self.combo_bolsa.set("Nenhuma bolsa ativa")

            conn.close()
            print("✓ Dados dos Comboboxes recarregados com sucesso.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados para seleção:\n{str(e)}")
            
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

        # Container do Status de Aprovação
        ctk.CTkLabel(card_direito, text="Estado da Elegibilidade", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(30, 6))

        self.badge_status = ctk.CTkFrame(card_direito, fg_color="#F3F4F6", height=65, corner_radius=10)
        self.badge_status.pack(fill="x", padx=30, pady=(0, 15))
        self.badge_status.pack_propagate(False)

        self.lbl_status = ctk.CTkLabel(
            self.badge_status, text="AGUARDANDO SIMULAÇÃO",
            font=("Segoe UI", 15, "bold"), text_color="#4B5563"
        )
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")

        # Seção de Motivos
        ctk.CTkLabel(card_direito, text="Análise de Elegibilidade", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(15, 8))

        self.frame_motivos = ctk.CTkFrame(card_direito, fg_color="#F9FAFB", corner_radius=8, border_width=1, border_color="#E5E7EB")
        self.frame_motivos.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Mensagem inicial
        ctk.CTkLabel(
            self.frame_motivos, text="Clique em 'Processar Avaliação' para ver a análise detalhada.",
            font=("Segoe UI", 11), text_color="#9CA3AF"
        ).pack(anchor="w", padx=10, pady=10)