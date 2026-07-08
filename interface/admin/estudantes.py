# estudantes.py
import customtkinter as ctk
from PIL import Image
import os
import sys
import sqlite3
from tkinter import messagebox


class EstudantesPage(ctk.CTkFrame):
    """Página de Gestão de Estudantes com ícones na sidebar"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.pack(fill="both", expand=True)

        # Configurações
        self.caminho_db = self.obter_caminho_db()
        self.estudantes = []
        self.estudantes_filtrados = []
        self.modo_edicao = False

        # Carregar dados
        self.carregar_estudantes()
        
        # Carregar imagens e criar interface
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
        # Ícones do menu
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
        self.icon_add = self.carregar("assets/adicionar.png", (16, 16))
        self.icon_edit = self.carregar("assets/editar.png", (16, 16))
        self.icon_delete = self.carregar("assets/eliminar.png", (16, 16))

    def carregar_estudantes(self):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, universidade, curso, media, rendimento
                FROM estudantes ORDER BY nome
            """)
            resultados = cursor.fetchall()
            conn.close()

            self.estudantes = [
                {
                    'id': row[0], 'nome': row[1], 'email': row[2],
                    'universidade': row[3], 'curso': row[4],
                    'media': row[5], 'rendimento': row[6]
                } for row in resultados
            ]
            self.estudantes_filtrados = self.estudantes.copy()
        except sqlite3.Error as e:
            print(f"⚠️ Erro ao carregar estudantes: {e}")
            self.estudantes = []
            self.estudantes_filtrados = []

    # ==========================================
    # INTERFACE PRINCIPAL
    # ==========================================
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

        # Logo
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

        # Menu com ícones
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
                fg_color="#11457B" if item == "Estudantes" else "transparent",
                hover_color="#11457B",
                anchor="w",
                height=45,
                font=("Segoe UI", 13),
                command=lambda i=item: self.menu_click(i)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.botoes_menu[item] = btn

        # Separador e Logout
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

    # ==========================================
    # CONTEÚDO PRINCIPAL
    # ==========================================
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
            text="🎓 Estudantes",
            font=("Segoe UI", 28, "bold"),
            text_color="#0B2A4A"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=f"Gerir todos os estudantes registados. ({len(self.estudantes)} estudantes)",
            text_color="#6B7280",
            font=("Segoe UI", 13)
        ).pack(anchor="w")

        # Botão Adicionar
        add_btn = ctk.CTkButton(
            topbar,
            text="➕ Adicionar Estudante",
            command=self.abrir_form_estudante,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            width=200,
            height=42,
            corner_radius=8,
            font=("Segoe UI", 13, "bold")
        )
        add_btn.pack(side="right")

        # Separador
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

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="🔍 Pesquisar por nome, email ou curso...",
            height=45,
            corner_radius=8
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.aplicar_filtros)

        self.filtro_universidade = ctk.CTkComboBox(
            filter_frame,
            values=self.obter_universidades(),
            width=180,
            height=45,
            command=self.aplicar_filtros
        )
        self.filtro_universidade.pack(side="left", padx=(15, 0))
        self.filtro_universidade.set("Todas")

        ctk.CTkButton(
            filter_frame,
            text="🔄 Limpar",
            width=100,
            height=45,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.limpar_filtros
        ).pack(side="left", padx=(10, 0))

    def obter_universidades(self):
        universidades = set()
        for est in self.estudantes:
            if est.get('universidade'):
                universidades.add(est['universidade'])
        return ["Todas"] + sorted(list(universidades))

    def aplicar_filtros(self, event=None):
        pesquisa = self.search_entry.get().lower().strip()
        universidade = self.filtro_universidade.get()

        self.estudantes_filtrados = []
        for est in self.estudantes:
            if pesquisa:
                if (pesquisa not in est['nome'].lower() and 
                    pesquisa not in est['email'].lower() and 
                    pesquisa not in est['curso'].lower()):
                    continue
            if universidade != "Todas" and est.get('universidade') != universidade:
                continue
            self.estudantes_filtrados.append(est)

        self.atualizar_tabela()
        self.atualizar_footer()

    def limpar_filtros(self):
        self.search_entry.delete(0, "end")
        self.filtro_universidade.set("Todas")
        self.estudantes_filtrados = self.estudantes.copy()
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

        # Cabeçalho
        headers = ["ID", "Nome", "Email", "Universidade", "Curso", "Média", "Rendimento", "Ações"]
        widths = [50, 150, 220, 140, 180, 70, 120, 120]

        header = ctk.CTkFrame(self.table_card, fg_color="#F8FAFC", height=55)
        header.pack(fill="x")

        for texto, largura in zip(headers, widths):
            ctk.CTkLabel(
                header, text=texto, width=largura,
                font=("Segoe UI", 12, "bold"), text_color="#334155"
            ).pack(side="left", padx=5, pady=15)

        ctk.CTkFrame(self.table_card, height=1, fg_color="#E5E7EB").pack(fill="x")

        # Corpo
        self.corpo_tabela = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.corpo_tabela.pack(fill="both", expand=True)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.corpo_tabela.winfo_children():
            widget.destroy()

        if not self.estudantes_filtrados:
            ctk.CTkLabel(
                self.corpo_tabela,
                text="📭 Nenhum estudante encontrado",
                font=("Segoe UI", 16),
                text_color="#6B7280"
            ).pack(pady=50)
            return

        for idx, est in enumerate(self.estudantes_filtrados):
            row = ctk.CTkFrame(
                self.corpo_tabela,
                fg_color="#F9FAFB" if idx % 2 == 0 else "white",
                height=65
            )
            row.pack(fill="x")

            # ID
            ctk.CTkLabel(row, text=str(est['id']), width=50, anchor="w").pack(side="left", padx=5)
            # Nome
            ctk.CTkLabel(row, text=est['nome'], width=150, anchor="w", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
            # Email
            ctk.CTkLabel(row, text=est['email'], width=220, anchor="w").pack(side="left", padx=5)
            # Universidade
            ctk.CTkLabel(row, text=est.get('universidade', '-'), width=140, anchor="w").pack(side="left", padx=5)
            # Curso
            ctk.CTkLabel(row, text=est.get('curso', '-'), width=180, anchor="w").pack(side="left", padx=5)
            # Média
            media = est.get('media', 0) or 0
            cor_media = "#16A34A" if media >= 14 else "#D97706" if media >= 10 else "#DC2626"
            ctk.CTkLabel(row, text=f"{media:.1f}" if media else "-", width=70, anchor="w", text_color=cor_media).pack(side="left", padx=5)
            # Rendimento
            rend = est.get('rendimento', 0) or 0
            ctk.CTkLabel(row, text=f"{rend:,.0f} Kz" if rend else "-", width=120, anchor="w").pack(side="left", padx=5)

            # Ações
            acoes = ctk.CTkFrame(row, fg_color="transparent")
            acoes.pack(side="left", padx=5)

            ctk.CTkButton(
                acoes, text="✏️", width=35, height=35,
                fg_color="#EFF6FF", hover_color="#DBEAFE", text_color="#2563EB",
                command=lambda e=est: self.editar_estudante(e)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes, text="🗑️", width=35, height=35,
                fg_color="#FEF2F2", hover_color="#FEE2E2", text_color="#EF4444",
                command=lambda e=est: self.eliminar_estudante(e)
            ).pack(side="left", padx=2)

            ctk.CTkFrame(self.corpo_tabela, height=1, fg_color="#E5E7EB").pack(fill="x")

    def criar_footer(self):
        self.footer = ctk.CTkFrame(self.main, fg_color="transparent")
        self.footer.pack(fill="x", pady=15)
        self.atualizar_footer()

    def atualizar_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

        total = len(self.estudantes_filtrados)
        total_geral = len(self.estudantes)

        info_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        info_frame.pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f"📊 Mostrando {total} de {total_geral} estudantes",
            text_color="#334155",
            font=("Segoe UI", 12)
        ).pack(side="left")

        if self.estudantes_filtrados:
            medias = [e.get('media', 0) for e in self.estudantes_filtrados if e.get('media')]
            if medias:
                media_geral = sum(medias) / len(medias)
                ctk.CTkLabel(
                    info_frame,
                    text=f" | Média geral: {media_geral:.1f}",
                    text_color="#334155",
                    font=("Segoe UI", 12)
                ).pack(side="left", padx=(10, 0))

    # ==========================================
    # CRUD OPERATIONS
    # ==========================================
    def abrir_form_estudante(self, estudante=None):
        modal = ctk.CTkToplevel(self)
        modal.title("Adicionar Estudante" if not estudante else f"Editar: {estudante['nome']}")
        modal.geometry("600x700")
        modal.configure(fg_color="#F4F6FB")
        modal.grab_set()

        frame = ctk.CTkFrame(modal, fg_color="white", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(
            frame,
            text="➕ Novo Estudante" if not estudante else f"✏️ {estudante['nome']}",
            font=("Segoe UI", 24, "bold"),
            text_color="#0B2A4A"
        ).pack(pady=(20, 30))

        campos = [
            ("👤 Nome Completo", "nome", estudante['nome'] if estudante else ""),
            ("📧 Email", "email", estudante['email'] if estudante else ""),
            ("🏛️ Universidade", "universidade", estudante.get('universidade', '') if estudante else ""),
            ("📚 Curso", "curso", estudante.get('curso', '') if estudante else ""),
            ("📊 Média", "media", str(estudante.get('media', '')) if estudante else ""),
            ("💰 Rendimento", "rendimento", str(estudante.get('rendimento', '')) if estudante else "")
        ]

        entries = {}
        for label, key, valor in campos:
            ctk.CTkLabel(
                frame, text=label,
                font=("Segoe UI", 13, "bold"),
                text_color="#0B2A4A"
            ).pack(anchor="w", padx=40, pady=(10, 2))

            entry = ctk.CTkEntry(frame, height=40, font=("Segoe UI", 13))
            entry.insert(0, valor)
            entry.pack(fill="x", padx=40, pady=(0, 5))
            entries[key] = entry

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=(30, 20))

        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            width=150, height=45,
            fg_color="#2563EB", hover_color="#1D4ED8",
            command=lambda: self.guardar_estudante(modal, entries, estudante)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            width=150, height=45,
            fg_color="#6B7280", hover_color="#4B5563",
            command=modal.destroy
        ).pack(side="left", padx=10)

    def guardar_estudante(self, modal, entries, estudante=None):
        try:
            nome = entries['nome'].get().strip()
            email = entries['email'].get().strip()
            universidade = entries['universidade'].get().strip()
            curso = entries['curso'].get().strip()
            media = entries['media'].get().strip()
            rendimento = entries['rendimento'].get().strip()

            if not nome or not email:
                messagebox.showerror("Erro", "Nome e Email são obrigatórios!")
                return

            if "@" not in email:
                messagebox.showerror("Erro", "Email inválido!")
                return

            media_val = float(media) if media else 0
            rendimento_val = float(rendimento.replace(',', '.')) if rendimento else 0

            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()

            if estudante:
                cursor.execute("""
                    UPDATE estudantes
                    SET nome=?, email=?, universidade=?, curso=?, media=?, rendimento=?
                    WHERE id=?
                """, (nome, email, universidade, curso, media_val, rendimento_val, estudante['id']))
                messagebox.showinfo("Sucesso", "Estudante atualizado!")
            else:
                cursor.execute("""
                    INSERT INTO estudantes (nome, email, universidade, curso, media, rendimento)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nome, email, universidade, curso, media_val, rendimento_val))
                messagebox.showinfo("Sucesso", "Estudante adicionado!")

            conn.commit()
            conn.close()

            modal.destroy()
            self.carregar_estudantes()
            self.estudantes_filtrados = self.estudantes.copy()
            self.atualizar_tabela()
            self.atualizar_footer()
            self.filtro_universidade.configure(values=self.obter_universidades())

        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {e}")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao guardar: {e}")

    def editar_estudante(self, estudante):
        self.abrir_form_estudante(estudante)

    def eliminar_estudante(self, estudante):
        if messagebox.askyesno("Confirmar", f"Eliminar {estudante['nome']}?"):
            try:
                conn = sqlite3.connect(self.caminho_db)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM estudantes WHERE id=?", (estudante['id'],))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Estudante eliminado!")
                self.carregar_estudantes()
                self.estudantes_filtrados = self.estudantes.copy()
                self.atualizar_tabela()
                self.atualizar_footer()
                self.filtro_universidade.configure(values=self.obter_universidades())
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao eliminar: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("SIBES - Estudantes")
    root.state("zoomed")
    EstudantesPage(root)
    root.mainloop()