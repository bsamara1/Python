# bolsas.py
import customtkinter as ctk
from PIL import Image
import os
import sys
import sqlite3
from tkinter import messagebox


class BolsasPage(ctk.CTkFrame):
    """Página de Gestão de Bolsas com ícones na sidebar"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.pack(fill="both", expand=True)

        self.caminho_db = self.obter_caminho_db()
        self.bolsas = []
        self.bolsas_filtradas = []

        self.carregar_bolsas()
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

    def carregar_bolsas(self):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, tipo, valor, vagas, estado, descricao
                FROM bolsas ORDER BY nome
            """)
            resultados = cursor.fetchall()
            conn.close()

            self.bolsas = [
                {
                    'id': row[0], 'nome': row[1], 'tipo': row[2],
                    'valor': row[3], 'vagas': row[4], 'estado': row[5],
                    'descricao': row[6]
                } for row in resultados
            ]
            self.bolsas_filtradas = self.bolsas.copy()
        except sqlite3.Error as e:
            print(f"⚠️ Erro ao carregar bolsas: {e}")
            self.bolsas = []
            self.bolsas_filtradas = []

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
                fg_color="#11457B" if item == "Bolsas" else "transparent",
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
            text="🎓 Bolsas",
            font=("Segoe UI", 28, "bold"),
            text_color="#0B2A4A"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=f"Gerir bolsas de estudo disponíveis. ({len(self.bolsas)} bolsas)",
            text_color="#6B7280",
            font=("Segoe UI", 13)
        ).pack(anchor="w")

        add_btn = ctk.CTkButton(
            topbar,
            text="➕ Adicionar Bolsa",
            command=self.abrir_form_bolsa,
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

        self.filtro_tipo = ctk.CTkComboBox(
            filter_frame,
            values=["Todos os tipos", "Académica", "Social", "Desportiva", "Especial"],
            width=180,
            height=42,
            command=self.aplicar_filtros
        )
        self.filtro_tipo.pack(side="left")
        self.filtro_tipo.set("Todos os tipos")

        self.filtro_estado = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "Ativa", "Encerrada", "Em Breve"],
            width=150,
            height=42,
            command=self.aplicar_filtros
        )
        self.filtro_estado.pack(side="left", padx=(15, 0))
        self.filtro_estado.set("Todos")

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="🔍 Pesquisar bolsa...",
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

    def aplicar_filtros(self, event=None):
        tipo = self.filtro_tipo.get()
        estado = self.filtro_estado.get()
        pesquisa = self.search_entry.get().lower().strip()

        self.bolsas_filtradas = []
        for b in self.bolsas:
            if tipo != "Todos os tipos" and b['tipo'] != tipo:
                continue
            if estado != "Todos" and b['estado'] != estado:
                continue
            if pesquisa and pesquisa not in b['nome'].lower():
                continue
            self.bolsas_filtradas.append(b)

        self.atualizar_tabela()
        self.atualizar_footer()

    def limpar_filtros(self):
        self.filtro_tipo.set("Todos os tipos")
        self.filtro_estado.set("Todos")
        self.search_entry.delete(0, "end")
        self.bolsas_filtradas = self.bolsas.copy()
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

        headers = ["ID", "Nome", "Tipo", "Valor (Kz)", "Vagas", "Estado", "Ações"]
        widths = [60, 250, 180, 140, 120, 150, 120]

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

        if not self.bolsas_filtradas:
            ctk.CTkLabel(
                self.corpo_tabela,
                text="📭 Nenhuma bolsa encontrada",
                font=("Segoe UI", 16),
                text_color="#6B7280"
            ).pack(pady=50)
            return

        cores_tipo = {
            "Académica": "#2563EB",
            "Social": "#16A34A",
            "Desportiva": "#D97706",
            "Especial": "#7C3AED"
        }

        cores_estado = {
            "Ativa": {"bg": "#DCFCE7", "fg": "#16A34A"},
            "Encerrada": {"bg": "#FEE2E2", "fg": "#DC2626"},
            "Em Breve": {"bg": "#DBEAFE", "fg": "#2563EB"}
        }

        for idx, b in enumerate(self.bolsas_filtradas):
            row = ctk.CTkFrame(
                self.corpo_tabela,
                fg_color="#F9FAFB" if idx % 2 == 0 else "white",
                height=65
            )
            row.pack(fill="x")

            ctk.CTkLabel(row, text=str(b['id']), width=60, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=b['nome'], width=250, anchor="w", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=b['tipo'], width=180, anchor="w", text_color=cores_tipo.get(b['tipo'], "#6B7280")).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{b['valor']:,.2f} Kz" if b['valor'] else "-", width=140, anchor="w").pack(side="left", padx=5)
            
            vagas = b.get('vagas', 0) or 0
            cor_vagas = "#16A34A" if vagas > 10 else "#D97706" if vagas > 0 else "#DC2626"
            ctk.CTkLabel(row, text=str(vagas), width=120, anchor="w", text_color=cor_vagas).pack(side="left", padx=5)

            cor = cores_estado.get(b['estado'], {"bg": "#F3F4F6", "fg": "#6B7280"})
            ctk.CTkLabel(
                row,
                text=b['estado'],
                fg_color=cor["bg"],
                text_color=cor["fg"],
                corner_radius=12,
                width=100,
                height=28
            ).pack(side="left", padx=5)

            acoes = ctk.CTkFrame(row, fg_color="transparent")
            acoes.pack(side="left", padx=5)

            ctk.CTkButton(
                acoes, text="✏️", width=35, height=35,
                fg_color="#EFF6FF", hover_color="#DBEAFE", text_color="#2563EB",
                command=lambda bo=b: self.editar_bolsa(bo)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes, text="🗑️", width=35, height=35,
                fg_color="#FEF2F2", hover_color="#FEE2E2", text_color="#EF4444",
                command=lambda bo=b: self.eliminar_bolsa(bo)
            ).pack(side="left", padx=2)

            if b['estado'] == "Ativa":
                btn_texto, cor_btn, cor_text, cmd = "⏸", "#FEF3C7", "#D97706", "Encerrada"
            else:
                btn_texto, cor_btn, cor_text, cmd = "▶️", "#DCFCE7", "#16A34A", "Ativa"

            ctk.CTkButton(
                acoes, text=btn_texto, width=35, height=35,
                fg_color=cor_btn, hover_color="#F3F4F6", text_color=cor_text,
                command=lambda bo=b, estado=cmd: self.alternar_estado(bo, estado)
            ).pack(side="left", padx=2)

            ctk.CTkFrame(self.corpo_tabela, height=1, fg_color="#E5E7EB").pack(fill="x")

    def criar_footer(self):
        self.footer = ctk.CTkFrame(self.main, fg_color="transparent")
        self.footer.pack(fill="x", pady=15)
        self.atualizar_footer()

    def atualizar_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

        total = len(self.bolsas_filtradas)
        total_geral = len(self.bolsas)
        ativas = len([b for b in self.bolsas_filtradas if b['estado'] == 'Ativa'])
        total_vagas = sum(b.get('vagas', 0) or 0 for b in self.bolsas_filtradas)

        info_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        info_frame.pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f"📊 Mostrando {total} de {total_geral} bolsas",
            text_color="#334155",
            font=("Segoe UI", 12)
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f" | 🟢 {ativas} ativas",
            text_color="#16A34A",
            font=("Segoe UI", 12)
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f" | 📝 {total_vagas} vagas",
            text_color="#334155",
            font=("Segoe UI", 12)
        ).pack(side="left")

    # ==========================================
    # CRUD OPERATIONS (resumido para brevidade)
    # ==========================================
    def abrir_form_bolsa(self, bolsa=None):
        # Implementação similar à de estudantes
        pass

    def guardar_bolsa(self, modal, entries, estado_entry, bolsa=None):
        # Implementação similar à de estudantes
        pass

    def editar_bolsa(self, bolsa):
        self.abrir_form_bolsa(bolsa)

    def eliminar_bolsa(self, bolsa):
        if messagebox.askyesno("Confirmar", f"Eliminar {bolsa['nome']}?"):
            try:
                conn = sqlite3.connect(self.caminho_db)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bolsas WHERE id=?", (bolsa['id'],))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Bolsa eliminada!")
                self.carregar_bolsas()
                self.bolsas_filtradas = self.bolsas.copy()
                self.atualizar_tabela()
                self.atualizar_footer()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao eliminar: {e}")

    def alternar_estado(self, bolsa, novo_estado):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("UPDATE bolsas SET estado=? WHERE id=?", (novo_estado, bolsa['id']))
            conn.commit()
            conn.close()

            estado_texto = "ativada" if novo_estado == "Ativa" else "encerrada"
            messagebox.showinfo("Sucesso", f"Bolsa {estado_texto}!")
            self.carregar_bolsas()
            self.bolsas_filtradas = self.bolsas.copy()
            self.atualizar_tabela()
            self.atualizar_footer()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao alterar estado: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("SIBES - Bolsas")
    root.state("zoomed")
    BolsasPage(root)
    root.mainloop()