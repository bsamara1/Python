# interface/admin/relatorios.py
import customtkinter as ctk
from tkinter import messagebox

class RelatoriosPage(ctk.CTkFrame):
    """Página de Relatórios com Design Moderno e Fiel à Imagem de Referência"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.criar_interface()

    def exportar(self, tipo_relatorio, formato):
        """Dispara uma notificação limpa simulando a exportação de dados"""
        messagebox.showinfo(
            "Exportação Concluída", 
            f"O relatório de {tipo_relatorio} foi exportado com sucesso no formato {formato}."
        )

    def criar_interface(self):
        # 1. CABEÇALHO DA PÁGINA
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=30, pady=(25, 15))

        lbl_titulo = ctk.CTkLabel(frame_topo, text="Relatórios & Estatísticas", font=("Segoe UI", 24, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_topo, text="Consulte gráficos analíticos, métricas de desempenho e exporte relatórios gerenciais.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(4, 0))

        # 2. SECCÃO DE METRICAS RÁPIDAS (Cards de Resumo Superior)
        frame_metricas = ctk.CTkFrame(self, fg_color="transparent")
        frame_metricas.pack(fill="x", padx=20, pady=5)
        frame_metricas.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.criar_mini_card(frame_metricas, 0, "Taxa de Aprovação", "84.2%", "#ECFFF0", "#03543F")
        self.criar_mini_card(frame_metricas, 1, "Total Investido", "4.2M CVE", "#EEF4FF", "#1E40AF")
        self.criar_mini_card(frame_metricas, 2, "Bolsas Ativas", "124", "#FFF8EA", "#92400E")
        self.criar_mini_card(frame_metricas, 3, "Tempo Médio Análise", "2.4 Dias", "#F6EEFF", "#6B21A8")

        # 3. CONTAINER DOS GRÁFICOS E ANÁLISES (Duas Colunas Perfeitas)
        container_graficos = ctk.CTkFrame(self, fg_color="transparent")
        container_graficos.pack(fill="both", expand=True, padx=20, pady=15)
        container_graficos.grid_columnconfigure(0, weight=1, uniform="coluna_rel")
        container_graficos.grid_columnconfigure(1, weight=1, uniform="coluna_rel")
        container_graficos.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # COLUNA ESQUERDA: DISTRIBUIÇÃO POR CATEGORIA (GRÁFICO SIMULADO)
        # ----------------------------------------------------
        card_esq = ctk.CTkFrame(container_graficos, fg_color="white", corner_radius=14, border_width=1, border_color="#E5E7EB")
        card_esq.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(card_esq, text="Distribuição de Bolsas por Tipo", font=("Segoe UI", 16, "bold"), text_color="#111827").pack(anchor="w", padx=25, pady=(25, 5))
        ctk.CTkLabel(card_esq, text="Proporção atual do orçamento alocado.", font=("Segoe UI", 12), text_color="#6B7280").pack(anchor="w", padx=25, pady=(0, 20))

        # Barras Analíticas Verticais / Horizontais com Barras de Progresso Reais
        categorias = [
            ("Bolsas de Mérito Académico", 0.65, "65%", "#3B82F6"),
            ("Bolsas de Apoio Social", 0.45, "45%", "#10B981"),
            ("Bolsas de Incentivo ao Desporto", 0.25, "25%", "#F59E0B"),
            ("Bolsas de Excelência Científica", 0.15, "15%", "#8B5CF6")
        ]

        for nome, perc, txt_perc, cor_barra in categorias:
            lbl_f = ctk.CTkFrame(card_esq, fg_color="transparent")
            lbl_f.pack(fill="x", padx=25, pady=8)
            
            ctk.CTkLabel(lbl_f, text=nome, font=("Segoe UI", 13), text_color="#374151").pack(side="left")
            ctk.CTkLabel(lbl_f, text=txt_perc, font=("Segoe UI", 13, "bold"), text_color="#111827").pack(side="right")
            
            pbar = ctk.CTkProgressBar(card_esq, height=8, corner_radius=4, progress_color=cor_barra, fg_color="#F3F4F6")
            pbar.pack(fill="x", padx=25, pady=(2, 12))
            pbar.set(perc)

        # Divisor de Espaço Automático
        ctk.CTkFrame(card_esq, fg_color="transparent", height=1).pack(fill="both", expand=True)

        # Botão de Exportação Inferior
        btn_exp_esq = ctk.CTkButton(
            card_esq, text="Exportar Dados de Alocação", font=("Segoe UI", 13, "bold"),
            fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#374151",
            height=42, corner_radius=8, command=lambda: self.exportar("Alocação de Bolsas", "PDF")
        )
        btn_exp_esq.pack(fill="x", padx=25, pady=(0, 25))


        # ----------------------------------------------------
        # COLUNA DIREITA: RELATÓRIO DE DESEMPENHO E EXPORTAÇÃO GLOBAL
        # ----------------------------------------------------
        card_dir = ctk.CTkFrame(container_graficos, fg_color="white", corner_radius=14, border_width=1, border_color="#E5E7EB")
        card_dir.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(card_dir, text="Ações e Exportação Consolidada", font=("Segoe UI", 16, "bold"), text_color="#111827").pack(anchor="w", padx=25, pady=(25, 5))
        ctk.CTkLabel(card_dir, text="Gere relatórios completos para auditoria institucional.", font=("Segoe UI", 12), text_color="#6B7280").pack(anchor="w", padx=25, pady=(0, 25))

        # Bloco de Relatório Académico
        f_rel1 = ctk.CTkFrame(card_dir, fg_color="#F8FAFC", corner_radius=10, border_width=1, border_color="#E2E8F0")
        f_rel1.pack(fill="x", padx=25, pady=10)
        
        lbl_t1 = ctk.CTkLabel(f_rel1, text="Relatório Anual de Desempenho", font=("Segoe UI", 13, "bold"), text_color="#1E293B")
        lbl_t1.pack(anchor="w", padx=15, pady=(12, 2))
        lbl_d1 = ctk.CTkLabel(f_rel1, text="Contém médias ponderadas, taxas de retenção e evolução do rendimento estudantil.", font=("Segoe UI", 11), text_color="#64748B", justify="left", wraplength=320)
        lbl_d1.pack(anchor="w", padx=15, pady=(0, 12))
        
        btn_r1 = ctk.CTkButton(f_rel1, text="Gerar PDF Académico", font=("Segoe UI", 12, "bold"), fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white", height=34, width=160, corner_radius=6, command=lambda: self.exportar("Desempenho Académico", "PDF"))
        btn_r1.pack(anchor="e", padx=15, pady=(0, 12))

        # Bloco de Relatório Financeiro
        f_rel2 = ctk.CTkFrame(card_dir, fg_color="#F8FAFC", corner_radius=10, border_width=1, border_color="#E2E8F0")
        f_rel2.pack(fill="x", padx=25, pady=10)
        
        lbl_t2 = ctk.CTkLabel(f_rel2, text="Balancete Financeiro OGE", font=("Segoe UI", 13, "bold"), text_color="#1E293B")
        lbl_t2.pack(anchor="w", padx=15, pady=(12, 2))
        lbl_d2 = ctk.CTkLabel(f_rel2, text="Demonstrativo completo de repasses, pagamentos efetuados e saldo orçamental.", font=("Segoe UI", 11), text_color="#64748B", justify="left", wraplength=320)
        lbl_d2.pack(anchor="w", padx=15, pady=(0, 12))
        
        btn_r2 = ctk.CTkButton(f_rel2, text="Exportar Planilha Excel", font=("Segoe UI", 12, "bold"), fg_color="#10B981", hover_color="#059669", text_color="white", height=34, width=160, corner_radius=6, command=lambda: self.exportar("Balancete Financeiro", "Excel"))
        btn_r2.pack(anchor="e", padx=15, pady=(0, 12))

    def criar_mini_card(self, parent, col, titulo, valor, cor_fundo, cor_texto):
        """Cria um card premium compacto para exibição rápida de métricas no topo"""
        card = ctk.CTkFrame(parent, fg_color=cor_fundo, corner_radius=12, height=85)
        card.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
        card.pack_propagate(False)

        # Centralização harmoniosa do conteúdo interno
        lbl_val = ctk.CTkLabel(card, text=valor, font=("Segoe UI", 20, "bold"), text_color=cor_texto)
        lbl_val.place(relx=0.5, rely=0.38, anchor="center")

        lbl_tit = ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 11, "bold"), text_color="#6B7280")
        lbl_tit.place(relx=0.5, rely=0.72, anchor="center")