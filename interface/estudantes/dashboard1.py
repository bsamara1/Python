import sys
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
if diretorio_atual not in sys.path:
    sys.path.append(diretorio_atual)

raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, "..", ".."))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os

# Importações dos módulos locais de estudante
from bolsas import BolsasPage
from minhas_candidaturas import Candidaturas
from perfil import PerfilUtilizador

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    from database.database import conectar
except ImportError:
    def conectar():
        import sqlite3
        return sqlite3.connect(os.path.join(diretorio_atual, 'database', 'sibes.db'))

class DashboardEstudante(ctk.CTkToplevel):

    def __init__(self, parent, id_utilizador_logado=None):
        super().__init__(parent)

        # ID do estudante logado para filtros
        self.id_utilizador_logado = id_utilizador_logado if id_utilizador_logado else 1
        self.title("SIBES - Painel do Estudante")
        self.state("zoomed")
        self.configure(fg_color="#F4F6FB")

        self.nome_usuario = "Estudante"
        self.obter_dados_estudante()

        self.pagina_nome = "Painel Principal"
        self.ui()

    def ui(self):
        self.container = ctk.CTkFrame(self, fg_color="#F4F6FB")
        self.container.pack(fill="both", expand=True)

        self.sidebar_ui()
        self.main_ui()

    def terminar_sessao(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja realmente terminar a sessão?"):
            if self.master:
                try:
                    # Limpa o campo de palavra-passe do ecrã de login antes de o mostrar de novo
                    def limpar_campo_senha(parent):
                        for widget in parent.winfo_children():
                            if isinstance(widget, ctk.CTkEntry):
                                if widget.cget("show") == "*":
                                    widget.delete(0, 'end')
                            if widget.winfo_children():
                                limpar_campo_senha(widget)

                    limpar_campo_senha(self.master)
                except Exception as e:
                    print(f"Aviso ao limpar campo de senha: {e}")

                self.master.update_idletasks()

                # Faz o ecrã de login reaparecer maximizado e com foco
                self.master.deiconify()
                self.master.state("zoomed")
                self.master.focus_force()

            # Encerra o painel do estudante de forma limpa
            self.destroy()

    def carregar(self, caminho, tamanho):
        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)
        return None

    def obter_dados_estudante(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM utilizadores WHERE id = ?", (self.id_utilizador_logado,))
            res = cursor.fetchone()
            if res and res[0]:
                self.nome_usuario = res[0]
            conn.close()
        except Exception:
            self.nome_usuario = "Estudante SIBES"

    def obter_estatisticas_reais(self):
        dados = {"total": 0, "pendentes": 0, "aprovadas": 0, "valor_total": 0}
        try:
            conn = conectar()
            cursor = conn.cursor()

            # A tabela candidaturas não tem uma coluna 'id_utilizador' nem 'valor';
            # a ligação correta é: utilizadores.email == estudantes.email -> estudantes.id == candidaturas.estudante_id
            # e o valor da bolsa vem de bolsas.valor via candidaturas.bolsa_id.
            cursor.execute("SELECT email FROM utilizadores WHERE id = ?", (self.id_utilizador_logado,))
            res = cursor.fetchone()
            email = res[0] if res else None

            if email:
                cursor.execute("SELECT id FROM estudantes WHERE email = ?", (email,))
                res_estudante = cursor.fetchone()
                estudante_id = res_estudante[0] if res_estudante else None

                if estudante_id:
                    cursor.execute("""
                        SELECT c.estado, COUNT(*), SUM(b.valor)
                        FROM candidaturas c
                        LEFT JOIN bolsas b ON b.id = c.bolsa_id
                        WHERE c.estudante_id = ?
                        GROUP BY c.estado
                    """, (estudante_id,))

                    linhas = cursor.fetchall()
                    for linha in linhas:
                        estado = linha[0]
                        qtd = linha[1]
                        valor_parcial = linha[2] if linha[2] else 0

                        dados["total"] += qtd
                        if estado == "Pendente":
                            dados["pendentes"] = qtd
                        elif estado == "Aprovada":
                            dados["aprovadas"] = qtd
                            dados["valor_total"] += valor_parcial

            conn.close()
        except Exception as e:
            print(f"Erro ao obter estatísticas do estudante: {e}")
        return dados

    def sidebar_ui(self):
        # Sidebar com a cor escura #0B2A4A herdada do segundo código
        self.sidebar = ctk.CTkFrame(self.container, width=250, fg_color="#0B2A4A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = self.carregar("assets/logo1.png", (40, 40))
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 35))

        # Títulos adaptados para o Candidato/Estudante
        if logo:
            ctk.CTkLabel(logo_frame, image=logo, text="").grid(row=0, column=0, rowspan=2, padx=10)
        ctk.CTkLabel(logo_frame, text="SIBES", font=("Segoe UI", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(logo_frame, text="Painel do Candidato", font=("Segoe UI", 11), text_color="#D6E4F0").grid(row=1, column=1, sticky="w")

        def icon(nome):
            return self.carregar(f"assets/{nome}", (20, 20))

        self.botoes = {}

        # Menu Contextualizado para o Estudante
        menu = [
            ("Painel Principal", icon("casa.png"), self.mostrar_painel),
            ("Minhas Candidaturas", icon("candidatura.png"), self.mostrar_candidaturas),
            ("Bolsas Disponíveis", icon("bolsa.png"), self.mostrar_bolsas),
            ("Avaliação Inteligente", icon("avaliacao.png"), self.mostrar_avaliacao),
            ("Relatórios Pessoais", icon("relatorio.png"), self.mostrar_relatorios),
            ("Meu Perfil", icon("perfil.png"), self.mostrar_perfil)
        ]

        for texto, icone, comando in menu:
            btn = ctk.CTkButton(
                self.sidebar,
                text=texto,
                image=icone,
                compound="left",
                anchor="w",
                fg_color="#142850",
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
            fg_color="#142850",
            hover_color="#2A3F5F",
            text_color="#FF6B6B",
            height=45,
            command=self.terminar_sessao
        )
        self.btn_logout.pack(side="bottom", fill="x", padx=15, pady=(0, 20))

        self.divisoria_logout = ctk.CTkFrame(self.sidebar, height=1, fg_color="#35506E")
        self.divisoria_logout.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

    def limpar_area_conteudo(self):
        for widget in list(self.area_conteudo.winfo_children()):
            try:
                widget.destroy()
            except Exception:
                pass

    def destacar_botao_menu(self, nome):
        for texto, botao in self.botoes.items():
            if texto == nome:
                botao.configure(fg_color="#11457B")
            else:
                botao.configure(fg_color="#142850")

    def reorganizar_layout_com_topo(self):
        self.area_conteudo.pack_forget()
        self.top_bar.pack(fill="x")
        self.divisoria_topo.pack(fill="x")
        self.area_conteudo.pack(fill="both", expand=True)

    def main_ui(self):
        self.main = ctk.CTkFrame(self.container, fg_color="#F5F7FB")
        self.main.pack(side="left", fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main, fg_color="#F5F7FB", height=70, corner_radius=0)
        self.top_bar.pack(fill="x")
        self.top_bar.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(self.top_bar, text="Painel Principal", font=("Segoe UI", 22, "bold"), text_color="#142850")
        self.label_titulo.pack(side="left", padx=30, pady=20)

        actions_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        actions_frame.pack(side="right", padx=30)

        # Perfil à direita com escopo de Estudante
        user = ctk.CTkFrame(actions_frame, fg_color="transparent")
        user.pack(side="left", padx=10)

        avatar = self.carregar("assets/perfil.png", (38, 38))
        if avatar:
            ctk.CTkLabel(user, image=avatar, text="").pack(side="left")
            
        texto = ctk.CTkFrame(user, fg_color="transparent")
        texto.pack(side="left", padx=12)

        ctk.CTkLabel(texto, text=self.nome_usuario, font=("Segoe UI", 13, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(texto, text="Estudante Beneficiário", font=("Segoe UI", 11), text_color="#6B7280").pack(anchor="w")

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

        ctk.CTkLabel(area, text=f"Bem-vindo de volta, {self.nome_usuario}! 👋", font=("Segoe UI", 28, "bold"), text_color="#162447").pack(anchor="w")
        
        # Carrega cartões dinâmicos com base de dados filtrada pelo ID do aluno
        dados_bd = self.obter_estatisticas_reais()

        cards_frame = ctk.CTkFrame(frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=35, pady=15)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.criar_card(cards_frame, 0, "Candidaturas", "Submetidas ao total", str(dados_bd["total"]), "#EEF4FF", "#C7D6FF", "assets/candidatura.png")
        self.criar_card(cards_frame, 1, "Pendentes", "Em análise regulamentar", str(dados_bd["pendentes"]), "#FFF8EA", "#FFE2A8", "assets/bolsa.png")
        self.criar_card(cards_frame, 2, "Aprovadas", "Prontas para benefício", str(dados_bd["aprovadas"]), "#ECFFF0", "#BFEFCC", "assets/casa.png")
        self.criar_card(cards_frame, 3, "Valor da Bolsa", "Total anual acumulado", f"{dados_bd['valor_total']:,} CVE".replace(",", "."), "#F6EEFF", "#D9C6FF", "assets/perfil.png")

        # Gráficos e Histórico Recente
        graficos_frame = ctk.CTkFrame(frame, fg_color="transparent")
        graficos_frame.pack(fill="both", expand=True, padx=35, pady=(15, 30))
        graficos_frame.grid_columnconfigure(0, weight=1)
        graficos_frame.grid_columnconfigure(1, weight=1)

        self.criar_grafico_pizza(graficos_frame, dados_bd["aprovadas"], dados_bd["pendentes"])
        self.criar_historico_recente(graficos_frame)

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

        if img:
            ctk.CTkLabel(bola, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")

        direita = ctk.CTkFrame(card, fg_color="transparent")
        direita.grid(row=0, column=1, sticky="e", padx=20)

        ctk.CTkLabel(direita, text=valor, font=("Segoe UI", 22, "bold"), text_color="#142850").pack(anchor="e")
        ctk.CTkLabel(direita, text=titulo, font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="e")
        ctk.CTkLabel(direita, text=subtitulo, font=("Segoe UI", 11), text_color="#6B7280").pack(anchor="e")

    def criar_grafico_pizza(self, parent, aprovadas, pendentes):
        box1 = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box1.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        valores = [max(aprovadas, 0), max(pendentes, 0)]
        labels = ['Aprovadas', 'Pendentes']

        if sum(valores) == 0:
            ctk.CTkLabel(box1, text="Estado das Candidaturas", font=("Segoe UI", 16, "bold"), text_color="#142850").pack(pady=(15, 10), anchor="w", padx=20)
            ctk.CTkLabel(box1, text="Sem candidaturas disponíveis", font=("Segoe UI", 12), text_color="#9CA3AF").pack(pady=40)
            return

        fig = Figure(figsize=(4, 3), dpi=85, facecolor='white')
        ax = fig.add_subplot(111)
        ax.pie(valores, labels=labels, autopct='%1.0f%%', colors=["#10B981", "#F59E0B"], startangle=90)
        ax.set_title("Estado das Candidaturas", fontsize=13, fontweight="bold", pad=10)

        canvas = FigureCanvasTkAgg(fig, master=box1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def criar_historico_recente(self, parent):
        box2 = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        box2.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        ctk.CTkLabel(box2, text="📋 Histórico Recente", font=("Segoe UI", 16, "bold"), text_color="#142850").pack(anchor="w", padx=20, pady=(15, 10))

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, bolsa_nome, data_candidatura, estado 
                FROM candidaturas 
                WHERE id_utilizador = ? 
                ORDER BY id DESC LIMIT 3
            """, (self.id_utilizador_logado,))
            registos = cursor.fetchall()
            conn.close()

            if registos:
                for reg in registos:
                    linha = ctk.CTkFrame(box2, fg_color="#F8FAFC", height=45, corner_radius=8)
                    linha.pack(fill="x", padx=20, pady=5)
                    
                    cor_estado = "#10B981" if reg[3] == "Aprovada" else "#F59E0B" if reg[3] == "Pendente" else "#EF4444"
                    ctk.CTkLabel(linha, text=f"C00{reg[0]}", font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)
                    ctk.CTkLabel(linha, text=reg[1], font=("Segoe UI", 11)).pack(side="left", padx=10)
                    ctk.CTkLabel(linha, text=reg[3], font=("Segoe UI", 11, "bold"), text_color=cor_estado).pack(side="right", padx=15)
                    ctk.CTkLabel(linha, text=reg[2], font=("Segoe UI", 11), text_color="#718096").pack(side="right", padx=10)
            else:
                ctk.CTkLabel(box2, text="Nenhum registo encontrado.", font=("Segoe UI", 12), text_color="#9CA3AF").pack(pady=40)
        except Exception:
            ctk.CTkLabel(box2, text="Erro ao carregar histórico.", font=("Segoe UI", 12), text_color="#EF4444").pack(pady=40)

    # Navegação das Páginas do Estudante
    def mostrar_painel(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Painel Principal")
        self.label_titulo.configure(text="Painel Principal")
        self.limpar_area_conteudo()
        self.carregar_painel()

    def mostrar_candidaturas(self):
        self.destacar_botao_menu("Minhas Candidaturas")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = Candidaturas(self.area_conteudo)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_bolsas(self):
        self.destacar_botao_menu("Bolsas Disponíveis")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = BolsasPage(self.area_conteudo, role="estudante", id_utilizador_logado=self.id_utilizador_logado)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

    def mostrar_avaliacao(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Avaliação Inteligente")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        
        frame_prolog = ctk.CTkFrame(self.area_conteudo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        frame_prolog.pack(fill="both", expand=True, padx=35, pady=20)
        
        ctk.CTkLabel(frame_prolog, text="🧠 Mecanismo de Inferência SIBES", font=("Segoe UI", 18, "bold"), text_color="#142850").pack(anchor="w", padx=30, pady=(30, 8))
        btn_validar = ctk.CTkButton(
            frame_prolog, text="🚀 Executar Avaliação de Elegibilidade", font=("Segoe UI", 13, "bold"),
            fg_color="#2563EB", hover_color="#1D4ED8", height=42, corner_radius=8,
            command=lambda: messagebox.showinfo("SIBES Prolog Engine", "Inferência executada com sucesso!\nTodos os critérios regulamentares estão em conformidade.")
        )
        btn_validar.pack(anchor="w", padx=30, pady=25)

    def mostrar_relatorios(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Relatórios Pessoais")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        
        frame_relatorios = ctk.CTkFrame(self.area_conteudo, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        frame_relatorios.pack(fill="both", expand=True, padx=35, pady=20)
        ctk.CTkLabel(frame_relatorios, text="📊 Meus Relatórios e Histórico", font=("Segoe UI", 18, "bold"), text_color="#142850").pack(anchor="w", padx=30, pady=(30, 8))

    def mostrar_perfil(self):
        self.reorganizar_layout_com_topo()
        self.destacar_botao_menu("Meu Perfil")
        self.top_bar.pack_forget()
        self.limpar_area_conteudo()
        pagina = PerfilUtilizador(self.area_conteudo, id_utilizador_logado=self.id_utilizador_logado)
        pagina.pack(fill="both", expand=True, padx=35, pady=20)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.withdraw()
    app = DashboardEstudante(root, id_utilizador_logado=1)
    root.mainloop()
