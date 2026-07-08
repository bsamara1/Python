# candidaturas.py - Versão com ícones
import customtkinter as ctk
from PIL import Image
import os
import sys
import sqlite3
from tkinter import messagebox
from datetime import datetime


class CandidaturasPage(ctk.CTkFrame):
    """Página de Candidaturas com ícones na sidebar"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.pack(fill="both", expand=True)

        self.caminho_db = self.obter_caminho_db()
        self.candidaturas = []
        self.candidaturas_filtradas = []

        self.carregar_candidaturas()
        self.carregar_imagens()
        self.criar_interface()

    def obter_caminho_db(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'database', 'sibes.db')

    def carregar(self, caminho, tamanho):
        try:
            if os.path.exists(caminho):
                return ctk.CTkImage(Image.open(caminho), size=tamanho)
        except Exception as e:
            print(f"Erro ao carregar {caminho}: {e}")
        return None

    def carregar_imagens(self):
        self.icon_casa = self.carregar("assets/casa.png", (20, 20))
        self.icon_perfil = self.carregar("assets/perfil.png", (20, 20))
        self.icon_bolsa = self.carregar("assets/bolsa.png", (20, 20))
        self.icon_candidatura = self.carregar("assets/candidatura.png", (20, 20))
        self.icon_avaliacao = self.carregar("assets/avaliacao.png", (20, 20))
        self.icon_relatorio = self.carregar("assets/relatorio.png", (20, 20))
        self.icon_utilizadores = self.carregar("assets/utilizadores.png", (20, 20))
        self.icon_definicao = self.carregar("assets/definicao.png", (20, 20))
        self.icon_logout = self.carregar("assets/sair.png", (20, 20))
        self.logo = self.carregar("assets/logo.png", (40, 40))

    def carregar_candidaturas(self):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, e.nome, b.nome, c.data_candidatura, c.estado
                FROM candidaturas c
                JOIN estudantes e ON c.estudante_id = e.id
                JOIN bolsas b ON c.bolsa_id = b.id
                ORDER BY c.data_candidatura DESC
            """)
            resultados = cursor.fetchall()
            conn.close()

            self.candidaturas = [
                {
                    'id': row[0], 'estudante': row[1], 'bolsa': row[2],
                    'data': row[3], 'estado': row[4]
                } for row in resultados
            ]
            self.candidaturas_filtradas = self.candidaturas.copy()
        except sqlite3.Error as e:
            print(f"⚠️ Erro ao carregar candidaturas: {e}")
            self.candidaturas = []
            self.candidaturas_filtradas = []

    def criar_interface(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.criar_sidebar()
        self.criar_conteudo()

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.container, width=240, fg_color="#0B2A4A"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        topo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(25, 35))

        ctk.CTkLabel(topo, image=self.logo, text="").grid(
            row=0, column=0, rowspan=2, padx=10
        )
        ctk.CTkLabel(
            topo, text="SIBES",
            font=("Segoe UI", 20, "bold"), text_color="white"
        ).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(
            topo, text="Sistema Inteligente\nBolsas Sustentáveis",
            text_color="#D6E4F0", justify="left"
        ).grid(row=1, column=1, sticky="w")

        self.botoes_menu = {}
        icones_menu = {
            "Painel Principal": self.icon_casa,
            "Estudantes": self.icon_perfil,
            "Bolsas": self.icon_bolsa,
            "Candidaturas": self.icon_candidatura,
            "Avaliação": self.icon_avaliacao,
            "Relatórios": self.icon_relatorio,
            "Utilizadores": self.icon_utilizadores,
            "Definições": self.icon_definicao,
            "Perfil": self.icon_perfil
        }

        for item in icones_menu.keys():
            btn = ctk.CTkButton(
                self.sidebar,
                text=item,
                image=icones_menu[item],
                compound="left",
                fg_color="#11457B" if item == "Candidaturas" else "transparent",
                hover_color="#11457B",
                anchor="w",
                height=45,
                font=("Segoe UI", 13),
                command=lambda i=item: self.menu_click(i)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.botoes_menu[item] = btn

        ctk.CTkFrame(
            self.sidebar, height=1, fg_color="#35506E"
        ).pack(side="bottom", fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(
            self.sidebar,
            text="Terminar Sessão",
            image=self.icon_logout,
            compound="left",
            fg_color="transparent",
            hover_color="#2A3F5F",
            text_color="#FF6B6B",
            anchor="w",
            height=45,
            command=self.terminar_sessao
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def menu_click(self, item):
        for btn in self.botoes_menu.values():
            btn.configure(fg_color="transparent")
        self.botoes_menu[item].configure(fg_color="#11457B")

        if hasattr(self.master, 'trocar_pagina'):
            self.master.trocar_pagina(item)
        else:
            print(f"🔀 Navegando para: {item}")

    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            self.master.destroy()
            try:
                from login import Login
                login_root = ctk.CTk()
                Login(login_root)
                login_root.mainloop()
            except:
                print("👋 Sessão terminada")

    def criar_conteudo(self):
        self.main = ctk.CTkFrame(self.container, fg_color="#F4F6FB")
        self.main.pack(side="left", fill="both", expand=True, padx=25, pady=20)

        # Topo
        topbar = ctk.CTkFrame(self.main, fg_color="transparent")
        topbar.pack(fill="x")

        title_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="📋 Candidaturas",
            font=("Segoe UI", 28, "bold"),
            text_color="#0B2A4A"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=f"Consultar e gerir candidaturas submetidas. ({len(self.candidaturas)})",
            text_color="#6B7280",
            font=("Segoe UI", 13)
        ).pack(anchor="w")

        add_btn = ctk.CTkButton(
            topbar,
            text="➕ Nova Candidatura",
            command=self.nova_candidatura,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            width=180,
            height=42,
            corner_radius=8,
            font=("Segoe UI", 13, "bold")
        )
        add_btn.pack(side="right")

        ctk.CTkFrame(self.main, height=1, fg_color="#D1D5DB").pack(fill="x", pady=20)

        # Filtros
        self.criar_filtros()

        # Tabela
        self.criar_tabela()

        # Footer
        self.criar_footer()

    def criar_filtros(self):
        filter_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 15))

        self.filtro_estado = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "Pendente", "Aprovada", "Rejeitada", "Em Análise"],
            width=180,
            height=42,
            command=self.aplicar_filtros
        )
        self.filtro_estado.pack(side="left")
        self.filtro_estado.set("Todos")

        self.filtro_bolsa = ctk.CTkComboBox(
            filter_frame,
            values=self.obter_bolsas(),
            width=200,
            height=42,
            command=self.aplicar_filtros
        )
        self.filtro_bolsa.pack(side="left", padx=(15, 0))
        self.filtro_bolsa.set("Todas")

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="🔍 Pesquisar estudante...",
            height=42
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(15, 0))
        self.search_entry.bind("<KeyRelease>", self.aplicar_filtros)

        ctk.CTkButton(
            filter_frame,
            text="🔄 Limpar",
            width=100,
            height=42,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.limpar_filtros
        ).pack(side="left", padx=(10, 0))

    def obter_bolsas(self):
        bolsas = set()
        for c in self.candidaturas:
            bolsas.add(c['bolsa'])
        return ["Todas"] + sorted(list(bolsas))

    def aplicar_filtros(self, event=None):
        estado = self.filtro_estado.get()
        bolsa = self.filtro_bolsa.get()
        pesquisa = self.search_entry.get().lower().strip()

        self.candidaturas_filtradas = []
        for c in self.candidaturas:
            if estado != "Todos" and c['estado'] != estado:
                continue
            if bolsa != "Todas" and c['bolsa'] != bolsa:
                continue
            if pesquisa and pesquisa not in c['estudante'].lower():
                continue
            self.candidaturas_filtradas.append(c)

        self.atualizar_tabela()
        self.atualizar_footer()

    def limpar_filtros(self):
        self.filtro_estado.set("Todos")
        self.filtro_bolsa.set("Todas")
        self.search_entry.delete(0, "end")
        self.candidaturas_filtradas = self.candidaturas.copy()
        self.atualizar_tabela()
        self.atualizar_footer()

    def criar_tabela(self):
        self.table_card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        self.table_card.pack(fill="both", expand=True)

        headers = ["ID", "Estudante", "Bolsa", "Data", "Estado", "Ações"]
        widths = [60, 200, 250, 150, 150, 120]

        header = ctk.CTkFrame(self.table_card, fg_color="#F8FAFC", height=55)
        header.pack(fill="x")

        for texto, largura in zip(headers, widths):
            ctk.CTkLabel(
                header, text=texto, width=largura,
                font=("Segoe UI", 12, "bold"), text_color="#334155"
            ).pack(side="left", padx=5, pady=15)

        ctk.CTkFrame(self.table_card, height=1, fg_color="#E5E7EB").pack(fill="x")

        self.corpo_tabela = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.corpo_tabela.pack(fill="both", expand=True)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.corpo_tabela.winfo_children():
            widget.destroy()

        if not self.candidaturas_filtradas:
            ctk.CTkLabel(
                self.corpo_tabela,
                text="📭 Nenhuma candidatura encontrada",
                font=("Segoe UI", 16),
                text_color="#6B7280"
            ).pack(pady=50)
            return

        cores_estado = {
            "Aprovada": {"bg": "#DCFCE7", "fg": "#16A34A"},
            "Rejeitada": {"bg": "#FEE2E2", "fg": "#DC2626"},
            "Pendente": {"bg": "#FEF3C7", "fg": "#D97706"},
            "Em Análise": {"bg": "#DBEAFE", "fg": "#2563EB"}
        }

        for idx, c in enumerate(self.candidaturas_filtradas):
            row = ctk.CTkFrame(
                self.corpo_tabela,
                fg_color="#F9FAFB" if idx % 2 == 0 else "white",
                height=65
            )
            row.pack(fill="x")

            ctk.CTkLabel(row, text=str(c['id']), width=60, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=c['estudante'], width=200, anchor="w", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=c['bolsa'], width=250, anchor="w").pack(side="left", padx=5)

            data_formatada = self.formatar_data(c['data'])
            ctk.CTkLabel(row, text=data_formatada, width=150, anchor="w").pack(side="left", padx=5)

            cor = cores_estado.get(c['estado'], {"bg": "#F3F4F6", "fg": "#6B7280"})
            ctk.CTkLabel(
                row,
                text=c['estado'],
                fg_color=cor["bg"],
                text_color=cor["fg"],
                corner_radius=12,
                width=100,
                height=28
            ).pack(side="left", padx=5)

            acoes = ctk.CTkFrame(row, fg_color="transparent")
            acoes.pack(side="left", padx=5)

            ctk.CTkButton(
                acoes, text="👁️", width=35, height=35,
                fg_color="#EFF6FF", hover_color="#DBEAFE", text_color="#2563EB",
                command=lambda ca=c: self.visualizar_candidatura(ca)
            ).pack(side="left", padx=2)

            if c['estado'] in ["Pendente", "Em Análise"]:
                ctk.CTkButton(
                    acoes, text="✅", width=35, height=35,
                    fg_color="#DCFCE7", hover_color="#BBF7D0", text_color="#16A34A",
                    command=lambda ca=c: self.aprovar_candidatura(ca)
                ).pack(side="left", padx=2)

                ctk.CTkButton(
                    acoes, text="❌", width=35, height=35,
                    fg_color="#FEE2E2", hover_color="#FECACA", text_color="#DC2626",
                    command=lambda ca=c: self.rejeitar_candidatura(ca)
                ).pack(side="left", padx=2)

            ctk.CTkFrame(self.corpo_tabela, height=1, fg_color="#E5E7EB").pack(fill="x")

    def formatar_data(self, data):
        try:
            if isinstance(data, str):
                dt = datetime.strptime(data, '%Y-%m-%d')
                return dt.strftime('%d/%m/%Y')
            return str(data)
        except:
            return str(data)

    def criar_footer(self):
        self.footer = ctk.CTkFrame(self.main, fg_color="transparent")
        self.footer.pack(fill="x", pady=15)
        self.atualizar_footer()

    def atualizar_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

        total = len(self.candidaturas_filtradas)
        total_geral = len(self.candidaturas)

        pendentes = len([c for c in self.candidaturas_filtradas if c['estado'] == 'Pendente'])
        aprovadas = len([c for c in self.candidaturas_filtradas if c['estado'] == 'Aprovada'])

        info_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        info_frame.pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f"📊 Mostrando {total} de {total_geral} candidaturas",
            text_color="#334155",
            font=("Segoe UI", 12)
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f" | ⏳ {pendentes} pendentes",
            text_color="#D97706",
            font=("Segoe UI", 12)
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f" | ✅ {aprovadas} aprovadas",
            text_color="#16A34A",
            font=("Segoe UI", 12)
        ).pack(side="left")

    # ==========================================
    # AÇÕES
    # ==========================================
    def nova_candidatura(self):
        messagebox.showinfo("Info", "📝 Formulário de candidatura em desenvolvimento")

    def visualizar_candidatura(self, candidatura):
        messagebox.showinfo("Visualizar", f"Candidatura #{candidatura['id']}\nEstudante: {candidatura['estudante']}\nBolsa: {candidatura['bolsa']}")

    def aprovar_candidatura(self, candidatura):
        if messagebox.askyesno("Aprovar", f"Aprovar candidatura de {candidatura['estudante']}?"):
            self.atualizar_estado(candidatura['id'], "Aprovada")

    def rejeitar_candidatura(self, candidatura):
        if messagebox.askyesno("Rejeitar", f"Rejeitar candidatura de {candidatura['estudante']}?"):
            self.atualizar_estado(candidatura['id'], "Rejeitada")

    def atualizar_estado(self, candidatura_id, novo_estado):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE candidaturas
                SET estado = ?, data_atualizacao = datetime('now')
                WHERE id = ?
            """, (novo_estado, candidatura_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Candidatura {novo_estado.lower()}!")

            self.carregar_candidaturas()
            self.aplicar_filtros()
            self.filtro_bolsa.configure(values=self.obter_bolsas())

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("SIBES - Candidaturas")
    root.state("zoomed")
    CandidaturasPage(root)
    root.mainloop()