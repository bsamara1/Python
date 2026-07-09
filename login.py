import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os
# Importação interna do seu próprio módulo de base de dados
from database.database import DATABASE, conectar

# Importação da sua Dashboard do Admin
from interface.admin.dashboard import App as DashboardAdmin

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Login:

    def __init__(self, root):
        self.root = root
        self.root.title("SIBES - Sistema Inteligente de Bolsas de Estudo")
        self.root.after(100, lambda: self.root.state("zoomed"))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.configure(fg_color="#F5F7FB")
        self.criar_interface()

    def criar_interface(self):
        # ==================================================
        # CONTAINER PRINCIPAL
        # ==================================================
        self.main = ctk.CTkFrame(self.root, fg_color="#F5F7FB")
        self.main.pack(fill="both", expand=True)

        # ==================================================
        # SIDEBAR
        # ==================================================
        self.sidebar = ctk.CTkFrame(self.main, width=120, fg_color="#081A3C", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ==================================================
        # ÁREA ESQUERDA
        # ==================================================
        self.left_area = ctk.CTkFrame(self.main, fg_color="#F5F7FB")
        self.left_area.pack(side="left", fill="both", expand=True)

        # ==================================================
        # LOGO + SIBES
        # ==================================================
        logo_frame = ctk.CTkFrame(self.left_area, fg_color="transparent")
        logo_frame.place(x=90, y=130)

        try:
            logo = Image.open("assets/logo.png")
            self.logo_img = ctk.CTkImage(light_image=logo, dark_image=logo, size=(180, 180))
            ctk.CTkLabel(logo_frame, image=self.logo_img, text="").pack(side="left")
        except:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="SIBES",
            font=("Segoe UI", 80, "bold"),
            text_color="#081A3C"
        ).pack(side="left", padx=(30, 0))

        # ==================================================
        # SUBTÍTULO
        # ==================================================
        ctk.CTkLabel(
            self.left_area,
            text="Sistema Inteligente de\nBolsas de Estudo Sustentáveis",
            font=("Segoe UI", 25, "normal"),
            text_color="#4B5563",
            justify="center"
        ).place(x=230, y=300)

        # ==================================================
        # IMAGEM PRINCIPAL
        # ==================================================
        try:
            img = Image.open("assets/img1.png")
            self.main_img = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 550))
            ctk.CTkLabel(self.left_area, image=self.main_img, text="").place(x=20, y=390)
        except:
            pass

        # ==================================================
        # CARD LOGIN
        # ==================================================
        self.card = ctk.CTkFrame(
            self.main,
            width=580,
            height=760,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )
        self.card.place(relx=0.74, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # ==================================================
        # TÍTULOS DO CARD
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Bem-vindo de volta!",
            font=("Segoe UI", 32, "bold"),
            text_color="#081A3C"
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            self.card,
            text="Inicie sessão para continuar",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        ).pack(pady=(0, 40))

        # ==================================================
        # CAMPO EMAIL
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Email",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.email = ctk.CTkEntry(self.card, width=450, height=52, placeholder_text="exemplo@email.com")
        self.email.pack(pady=(8, 20))

        # ==================================================
        # CAMPO SENHA
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Palavra-passe",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(anchor="w", padx=65)

        self.senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Digite a sua palavra-passe",
            show="*"
        )
        self.senha.pack(pady=(8, 20))

        # ==================================================
        # OPÇÕES ADICIONAIS
        # ==================================================
        opcoes = ctk.CTkFrame(self.card, fg_color="transparent")
        opcoes.pack(fill="x", padx=65)

        self.lembrar_var = ctk.IntVar()

        ctk.CTkCheckBox(
            opcoes,
            text="Lembrar-me",
            text_color="#081A3C",
            variable=self.lembrar_var
        ).pack(side="left")

        ctk.CTkButton(
            opcoes,
            text="Esqueceu a palavra-passe?",
            fg_color="transparent",
            hover=False,
            text_color="#2563EB",
            command=self.esqueceu_senha
        ).pack(side="right")

        # ==================================================
        # BOTÃO ENTRAR
        # ==================================================
        ctk.CTkButton(
            self.card,
            text="Entrar",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self.login
        ).pack(pady=(35, 25))

        # ==================================================
        # RODAPÉ (REGISTO DE CONTA)
        # ==================================================
        rodape = ctk.CTkFrame(self.card, fg_color="transparent")
        rodape.pack()

        ctk.CTkLabel(
            rodape,
            text="Não tem conta?",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(side="left")

        ctk.CTkButton(
            rodape,
            text="Criar conta de estudante",
            fg_color="transparent",
            hover=False,
            text_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=self.criar_conta
        ).pack(side="left")

    # ==================================================
    # FUNÇÕES DE EVENTO
    # ==================================================

    def criar_conta(self):
        try:
            from criarConta import CriarConta
            janela_registo = ctk.CTkToplevel(self.root)
            janela_registo.title("Criar Conta")
            CriarConta(janela_registo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o ecrã de registo:\n{e}")

    def esqueceu_senha(self):
        messagebox.showinfo("Recuperação", "Instruções enviadas para o seu email.")

    def login(self):
        email = self.email.get().strip()
        senha = self.senha.get().strip()

        if email == "" or senha == "":
            messagebox.showwarning("Campos Vazios", "Preencha o email e a palavra-passe.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Busca as 5 colunas essenciais
            cursor.execute("""
                SELECT id, nome, email, perfil, telefone 
                FROM utilizadores
                WHERE email = ? AND senha = ?
            """, (email, senha))

            utilizador = cursor.fetchone()
            conn.close()

            if utilizador:
                id_utilizador = utilizador[0]
                nome_utilizador = utilizador[1]
                email_utilizador = utilizador[2]
                perfil = utilizador[3]
                telefone_utilizador = utilizador[4] # Captura o telefone do utilizador

                messagebox.showinfo("Sucesso", f"Login efetuado! Bem-vindo, {nome_utilizador}.")
                
                # Oculta a janela de login para não quebrar animações do CustomTkinter
                self.root.withdraw()

                if perfil == "Administrador":
                    # Passa o ID detetado para a DashboardAdmin
                    dashboard = DashboardAdmin(parent=self.root,id_utilizador_logado=id_utilizador)
                    # Mata o processo do Python por completo quando a Dashboard for fechada
                    dashboard.protocol("WM_DELETE_WINDOW", lambda: [dashboard.destroy(), self.root.destroy()])
                    self.root.withdraw()
                    dashboard.mainloop()
                else:
                    messagebox.showerror("Erro", "Tipo de perfil não mapeado no sistema.")
            else:
                messagebox.showerror("Erro", "Email ou palavra-passe incorretos.")

        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao aceder à base de dados:\n{erro}")

if __name__ == "__main__":
    from database.database import criar_base
    criar_base()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = Login(root)
    root.mainloop()