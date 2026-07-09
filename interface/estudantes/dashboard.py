import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os





class App(ctk.CTkToplevel):

    def __init__(self, parent, id_utilizador_logado=None):
        super().__init__(parent)

        self.id_utilizador_logado = id_utilizador_logado
        self.title("SIBES - Portal do Estudante")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.pagina_nome = "Painel Principal"
        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.sidebar_ui()
        self.main_ui()

    def carregar(self, caminho, tamanho):
        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)
        return None

    def sidebar_ui(self):
        self.sidebar = ctk.CTkFrame(self.container, width=240, fg_color="#0B2A4A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = self.carregar("assets/logo.png", (40, 40))
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 35))

        ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
        ctk.CTkLabel(logo_frame, text="SIBES", font=("Segoe UI", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(logo_frame, text="Portal do Estudante", font=("Segoe UI", 11), text_color="#D6E4F0").grid(row=1, column=1, sticky="w")

        def icon(nome):
            return self.carregar(f"assets/{nome}", (20, 20))

        self.botoes = {}

        # Menu adaptado para o fluxo do Estudante
        menu = [
            ("Painel Principal", icon("casa.png"), self.mostrar_painel),
            ("Minhas Candidaturas", icon("perfil.png"), self.mostrar_estudantes),
            ("Bolsas Disponíveis", icon("bolsa.png"), self.mostrar_bolsas),
            ("Elegibilidade", icon("candidatura.png"), self.mostrar_candidaturas),
            ("Meu Perfil", icon("avaliacao.png"), self.mostrar_avaliacao),
        ]

        for texto, icone, comando in menu:
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
            btn.pack(fill="x", padx=15, pady=5)
            self.botoes[texto] = btn

        logout = self.carregar("assets/sair.png", (20, 20))
        
        self.btn_logout = ctk.CTkButton(
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
        )
        self.btn_logout.pack(side="bottom", fill="x", padx=15, pady=(0, 20))

        self.divisoria_logout = ctk.CTkFrame(self.sidebar, height=1, fg_color="#35506E")
        self.divisoria_logout.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            if self.master:
                self.master.deiconify()
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

    def reorganizar_layout_com_topo(self):
        self.area_conteudo.pack_forget()
        self.top_bar.pack(fill="x")
        self.divisoria_topo.pack(fill="x")
        self.area_conteudo.pack(fill="both", expand=True)

    def mostrar_painel(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Painel Principal")
        self.label_titulo.configure(text="Painel Principal")
        self.limpar_area_conteudo()
        self.carregar_painel()

   

    def main_ui(self):
        self.main = ctk.CTkFrame(self.container, fg_color="#F5F7FB")
        self.main.pack(side="left", fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main, fg_color="#F5F7FB", height=80)
        self.top_bar.pack(fill="x")
        self.top_bar.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(self.top_bar, text="Painel Principal", font=("Segoe UI", 24, "bold"), text_color="#142850")
        self.label_titulo.pack(side="left", padx=30, pady=20)

        user = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        user.pack(side="right", padx=30)

        avatar = self.carregar("assets/perfil.png", (40, 40))
        seta = self.carregar("assets/seta.png", (14, 14))

        ctk.CTkLabel(user, image=avatar, text="").pack(side="left")
        texto = ctk.CTkFrame(user, fg_color="transparent")
        texto.pack(side="left", padx=8)

        # Alterado de Administrador para Estudante
        ctk.CTkLabel(texto, text="Estudante SIBES", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(texto, text="estudante@sibes.cv", font=("Segoe UI", 11)).pack(anchor="w")
        ctk.CTkLabel(user, image=seta, text="").pack(side="left")

        self.divisoria_topo = ctk.CTkFrame(self.main, height=1, fg_color="#E5E7EB")
        self.divisoria_topo.pack(fill="x")

        self.area_conteudo = ctk.CTkFrame(self.main, fg_color="transparent")
        self.area_conteudo.pack(fill="both", expand=True)

        self.mostrar_painel()  

    def carregar_painel(self):
        frame = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        area = ctk.CTkFrame(frame, fg_color="transparent")
        area.pack(fill="x", padx=35, pady=20)

        # Mensagem de boas-vindas customizada para o aluno
        ctk.CTkLabel(area, text="Olá, Estudante! 👋", font=("Segoe UI", 28, "bold"), text_color="#162447").pack(anchor="w")
        ctk.CTkLabel(area, text="Acompanha o estado das tuas candidaturas e bolsas disponíveis.", text_color="#6B7280").pack(anchor="w")

        self.criar_cards(frame)

        baixo = ctk.CTkFrame(frame, fg_color="transparent")
        baixo.pack(fill="both", expand=True, padx=35, pady=(15, 30))
        baixo.grid_columnconfigure(0, weight=1)
        baixo.grid_columnconfigure(1, weight=1)

        # Box 1: Estado do próprio aluno
        box1 = ctk.CTkFrame(baixo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(box1, text="Estado da Candidatura Atual", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=20)
        ctk.CTkLabel(box1, justify="left", text="● Tipo: Bolsa de Mérito\n\n● Estado: Em Análise ⏳\n\n● Última Atualização: Hoje").pack(anchor="w", padx=30, pady=40)

        # Box 2: Notificações ou Histórico do aluno
        box2 = ctk.CTkFrame(baixo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box2.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(box2, text="Histórico de Atividades", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=20)

        dados = [
            ("Submissão de Candidatura", "Bolsa Mérito", "Concluído"),
            ("Upload de Documentos", "Certificado Notas", "Validado"),
            ("Inscrição no Sistema", "Portal SIBES", "Ativo")
        ]

        for acao, referencia, estado in dados:
            linha = ctk.CTkFrame(box2, fg_color="transparent")
            linha.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(linha, text=acao, width=180, anchor="w", font=("Segoe UI", 12, "bold")).pack(side="left")
            ctk.CTkLabel(linha, text=referencia, width=140, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=estado, text_color="#2E7D32" if estado in ["Concluído", "Validado", "Ativo"] else "black").pack(side="right")

    def criar_cards(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=35, pady=15)
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Cards com métricas individuais do Estudante
        self.criar_card(frame, 0, "Candidaturas", "Submetidas por ti", "1", "#EEF4FF", "#C7D6FF", "assets/chapeu.png")
        self.criar_card(frame, 1, "Bolsas", "Disponíveis para inscrição", "15", "#ECFFF0", "#BFEFCC", "assets/livro.png")
        self.criar_card(frame, 2, "Requisitos", "Documentos em falta", "0", "#FFF8EA", "#FFE2A8", "assets/formulario.png")
        self.criar_card(frame, 3, "Mensagens", "Da administração", "2", "#F6EEFF", "#D9C6FF", "assets/certo.png")

    def criar_card(self, parent, col, titulo, subtitulo, valor, cor, circulo, icone):
        card = ctk.CTkFrame(parent, fg_color=cor, corner_radius=15, height=120)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.grid_columnconfigure(1, weight=1)

        img = self.carregar(icone, (22, 22))
        esquerda = ctk.CTkFrame(card, fg_color="transparent")
        esquerda.grid(row=0, column=0, padx=20, pady=20)

        bola = ctk.CTkFrame(esquerda, width=45, height=45, corner_radius=25, fg_color=circulo)
        bola.pack()
        bola.pack_propagate(False)

        ctk.CTkLabel(bola, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")

        direita = ctk.CTkFrame(card, fg_color="transparent")
        direita.grid(row=0, column=1, sticky="e", padx=20)

        ctk.CTkLabel(direita, text=valor, font=("Segoe UI", 26, "bold")).pack(anchor="e")
        ctk.CTkLabel(direita, text=titulo, font=("Segoe UI", 12, "bold")).pack(anchor="e")
        ctk.CTkLabel(direita, text=subtitulo, font=("Segoe UI", 11)).pack(anchor="e")


if __name__ == "__main__":
    criar_base()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()