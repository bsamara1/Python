import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os

class dashboard_estudante(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIBES")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.pagina_nome = "Painel Principal"

        self.ui()
    
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
        
    def carregar(self, caminho, tamanho):

        if os.path.exists(caminho):
            return ctk.CTkImage(
                Image.open(caminho),
                size=tamanho
            )

        return None


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

            ("Candidatura",icon("perfil.png"),self.mostrar_estudantes),

            ("Bolsas",icon("bolsa.png"),self.mostrar_bolsas),

            ("Candidaturas",icon("candidatura.png"),self.mostrar_candidaturas),

            ("Avaliação (Prolog)",icon("avaliacao.png"),self.mostrar_avaliacao),

            ("Relatórios",icon("relatorio.png"),self.mostrar_relatorios),

            ("Perfil",icon("utilizadores.png"),self.mostrar_utilizadores),

            ("Definições",icon("definicao.png"),self.mostrar_perfil)

        ]