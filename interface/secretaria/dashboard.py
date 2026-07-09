import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SIBES")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.pagina_nome = "Painel Principal"

        self.ui()

    # ==========================================
    # INTERFACE PRINCIPAL
    # ==========================================

    def ui(self):

        self.container = ctk.CTkFrame(
            self,
            fg_color="#F4F6FB"
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.sidebar_ui()
        self.main_ui()

    # ==========================================
    # CARREGAR IMAGENS
    # ==========================================

    def carregar(self, caminho, tamanho):

        if os.path.exists(caminho):
            return ctk.CTkImage(
                Image.open(caminho),
                size=tamanho
            )

        return None

    # ==========================================
    # SIDEBAR
    # ==========================================

    def sidebar_ui(self):

        self.sidebar = ctk.CTkFrame(
            self.container,
            width=240,
            fg_color="#0B2A4A"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        logo = self.carregar(
            "assets/logo.png",
            (40,40)
        )

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25,35)
        )

        ctk.CTkLabel(
            logo_frame,
            image=logo,
            text=""
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=10
        )

        ctk.CTkLabel(
            logo_frame,
            text="SIBES",
            font=("Segoe UI",20,"bold"),
            text_color="white"
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        ctk.CTkLabel(
            logo_frame,
            text="Sistema Inteligente de Bolsas Sustentáveis",
            font=("Segoe UI",11),
            text_color="#D6E4F0"
        ).grid(
            row=1,
            column=1,
            sticky="w"
        )

        def icon(nome):
            return self.carregar(
                f"assets/{nome}",
                (20,20)
            )

        self.botoes = {}

        menu = [

            ("Painel Principal",icon("casa.png"),self.mostrar_painel),

            ("Estudantes",icon("perfil.png"),self.mostrar_estudantes),

            ("Bolsas",icon("bolsa.png"),self.mostrar_bolsas),

            ("Candidaturas",icon("candidatura.png"),self.mostrar_candidaturas),

            ("Avaliação (Prolog)",icon("avaliacao.png"),self.mostrar_avaliacao),

            ("Relatórios",icon("relatorio.png"),self.mostrar_relatorios),

            ("Utilizadores",icon("utilizadores.png"),self.mostrar_utilizadores),

            ("Definições",icon("definicao.png"),self.mostrar_perfil)

        ]

        for texto,icone,comando in menu:

            btn = ctk.CTkButton(

                self.sidebar,

                text=texto,

                image=icone,

                compound="left",

                anchor="w",

                fg_color="transparent",

                hover_color="#11457B",

                text_color="white",

                height=45,

                command=comando

            )

            btn.pack(
                fill="x",
                padx=15,
                pady=5
            )

            self.botoes[texto]=btn

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#35506E"
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=(0,10)
        )

        logout = self.carregar(
            "assets/sair.png",
            (20,20)
        )

        ctk.CTkButton(

            self.sidebar,

            text="Terminar Sessão",

            image=logout,

            compound="left",

            anchor="w",

            fg_color="transparent",

            hover_color="#2A3F5F",

            text_color="#FF6B6B",

            height=45,

            command=self.terminar_sessao

        ).pack(

            side="bottom",

            fill="x",

            padx=15,

            pady=20

        )
    # ==========================================
    # MÉTODOS AUXILIARES
    # ==========================================

    def terminar_sessao(self):
        if messagebox.askyesno(
            "Terminar Sessão",
            "Deseja realmente terminar a sessão?"
        ):
            self.destroy()

    def limpar_area_conteudo(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    def destacar_botao_menu(self, nome):
        for texto, botao in self.botoes.items():
            if texto == nome:
                botao.configure(fg_color="#11457B")
            else:
                botao.configure(fg_color="transparent")

    # ==========================================
    # PÁGINAS
    # ==========================================

    def mostrar_painel(self):
        self.destacar_botao_menu("Painel Principal")
        self.label_titulo.configure(text="Painel Principal")

        self.limpar_area_conteudo()
        self.carregar_painel()

    def mostrar_estudantes(self):
        self.destacar_botao_menu("Estudantes")
        self.label_titulo.configure(text="Estudantes")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Estudantes",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_bolsas(self):
        self.destacar_botao_menu("Bolsas")
        self.label_titulo.configure(text="Bolsas")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Bolsas",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_candidaturas(self):
        self.destacar_botao_menu("Candidaturas")
        self.label_titulo.configure(text="Candidaturas")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Candidaturas",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_avaliacao(self):
        self.destacar_botao_menu("Avaliação (Prolog)")
        self.label_titulo.configure(text="Avaliação (Prolog)")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Avaliação",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_relatorios(self):
        self.destacar_botao_menu("Relatórios")
        self.label_titulo.configure(text="Relatórios")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Relatórios",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_utilizadores(self):
        self.destacar_botao_menu("Utilizadores")
        self.label_titulo.configure(text="Utilizadores")

        self.limpar_area_conteudo()

        ctk.CTkLabel(
            self.area_conteudo,
            text="Página Utilizadores",
            font=("Segoe UI",30,"bold")
        ).pack(pady=50)

    def mostrar_perfil(self):

        self.destacar_botao_menu("Definições")

        self.label_titulo.configure(text="")

        self.limpar_area_conteudo()

        from interface.admin.perfilUtilizador import PerfilUtilizador

        PerfilUtilizador(self.area_conteudo)

    # ==========================================
    # MAIN
    # ==========================================

    def main_ui(self):

        self.main = ctk.CTkFrame(
            self.container,
            fg_color="#F5F7FB"
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        top = ctk.CTkFrame(
            self.main,
            fg_color="#F5F7FB",
            height=80
        )

        top.pack(fill="x")
        top.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(
            top,
            text="Painel Principal",
            font=("Segoe UI",24,"bold"),
            text_color="#142850"
        )

        self.label_titulo.pack(
            side="left",
            padx=30,
            pady=20
        )

        user = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        user.pack(
            side="right",
            padx=30
        )

        avatar = self.carregar(
            "assets/perfil.png",
            (40,40)
        )

        seta = self.carregar(
            "assets/seta.png",
            (14,14)
        )

        ctk.CTkLabel(
            user,
            image=avatar,
            text=""
        ).pack(side="left")

        texto = ctk.CTkFrame(
            user,
            fg_color="transparent"
        )

        texto.pack(side="left", padx=8)

        ctk.CTkLabel(
            texto,
            text="Administrador",
            font=("Segoe UI",14,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            texto,
            text="admin@sibes.cv",
            font=("Segoe UI",11)
        ).pack(anchor="w")

        ctk.CTkLabel(
            user,
            image=seta,
            text=""
        ).pack(side="left")

        ctk.CTkFrame(
            self.main,
            height=1,
            fg_color="#E5E7EB"
        ).pack(fill="x")

        self.area_conteudo = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        self.area_conteudo.pack(
            fill="both",
            expand=True
        )

        self.mostrar_painel()  
    # ==========================================
    # PAINEL PRINCIPAL
    # ==========================================

    def carregar_painel(self):

        frame = ctk.CTkFrame(
            self.area_conteudo,
            fg_color="transparent"
        )

        frame.pack(fill="both", expand=True)

        area = ctk.CTkFrame(frame, fg_color="transparent")
        area.pack(fill="x", padx=35, pady=20)

        ctk.CTkLabel(
            area,
            text="Bem-vindo, Administrador! 👋",
            font=("Segoe UI", 28, "bold"),
            text_color="#162447"
        ).pack(anchor="w")

        ctk.CTkLabel(
            area,
            text="Aqui está um resumo geral do sistema.",
            text_color="#6B7280"
        ).pack(anchor="w")

        self.criar_cards(frame)

        baixo = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        baixo.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(15,30)
        )

        baixo.grid_columnconfigure(0, weight=1)
        baixo.grid_columnconfigure(1, weight=1)

        # =============================
        # BOX ESQUERDA
        # =============================

        box1 = ctk.CTkFrame(
            baixo,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        box1.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,10)
        )

        ctk.CTkLabel(
            box1,
            text="Candidaturas por Estado",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=20, pady=20)

        ctk.CTkLabel(
            box1,
            justify="left",
            text="● Aprovadas: 40\n\n● Pendentes: 25\n\n● Rejeitadas: 20"
        ).pack(anchor="w", padx=30, pady=40)

        # =============================
        # BOX DIREITA
        # =============================

        box2 = ctk.CTkFrame(
            baixo,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        box2.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        ctk.CTkLabel(
            box2,
            text="Candidaturas Recentes",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=20, pady=20)

        dados = [
            ("João Silva","Bolsa Mérito","Pendente"),
            ("Ana Santos","Bolsa Social","Aprovada"),
            ("Carlos Lima","Bolsa Desporto","Pendente"),
            ("Maria Costa","Bolsa Excelência","Rejeitada")
        ]

        for nome, bolsa, estado in dados:

            linha = ctk.CTkFrame(
                box2,
                fg_color="transparent"
            )

            linha.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                linha,
                text=nome,
                width=160,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                linha,
                text=bolsa,
                width=160,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                linha,
                text=estado
            ).pack(side="right")
    # ==========================================
    # CARDS
    # ==========================================

    def criar_cards(self, parent):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.pack(fill="x", padx=35, pady=15)

        frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.criar_card(
            frame,
            0,
            "Estudantes",
            "Estudantes registados",
            "120",
            "#EEF4FF",
            "#C7D6FF",
            "assets/chapeu.png"
        )

        self.criar_card(
            frame,
            1,
            "Bolsas",
            "Bolsas disponíveis",
            "15",
            "#ECFFF0",
            "#BFEFCC",
            "assets/livro.png"
        )

        self.criar_card(
            frame,
            2,
            "Candidaturas",
            "Candidaturas",
            "85",
            "#FFF8EA",
            "#FFE2A8",
            "assets/formulario.png"
        )

        self.criar_card(
            frame,
            3,
            "Aprovados",
            "Este mês",
            "40",
            "#F6EEFF",
            "#D9C6FF",
            "assets/certo.png"
        )

    def criar_card(
        self,
        parent,
        col,
        titulo,
        subtitulo,
        valor,
        cor,
        circulo,
        icone
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=cor,
            corner_radius=15,
            height=120
        )

        card.grid(
            row=0,
            column=col,
            padx=10,
            sticky="nsew"
        )

        card.grid_columnconfigure(1, weight=1)

        img = self.carregar(icone,(22,22))

        esquerda = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        esquerda.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        bola = ctk.CTkFrame(
            esquerda,
            width=45,
            height=45,
            corner_radius=25,
            fg_color=circulo
        )

        bola.pack()
        bola.pack_propagate(False)

        ctk.CTkLabel(
            bola,
            image=img,
            text=""
        ).place(relx=0.5,rely=0.5,anchor="center")

        direita = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        direita.grid(
            row=0,
            column=1,
            sticky="e",
            padx=20
        )

        ctk.CTkLabel(
            direita,
            text=valor,
            font=("Segoe UI",26,"bold")
        ).pack(anchor="e")

        ctk.CTkLabel(
            direita,
            text=titulo,
            font=("Segoe UI",12,"bold")
        ).pack(anchor="e")

        ctk.CTkLabel(
            direita,
            text=subtitulo,
            font=("Segoe UI",11)
        ).pack(anchor="e")
    # ==========================================
    # PÁGINAS (TEMPORÁRIAS)
    # ==========================================

    def carregar_estudantes(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Estudantes",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    def carregar_bolsas(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Bolsas",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    def carregar_candidaturas(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Candidaturas",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    def carregar_avaliacao(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Avaliação (Prolog)",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    def carregar_relatorios(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Relatórios",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    def carregar_utilizadores(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="Página Utilizadores",
            font=("Segoe UI", 30, "bold")
        ).pack(expand=True)

    # ==========================================
    # PERFIL
    # ==========================================

    def carregar_perfil(self):

        from interface.admin.perfilUtilizador import PerfilUtilizador

        PerfilUtilizador(self.area_conteudo)                    
# ==========================================
# EXECUTAR
# ==========================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
# interface/secretaria/dashboard_secretaria.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os

# Importar as páginas existentes


class AppSecretaria(ctk.CTk):
    def __init__(self, id_utilizador, nome_utilizador):
        super().__init__()
        self.id_utilizador = id_utilizador
        self.nome_utilizador = nome_utilizador

        self.title("SIBES - Painel da Secretaria")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")
        
        self.pagina_nome = "Painel Secretaria"
        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.container, width=260, fg_color="#081A3C", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Saudação e Nome da Secretaria
        ctk.CTkLabel(self.sidebar, text="SIBES", font=("Segoe UI", 28, "bold"), text_color="white").pack(pady=(30, 5))
        ctk.CTkLabel(self.sidebar, text=f"Secretaria: {self.nome_utilizador}", font=("Segoe UI", 14), text_color="#9CA3AF").pack(pady=(0, 30))

        # Botões de Navegação
        self.btn_estudantes = ctk.CTkButton(self.sidebar, text="Gestão de Estudantes", fg_color="transparent", anchor="w", command=self.abrir_estudantes)
        self.btn_estudantes.pack(fill="x", padx=15, pady=5)

        self.btn_bolsas = ctk.CTkButton(self.sidebar, text="Gestão de Bolsas", fg_color="transparent", anchor="w", command=self.abrir_bolsas)
        self.btn_bolsas.pack(fill="x", padx=15, pady=5)

        self.btn_candidaturas = ctk.CTkButton(self.sidebar, text="Candidaturas", fg_color="transparent", anchor="w", command=self.abrir_candidaturas)
        self.btn_candidaturas.pack(fill="x", padx=15, pady=5)

        # Botão Terminar Sessão
        ctk.CTkButton(self.sidebar, text="Terminar Sessão", fg_color="#EF4444", hover_color="#DC2626", command=self.logout).pack(side="bottom", fill="x", padx=15, pady=20)

        # Área de Conteúdo
        self.area_conteudo = ctk.CTkFrame(self.container, fg_color="transparent")
        self.area_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Abrir página inicial por defeito
        self.abrir_estudantes()

    def limpar_conteudo(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    def abrir_estudantes(self):
        self.limpar_conteudo()
        EstudantesPage(self.area_conteudo)

    def abrir_bolsas(self):
        self.limpar_conteudo()
        BolsasPage(self.area_conteudo)

    def abrir_candidaturas(self):
        self.limpar_conteudo()
        CandidaturasPage(self.area_conteudo)

    def logout(self):
        if messagebox.askyesno("Sair", "Deseja terminar a sessão?"):
            self.destroy()
            # Código para voltar ao login se necessário