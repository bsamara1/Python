import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from database.database import conectar
from interface.admin.perfilUtilizador import PerfilUtilizador
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DashboardEstudante(ctk.CTk):
    """Dashboard Completo do Estudante - SIBES v1.0"""

    def __init__(self, parent=None, id_utilizador_logado=None):
        super().__init__()

        self.parent = parent
        self.id_utilizador_logado = id_utilizador_logado
        self.title("SIBES - Painel do Estudante")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        # Carregar dados do utilizador
        self.nome_usuario = self.obter_nome()
        self.email_usuario = self.obter_email()

        self.criar_interface()

    # ========================================
    # MÉTODOS AUXILIARES
    # ========================================

    def obter_nome(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM utilizadores WHERE id = ?", (self.id_utilizador_logado,))
            resultado = cursor.fetchone()
            conn.close()
            return resultado[0] if resultado else "Utilizador"
        except:
            return "Utilizador"

    def obter_email(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM utilizadores WHERE id = ?", (self.id_utilizador_logado,))
            resultado = cursor.fetchone()
            conn.close()
            return resultado[0] if resultado else "email@example.com"
        except:
            return "email@example.com"

    def limpar_area(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    def destacar_menu(self, nome):
        for texto, btn in self.botoes_menu.items():
            if texto == nome:
                btn.configure(fg_color="#11457B")
            else:
                btn.configure(fg_color="transparent")

    # ========================================
    # INTERFACE PRINCIPAL
    # ========================================

    def criar_interface(self):
        # Container principal
        container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        container.pack(fill="both", expand=True)

        # ===== SIDEBAR =====
        sidebar = ctk.CTkFrame(container, width=250, fg_color="#0B2A4A", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        ctk.CTkLabel(
            sidebar,
            text="🎓 SIBES",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=30, padx=20, anchor="w")

        ctk.CTkLabel(
            sidebar,
            text="Sistema de Bolsas",
            font=("Segoe UI", 10),
            text_color="#A0AEC0"
        ).pack(padx=20, anchor="w")

        # Separador
        ctk.CTkFrame(sidebar, height=1, fg_color="#35506E").pack(fill="x", pady=20)

        # Menu de Navegação
        self.botoes_menu = {}
        menu_items = [
            ("📊 Painel Principal", self.mostrar_painel),
            ("📝 Minhas Candidaturas", self.mostrar_minhas_candidaturas),
            ("💰 Bolsas Disponíveis", self.mostrar_bolsas),
            ("🧠 Avaliação Inteligente", self.mostrar_avaliacao),
            ("📄 Relatórios Pessoais", self.mostrar_relatorios),
            ("👤 Meu Perfil", self.mostrar_perfil)
        ]

        for texto, comando in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=texto,
                anchor="w",
                fg_color="transparent",
                hover_color="#11457B",
                text_color="white",
                height=45,
                command=comando
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.botoes_menu[texto] = btn

        # Separador final
        ctk.CTkFrame(sidebar, height=1, fg_color="#35506E").pack(fill="x", pady=20, side="bottom")

        # Botão Terminar Sessão
        ctk.CTkButton(
            sidebar,
            text="🚪 Terminar Sessão",
            anchor="w",
            fg_color="transparent",
            hover_color="#2A3F5F",
            text_color="#FF6B6B",
            height=45,
            command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=15)

        # ===== MAIN CONTENT =====
        main = ctk.CTkFrame(container, fg_color="#F4F6FB")
        main.pack(side="left", fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main, fg_color="white", height=80, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(
            header,
            text="Painel Principal",
            font=("Segoe UI", 24, "bold"),
            text_color="#142850"
        )
        self.label_titulo.pack(side="left", padx=30, pady=20)

        # Usuário info no header
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="right", padx=30, pady=20)

        ctk.CTkLabel(
            info_frame,
            text=f"👤 {self.nome_usuario}",
            font=("Segoe UI", 12, "bold"),
            text_color="#142850"
        ).pack(anchor="e")

        ctk.CTkLabel(
            info_frame,
            text=self.email_usuario,
            font=("Segoe UI", 10),
            text_color="#6B7280"
        ).pack(anchor="e")

        # Área de conteúdo
        self.area_conteudo = ctk.CTkScrollableFrame(main, fg_color="#F4F6FB")
        self.area_conteudo.pack(fill="both", expand=True, padx=30, pady=20)

        # Mostrar painel principal por padrão
        self.mostrar_painel()

    # ========================================
    # PÁGINAS
    # ========================================

    def mostrar_painel(self):
        """Painel Principal com resumo e candidaturas recentes"""
        self.destacar_menu("📊 Painel Principal")
        self.label_titulo.configure(text="Painel Principal")
        self.limpar_area()

        # Boas-vindas
        ctk.CTkLabel(
            self.area_conteudo,
            text=f"Bem-vindo, {self.nome_usuario}! 👋",
            font=("Segoe UI", 26, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            self.area_conteudo,
            text="Acompanhe suas candidaturas e oportunidades de bolsas",
            font=("Segoe UI", 12),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(0, 20))

        # Cartões de resumo
        self.criar_cards_resumo()

        # Gráfico de candidaturas
        self.criar_grafico_candidaturas()

        # Candidaturas recentes
        self.criar_lista_recentes()

    def mostrar_minhas_candidaturas(self):
        """Lista de candidaturas com tabela"""
        self.destacar_menu("📝 Minhas Candidaturas")
        self.label_titulo.configure(text="Minhas Candidaturas")
        self.limpar_area()

        ctk.CTkLabel(
            self.area_conteudo,
            text="📝 Minhas Candidaturas",
            font=("Segoe UI", 20, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 20))

        # Tabela de candidaturas
        self.criar_tabela_candidaturas()

    def mostrar_bolsas(self):
        """Bolsas disponíveis com pesquisa e filtros"""
        self.destacar_menu("💰 Bolsas Disponíveis")
        self.label_titulo.configure(text="Bolsas Disponíveis")
        self.limpar_area()

        ctk.CTkLabel(
            self.area_conteudo,
            text="💰 Bolsas Disponíveis",
            font=("Segoe UI", 20, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 20))

        # Pesquisa e filtros
        search_frame = ctk.CTkFrame(self.area_conteudo, fg_color="white", corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(search_frame, text="Pesquisar:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=15)
        ctk.CTkEntry(search_frame, placeholder_text="Digite nome da bolsa...").pack(side="left", padx=(0, 15), fill="x", expand=True)
        ctk.CTkButton(search_frame, text="🔍 Pesquisar", width=100).pack(side="left", padx=15)

        # Lista de bolsas (placeholder)
        ctk.CTkLabel(
            self.area_conteudo,
            text="Funcionalidade em desenvolvimento...",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        ).pack(pady=30)

    def mostrar_avaliacao(self):
        """Avaliação Inteligente com Prolog"""
        self.destacar_menu("🧠 Avaliação Inteligente")
        self.label_titulo.configure(text="Avaliação Inteligente")
        self.limpar_area()

        ctk.CTkLabel(
            self.area_conteudo,
            text="🧠 Avaliação Inteligente",
            font=("Segoe UI", 20, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(
            self.area_conteudo,
            text="Selecione uma candidatura para avaliar elegibilidade",
            font=("Segoe UI", 12),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(0, 20))

        # Funcionalidade em desenvolvimento
        ctk.CTkLabel(
            self.area_conteudo,
            text="Funcionalidade em desenvolvimento...",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        ).pack(pady=30)

    def mostrar_relatorios(self):
        """Relatórios Pessoais com gráficos"""
        self.destacar_menu("📄 Relatórios Pessoais")
        self.label_titulo.configure(text="Relatórios Pessoais")
        self.limpar_area()

        ctk.CTkLabel(
            self.area_conteudo,
            text="📄 Relatórios Pessoais",
            font=("Segoe UI", 20, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 20))

        # Funcionalidade em desenvolvimento
        ctk.CTkLabel(
            self.area_conteudo,
            text="Funcionalidade em desenvolvimento...",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        ).pack(pady=30)

    def mostrar_perfil(self):
        """Perfil do Estudante"""
        self.destacar_menu("👤 Meu Perfil")
        self.label_titulo.configure(text="")
        self.limpar_area()

        PerfilUtilizador(self.area_conteudo, self.id_utilizador_logado)

    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            self.destroy()

    # ========================================
    # COMPONENTES DO PAINEL PRINCIPAL
    # ========================================

    def criar_cards_resumo(self):
        """Cria cartões de resumo"""
        cards_frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 30))

        cards_data = [
            ("Candidaturas", "5", "#EEF4FF", "#1E40AF"),
            ("Pendentes", "2", "#FFF8EA", "#92400E"),
            ("Aprovadas", "2", "#ECFFF0", "#03543F"),
            ("Valor Total", "120.000 CVE", "#F6EEFF", "#6B21A8")
        ]

        for titulo, valor, cor_fundo, cor_texto in cards_data:
            card = ctk.CTkFrame(cards_frame, fg_color=cor_fundo, corner_radius=10, height=100)
            card.pack(side="left", fill="both", expand=True, padx=(0, 15))
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=valor, font=("Segoe UI", 20, "bold"), text_color=cor_texto).pack(pady=(10, 0))
            ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 11), text_color=cor_texto).pack(pady=(5, 10))

    def criar_grafico_candidaturas(self):
        """Cria gráfico de candidaturas"""
        fig = Figure(figsize=(6, 3), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)

        # Dados de exemplo
        estados = ['Aprovadas', 'Pendentes', 'Rejeitadas']
        valores = [2, 2, 1]
        cores = ['#10B981', '#F59E0B', '#EF4444']

        ax.pie(valores, labels=estados, autopct='%1.0f%%', colors=cores, startangle=90)
        ax.set_title("Estado das Candidaturas")

        canvas = FigureCanvasTkAgg(fig, master=self.area_conteudo)
        canvas.get_tk_widget().pack(fill="x", pady=(0, 30))

    def criar_lista_recentes(self):
        """Cria lista de candidaturas recentes"""
        ctk.CTkLabel(
            self.area_conteudo,
            text="Candidaturas Recentes",
            font=("Segoe UI", 14, "bold"),
            text_color="#142850"
        ).pack(anchor="w", pady=(0, 15))

        # Tabela de candidaturas recentes
        columns = ("Código", "Bolsa", "Data", "Estado", "Valor")
        tree = ttk.Treeview(self.area_conteudo, columns=columns, height=5, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Dados de exemplo
        tree.insert('', 'end', values=('C001', 'Bolsa Social', '20/06/2026', 'Pendente', '40.000 CVE'))
        tree.insert('', 'end', values=('C002', 'Bolsa Mérito', '15/06/2026', 'Aprovada', '60.000 CVE'))

        tree.pack(fill="x")

    def criar_tabela_candidaturas(self):
        """Cria tabela detalhada de candidaturas"""
        columns = ("Código", "Bolsa", "Data", "Estado", "Valor", "Ações")
        tree = ttk.Treeview(self.area_conteudo, columns=columns, height=10, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Dados de exemplo
        tree.insert('', 'end', values=('C001', 'Bolsa Social', '20/06/2026', 'Pendente', '40.000 CVE', '👁️ Ver'))
        tree.insert('', 'end', values=('C002', 'Bolsa Mérito', '15/06/2026', 'Aprovada', '60.000 CVE', '👁️ Ver'))

        tree.pack(fill="both", expand=True)


# Alias para compatibilidade com login.py
class App(DashboardEstudante):
    def __init__(self, parent=None, id_utilizador_logado=None):
        super().__init__(parent, id_utilizador_logado)


if __name__ == "__main__":
    app = DashboardEstudante()
    app.mainloop()
