# dashboard.py
import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# Importação de todas as páginas locais

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIBES - Sistema de Gestão de Bolsas de Estudo (Admin)")
        self.state("zoomed")
        self.geometry("1280x720")
        
        ctk.set_appearance_mode("Light")
        self.configure(fg_color="#F4F6FB")

        self.pagina_atual_frame = None
        self.botoes_sidebar = {}

        self.construir_layout()
        self.selecionar_menu("estudantes", EstudantesPage)

    def construir_layout(self):
        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(fill="both", expand=True)

        # Sidebar Lateral Esquerda
        self.sidebar = ctk.CTkFrame(self.container_principal, width=260, fg_color="#1E293B", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Contentor Central Dinâmico
        self.area_conteudo = ctk.CTkFrame(self.container_principal, fg_color="transparent")
        self.area_conteudo.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        self.construir_sidebar_elementos()

    def carregar_icone(self, nome_arquivo, tamanho=(20, 20)):
        caminho = os.path.join(os.path.dirname(__file__), "assets", nome_arquivo)
        if os.path.exists(caminho):
            return ctk.CTkImage(light_image=Image.open(caminho), size=tamanho)
        return None

    def construir_sidebar_elementos(self):
        lbl_logo = ctk.CTkLabel(self.sidebar, text="🎓 SIBES", font=("Segoe UI", 24, "bold"), text_color="#F8FAFC")
        lbl_logo.pack(pady=(35, 5), padx=20, anchor="w")
        
        lbl_sub = ctk.CTkLabel(self.sidebar, text="Painel do Administrador", font=("Segoe UI", 12), text_color="#94A3B8")
        lbl_sub.pack(pady=(0, 35), padx=25, anchor="w")

        opcoes_menu = {
            "estudantes": ["Estudantes", EstudantesPage, "students.png"],
            "bolsas": ["Bolsas de Estudo", BolsasPage, "scholarships.png"],
            "candidaturas": ["Candidaturas", CandidaturasPage, "applications.png"],
            "avaliacao": ["Avaliação (Prolog)", AvaliacaoPage, "prolog.png"],
            "relatorios": ["Relatórios", RelatoriosPage, "reports.png"],
            "utilizadores": ["Gestão Utilizadores", UtilizadoresPage, "users.png"],
            "perfil": ["O Meu Perfil", PerfilUtilizador, "profile.png"]
        }

        for chave, dados in opcoes_menu.items():
            texto, classe_janela, arquivo_icone = dados
            icone = self.carregar_icone(arquivo_icone)

            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {texto}",
                image=icone,
                font=("Segoe UI", 14, "medium"),
                fg_color="transparent",
                text_color="#94A3B8",
                hover_color="#334155",
                height=45,
                corner_radius=8,
                anchor="w",
                command=lambda c=chave, cls=classe_janela: self.selecionar_menu(c, cls)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.botoes_sidebar[chave] = btn

        frame_espacador = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=1)
        frame_espacador.pack(fill="both", expand=True)

        btn_sair = ctk.CTkButton(
            self.sidebar,
            text="  Terminar Sessão",
            image=self.carregar_icone("logout.png"),
            font=("Segoe UI", 14),
            fg_color="transparent",
            text_color="#FCA5A5",
            hover_color="#EF4444",
            height=45,
            corner_radius=8,
            anchor="w",
            command=self.terminar_sessao
        )
        btn_sair.pack(fill="x", padx=15, pady=(0, 25))

    def selecionar_menu(self, chave_ativa, classe_pagina):
        for chave, botao in self.botoes_sidebar.items():
            if chave == chave_ativa:
                botao.configure(fg_color="#2563EB", text_color="#FFFFFF")
            else:
                botao.configure(fg_color="transparent", text_color="#94A3B8")

        if self.pagina_atual_frame is not None:
            self.pagina_atual_frame.destroy()

        self.pagina_atual_frame = classe_pagina(self.area_conteudo)
        self.pagina_atual_frame.pack(fill="both", expand=True)

    def terminar_sessao(self):
        if messagebox.askyesno("Sair", "Tens a certeza de que desejas sair do SIBES?"):
            self.destroy()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()