import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from login import Login


class CriarConta:

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
        self.main = ctk.CTkFrame(
            self.root,
            fg_color="#F5F7FB"
        )
        self.main.pack(fill="both", expand=True)

        # ==================================================
        # ÁREA ESQUERDA
        # ==================================================
        self.left_area = ctk.CTkFrame(
            self.main,
            fg_color="#F5F7FB"
        )
        self.left_area.pack(side="left", fill="both", expand=True)

        # ==================================================
        # LOGO + SIBES
        # ==================================================
        logo_frame = ctk.CTkFrame(self.left_area, fg_color="transparent")
        logo_frame.place(x=90, y=130)

        try:
            logo = Image.open("assets/logo.png")

            self.logo_img = ctk.CTkImage(
                light_image=logo,
                dark_image=logo,
                size=(180, 180)
            )

            ctk.CTkLabel(
                logo_frame,
                image=self.logo_img,
                text=""
            ).pack(side="left")

        except Exception:
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
            font=("Segoe UI", 25),
            text_color="#4B5563",
            justify="center"
        ).place(x=230, y=300)

        # ==================================================
        # IMAGEM PRINCIPAL
        # ==================================================
        try:
            img = Image.open("assets/img1.png")

            self.main_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(800, 550)
            )

            ctk.CTkLabel(
                self.left_area,
                image=self.main_img,
                text=""
            ).place(x=20, y=390)

        except Exception:
            pass

        # ==================================================
        # CARD REGISTO
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
        # TÍTULO
        # ==================================================
        ctk.CTkLabel(
            self.card,
            text="Criar Conta",
            font=("Segoe UI", 32, "bold"),
            text_color="#081A3C"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self.card,
            text="Preencha os dados para criar a sua conta",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        ).pack(pady=(0, 30))

        # ==================================================
        # NOME
        # ==================================================
        ctk.CTkLabel(self.card, text="Nome Completo",
                     font=("Segoe UI", 14, "bold"),
                     text_color="#081A3C").pack(anchor="w", padx=65)

        self.nome = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Digite o seu nome completo"
        )
        self.nome.pack(pady=(8, 15))

        # ==================================================
        # EMAIL
        # ==================================================
        ctk.CTkLabel(self.card, text="Email",
                     font=("Segoe UI", 14, "bold"),
                     text_color="#081A3C").pack(anchor="w", padx=65)

        self.email = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="exemplo@email.com"
        )
        self.email.pack(pady=(8, 15))

        # ==================================================
        # SENHA
        # ==================================================
        ctk.CTkLabel(self.card, text="Palavra-passe",
                     font=("Segoe UI", 14, "bold"),
                     text_color="#081A3C").pack(anchor="w", padx=65)

        self.senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            show="*",
            placeholder_text="Digite a sua palavra-passe"
        )
        self.senha.pack(pady=(8, 15))

        # ==================================================
        # CONFIRMAR SENHA
        # ==================================================
        ctk.CTkLabel(self.card, text="Confirmar Palavra-passe",
                     font=("Segoe UI", 14, "bold"),
                     text_color="#081A3C").pack(anchor="w", padx=65)

        self.confirmar_senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            show="*",
            placeholder_text="Confirme a sua palavra-passe"
        )
        self.confirmar_senha.pack(pady=(8, 25))

        # ==================================================
        # BOTÃO
        # ==================================================
        ctk.CTkButton(
            self.card,
            text="Criar Conta",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self.criar_conta
        ).pack()

        # ==================================================
        # FOOTER
        # ==================================================
        rodape = ctk.CTkFrame(self.card, fg_color="transparent")
        rodape.pack(pady=(25, 0))

        ctk.CTkLabel(
            rodape,
            text="Já tem conta?",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        ).pack(side="left")

        ctk.CTkButton(
            rodape,
            text="Entrar",
            fg_color="transparent",
            hover=False,
            text_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_login
        ).pack(side="left", padx=(5, 0))

    # ==================================================
    # FUNÇÕES
    # ==================================================
    def criar_conta(self):

        nome = self.nome.get()
        email = self.email.get()
        senha = self.senha.get()
        confirmar = self.confirmar_senha.get()

        if not nome or not email or not senha or not confirmar:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As palavras-passe não coincidem.")
            return

        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")

    def abrir_login(self):

        from login import Login

        janela_login = ctk.CTkToplevel(self.root)
        janela_login.title("Login")

        Login(janela_login)


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":

    root = ctk.CTk()
    app = CriarConta(root)
    root.mainloop()