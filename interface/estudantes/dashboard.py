import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
from interface.admin.estudantes import EstudantesPage
from interface.admin.bolsas import BolsasPage
from interface.admin.candidaturas import Candidaturas
from interface.admin.avaliacao import AvaliacaoPage
from interface.admin.relatorios import RelatoriosPage

# Se o perfilUtilizador estiver na raiz do projeto:
from interface.admin.perfilUtilizador import PerfilUtilizador

# IMPORTAÇÃO DA BASE DE DADOS
from database.database import criar_base, conectar

class App(ctk.CTkToplevel):

    def __init__(self, parent, id_utilizador_logado=None):
        super().__init__(parent)

        self.id_utilizador_logado = id_utilizador_logado
        self.title("SIBES")
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

    def obter_estatisticas_reais(self):
        """Procura as contagens reais na base de dados para alimentar os cards dinamicamente"""
        stats = {"estudantes": 0, "bolsas": 0, "candidaturas": 0, "aprovados": 0}
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Conta o número real de estudantes
            cursor.execute("SELECT COUNT(*) FROM estudantes")
            stats["estudantes"] = cursor.fetchone()[0]
            
            # Conta o número real de bolsas
            cursor.execute("SELECT COUNT(*) FROM bolsas")
            stats["bolsas"] = cursor.fetchone()[0]
            
            # Conta o número real de candidaturas
            cursor.execute("SELECT COUNT(*) FROM candidaturas")
            stats["candidaturas"] = cursor.fetchone()[0]
            
            # Conta o número real de candidaturas aprovadas
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE estado = 'Aprovada'")
            stats["aprovados"] = cursor.fetchone()[0]
            
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar estatísticas reais para os cards: {e}")
        return stats

    def sidebar_ui(self):
        self.sidebar = ctk.CTkFrame(self.container, width=240, fg_color="#0B2A4A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = self.carregar("assets/logo1.png", (40, 40))
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 35))

        ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
        ctk.CTkLabel(logo_frame, text="SIBES", font=("Segoe UI", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(logo_frame, text="Sistema Inteligente de Bolsas Sustentáveis", font=("Segoe UI", 11), text_color="#D6E4F0").grid(row=1, column=1, sticky="w")

        def icon(nome):
            return self.carregar(f"assets/{nome}", (20, 20))

        self.botoes = {}

        menu = [
            ("Painel Principal", icon("casa.png"), self.mostrar_painel),
            ("Estudantes", icon("perfil.png"), self.mostrar_estudantes),
            ("Bolsas", icon("bolsa.png"), self.mostrar_bolsas),
            ("Candidaturas", icon("candidatura.png"), self.mostrar_candidaturas),
            ("Avaliação ", icon("avaliacao.png"), self.mostrar_avaliacao),
            ("Relatórios", icon("relatorio.png"), self.mostrar_relatorios),
            ("Definições", icon("definicao.png"), self.mostrar_perfil)
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
        
        # 1. Primeiro empacotamos o Botão (Fica na parte mais inferior)
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

        # 2. Depois empacotamos a Linha (Fica posicionada imediatamente acima do botão)
        self.divisoria_logout = ctk.CTkFrame(self.sidebar, height=1, fg_color="#35506E")
        self.divisoria_logout.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            if self.master:
                try:
                    # 1. Varre os widgets à procura APENAS do campo que mascara a senha (show="*")
                    def limpar_campo_senha(parent):
                        for widget in parent.winfo_children():
                            if isinstance(widget, ctk.CTkEntry):
                                # Verifica se é o campo de palavra-passe pelo atributo 'show'
                                if widget.cget("show") == "*":
                                    widget.delete(0, 'end')
                            # Continua a procurar em sub-frames, se existirem
                            if widget.winfo_children():
                                limpar_campo_senha(widget)

                    limpar_campo_senha(self.master)
                    
                except Exception as e:
                    print(f"Aviso ao limpar campo de senha: {e}")

                # 2. Atualiza a interface gráfica em background antes de exibir a janela
                self.master.update_idletasks()

                # 3. Faz o ecrã de login reaparecer maximizado e com foco
                self.master.deiconify()
                self.master.state("zoomed")
                self.master.focus_force()

            # 4. Encerra o painel de administração atual de forma limpa
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
        """Remove e reinsere os elements na ordem sequencial correta para evitar erros do Tkinter"""
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

    def mostrar_estudantes(self):
        self.destacar_botao_menu("Estudantes")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = EstudantesPage(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_bolsas(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Bolsas")
        self.top_bar.pack_forget()
        self.divisoria_topo.pack_forget()
        
        self.limpar_area_conteudo()
        pagina = BolsasPage(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=(30, 20))

    def mostrar_candidaturas(self):
        self.destacar_botao_menu("Candidaturas")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = Candidaturas(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_avaliacao(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Avaliação ")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = AvaliacaoPage(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_relatorios(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Relatórios")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = RelatoriosPage(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_perfil(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Definições")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = PerfilUtilizador(self.area_conteudo, self.id_utilizador_logado)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def main_ui(self):
        self.main = ctk.CTkFrame(self.container, fg_color="#F5F7FB")
        self.main.pack(side="left", fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main, fg_color="#F5F7FB", height=70, corner_radius=0)
        self.top_bar.pack(fill="x")
        self.top_bar.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(self.top_bar, text="Painel Principal", font=("Segoe UI", 22, "bold"), text_color="#142850")
        self.label_titulo.pack(side="left", padx=30, pady=20)

        # Container de Ações à Direita (Com Notificações e Avatar do Usuário)
        actions_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        actions_frame.pack(side="right", padx=30)

        # Ícone de Notificações
        bell_icon = self.carregar("assets/notificacao.png", (22, 22))
        self.btn_notif = ctk.CTkButton(
            actions_frame, image=bell_icon, text="", width=40, height=40,
            fg_color="transparent", hover_color="#F0F2F5", command=lambda: print("Notificações clicadas")
        )
        self.btn_notif.pack(side="left", padx=(0, 10))

        # Linha Divisória Vertical entre Notificação e Perfil
        ctk.CTkFrame(actions_frame, width=1, height=30, fg_color="#E5E7EB").pack(side="left", padx=10)

        # Perfil do Utilizador
        user = ctk.CTkFrame(actions_frame, fg_color="transparent")
        user.pack(side="left", padx=10)

        avatar = self.carregar("assets/perfil.png", (38, 38))
        seta = self.carregar("assets/seta.png", (12, 12))

        ctk.CTkLabel(user, image=avatar, text="").pack(side="left")
        texto = ctk.CTkFrame(user, fg_color="transparent")
        texto.pack(side="left", padx=12)

        ctk.CTkLabel(texto, text="Administrador", font=("Segoe UI", 13, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(texto, text="admin@sibes.cv", font=("Segoe UI", 11), text_color="#6B7280").pack(anchor="w")
        
        if seta:
            ctk.CTkLabel(user, image=seta, text="").pack(side="left", padx=(5, 0))

        # Linha Divisória Horizontal no fundo do Topo (Border bottom)
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

        ctk.CTkLabel(area, text="Bem-vindo, Administrador! 👋", font=("Segoe UI", 28, "bold"), text_color="#162447").pack(anchor="w")
        ctk.CTkLabel(area, text="Aqui está um resumo geral do sistema.", text_color="#6B7280").pack(anchor="w")

        self.criar_cards(frame)

        baixo = ctk.CTkFrame(frame, fg_color="transparent")
        baixo.pack(fill="both", expand=True, padx=35, pady=(15, 30))
        baixo.grid_columnconfigure(0, weight=1)
        baixo.grid_columnconfigure(1, weight=1)

        box1 = ctk.CTkFrame(baixo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(box1, text="Candidaturas por Estado", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=20)
        ctk.CTkLabel(box1, justify="left", text="● Aprovadas: 40\n\n● Pendentes: 25\n\n● Rejeitadas: 20").pack(anchor="w", padx=30, pady=40)

        box2 = ctk.CTkFrame(baixo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box2.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(box2, text="Candidaturas Recentes", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=20)

        dados = [
            ("João Silva", "Bolsa Mérito", "Pendente"),
            ("Ana Santos", "Bolsa Social", "Aprovada"),
            ("Carlos Lima", "Bolsa Desporto", "Pendente"),
            ("Maria Costa", "Bolsa Excelência", "Rejeitada")
        ]

        for nome, bolsa, estado in dados:
            linha = ctk.CTkFrame(box2, fg_color="transparent")
            linha.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(linha, text=nome, width=160, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=bolsa, width=160, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=estado).pack(side="right")

    def criar_cards(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=35, pady=15)
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Procura as contagens atualizadas na base de dados SQLite
        estatisticas = self.obter_estatisticas_reais()

        self.criar_card(frame, 0, "Estudantes", "Estudantes registados", str(estatisticas["estudantes"]), "#EEF4FF", "#C7D6FF", "assets/chapeu.png")
        self.criar_card(frame, 1, "Bolsas", "Bolsas disponíveis", str(estatisticas["bolsas"]), "#ECFFF0", "#BFEFCC", "assets/livro.png")
        self.criar_card(frame, 2, "Candidaturas", "Candidaturas", str(estatisticas["candidaturas"]), "#FFF8EA", "#FFE2A8", "assets/formulario.png")
        self.criar_card(frame, 3, "Aprovados", "Este mês", str(estatisticas["aprovados"]), "#F6EEFF", "#D9C6FF", "assets/certo.png")

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

        ctk.CTkLabel(direita, text=valor, font=("Segoe UI", 26, "bold"), text_color="#142850").pack(anchor="e")
        ctk.CTkLabel(direita, text=titulo, font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="e")
        ctk.CTkLabel(direita, text=subtitulo, font=("Segoe UI", 11), text_color="#6B7280").pack(anchor="e")


if __name__ == "__main__":
    criar_base()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()