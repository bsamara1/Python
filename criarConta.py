import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import re
import os
import json

try:
    from database import registar_novo_estudante
except ImportError:
    from database.database import registar_novo_estudante


class CriarConta:

    def __init__(self, root):
        self.root = root
        self.root.title("SIBES - Sistema Inteligente de Bolsas de Estudo")
        self.root.after(100, lambda: self.root.state("zoomed"))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.configure(fg_color="#F5F7FB")

        self.criando_conta = False
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
        self.card = ctk.CTkScrollableFrame(
            self.main,
            width=580,
            height=760,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )
        self.card.place(relx=0.74, rely=0.5, anchor="center")

        # ==================================================
        # TÍTULOS
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
        # CAMPO NOME
        # ==================================================
        ctk.CTkLabel(self.card, text="Nome Completo", font=("Segoe UI", 14, "bold"), text_color="#081A3C").pack(anchor="w", padx=65)
        self.nome = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Digite o seu nome completo",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.nome.pack(pady=(8, 2))
        self.nome.bind("<KeyRelease>", lambda e: self.limpar_erro_nome())
        self.label_erro_nome = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11), text_color="#EF4444")
        self.label_erro_nome.pack(anchor="w", padx=65, pady=(0, 12))

        # ==================================================
        # CAMPO EMAIL
        # ==================================================
        ctk.CTkLabel(self.card, text="Email", font=("Segoe UI", 14, "bold"), text_color="#081A3C").pack(anchor="w", padx=65)
        self.email = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="exemplo@email.com",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.email.pack(pady=(8, 2))
        self.email.bind("<KeyRelease>", lambda e: self.limpar_erro_email())
        self.label_erro_email = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11), text_color="#EF4444")
        self.label_erro_email.pack(anchor="w", padx=65, pady=(0, 12))

        # ==================================================
        # CAMPO SENHA
        # ==================================================
        ctk.CTkLabel(self.card, text="Palavra-passe", font=("Segoe UI", 14, "bold"), text_color="#081A3C").pack(anchor="w", padx=65)
        self.senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            show="*",
            placeholder_text="Mín. 8 caracteres (números, maiúsculas, símbolos)",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.senha.pack(pady=(8, 2))
        self.senha.bind("<KeyRelease>", lambda e: self.avaliar_forca_senha())
        self.label_erro_senha = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11), text_color="#EF4444")
        self.label_erro_senha.pack(anchor="w", padx=65, pady=(0, 2))

        # Indicador de força da senha
        self.label_forca_senha = ctk.CTkLabel(
            self.card,
            text="",
            font=("Segoe UI", 10),
            text_color="#6B7280"
        )
        self.label_forca_senha.pack(anchor="w", padx=65, pady=(0, 12))

        # ==================================================
        # CAMPO CONFIRMAR SENHA
        # ==================================================
        ctk.CTkLabel(self.card, text="Confirmar Palavra-passe", font=("Segoe UI", 14, "bold"), text_color="#081A3C").pack(anchor="w", padx=65)
        self.confirmar_senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            show="*",
            placeholder_text="Confirme a sua palavra-passe",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.confirmar_senha.pack(pady=(8, 2))
        self.confirmar_senha.bind("<KeyRelease>", lambda e: self.limpar_erro_confirmar_senha())
        self.label_erro_confirmar_senha = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11), text_color="#EF4444")
        self.label_erro_confirmar_senha.pack(anchor="w", padx=65, pady=(0, 15))

        # ==================================================
        # CHECKBOX TERMOS
        # ==================================================
        self.termos_var = ctk.IntVar(value=0)
        self.cb_termos = ctk.CTkCheckBox(
            self.card,
            text="Concordo com os Termos de Serviço e Política de Privacidade",
            font=("Segoe UI", 11),
            text_color="#081A3C",
            variable=self.termos_var,
            checkbox_width=20,
            checkbox_height=20
        )
        self.cb_termos.pack(anchor="w", padx=65, pady=(5, 15))
        self.label_erro_termos = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11), text_color="#EF4444")
        self.label_erro_termos.pack(anchor="w", padx=65, pady=(0, 10))

        # ==================================================
        # BOTÃO SUBMIT
        # ==================================================
        self.btn_criar = ctk.CTkButton(
            self.card,
            text="Criar Conta",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            command=self.criar_conta
        )
        self.btn_criar.pack()

        # ==================================================
        # RODAPÉ (IR PARA LOGIN)
        # ==================================================
        rodape = ctk.CTkFrame(self.card, fg_color="transparent")
        rodape.pack(pady=(25, 0))

        ctk.CTkLabel(rodape, text="Já tem conta?", font=("Segoe UI", 14), text_color="#6B7280").pack(side="left")

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
    # MÉTODOS DE VALIDAÇÃO
    # ==================================================

    def validar_email(self, email):
        """Valida o formato de email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    def validar_forca_senha(self, senha):
        """Retorna tuple (é_forte, mensagem)"""
        if len(senha) < 8:
            return False, "❌ Mínimo 8 caracteres"
        if not re.search(r'[A-Z]', senha):
            return False, "❌ Precisa de pelo menos 1 maiúscula"
        if not re.search(r'[a-z]', senha):
            return False, "❌ Precisa de pelo menos 1 minúscula"
        if not re.search(r'[0-9]', senha):
            return False, "❌ Precisa de pelo menos 1 número"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            return False, "❌ Precisa de pelo menos 1 símbolo (!@#$%^&*)"
        return True, "✅ Palavra-passe forte"

    def avaliar_forca_senha(self):
        """Avalia e mostra a força da senha em tempo real"""
        senha = self.senha.get()
        if not senha:
            self.label_forca_senha.configure(text="")
            self.label_erro_senha.configure(text="")
            return

        eh_forte, mensagem = self.validar_forca_senha(senha)
        cor = "#10B981" if eh_forte else "#F59E0B"
        self.label_forca_senha.configure(text=mensagem, text_color=cor)
        self.label_erro_senha.configure(text="")

    def limpar_erro_nome(self):
        """Limpa erro de nome ao digitar"""
        self.nome.configure(border_color="#E5E7EB", border_width=1)
        self.label_erro_nome.configure(text="")

    def limpar_erro_email(self):
        """Limpa erro de email ao digitar"""
        self.email.configure(border_color="#E5E7EB", border_width=1)
        self.label_erro_email.configure(text="")

    def limpar_erro_confirmar_senha(self):
        """Limpa erro de confirmação de senha ao digitar"""
        self.confirmar_senha.configure(border_color="#E5E7EB", border_width=1)
        self.label_erro_confirmar_senha.configure(text="")

    def validar_formulario(self):
        """Valida todo o formulário antes de criar conta"""
        nome = self.nome.get().strip()
        email = self.email.get().strip()
        senha = self.senha.get().strip()
        confirmar = self.confirmar_senha.get().strip()

        valido = True

        # Validar nome
        if not nome:
            self.nome.configure(border_color="#EF4444", border_width=2)
            self.label_erro_nome.configure(text="❌ Nome obrigatório")
            valido = False
        elif len(nome) < 3:
            self.nome.configure(border_color="#EF4444", border_width=2)
            self.label_erro_nome.configure(text="❌ Nome deve ter mínimo 3 caracteres")
            valido = False
        else:
            self.limpar_erro_nome()

        # Validar email
        if not email:
            self.email.configure(border_color="#EF4444", border_width=2)
            self.label_erro_email.configure(text="❌ Email obrigatório")
            valido = False
        elif not self.validar_email(email):
            self.email.configure(border_color="#EF4444", border_width=2)
            self.label_erro_email.configure(text="❌ Email inválido")
            valido = False
        else:
            self.limpar_erro_email()

        # Validar senha
        if not senha:
            self.senha.configure(border_color="#EF4444", border_width=2)
            self.label_erro_senha.configure(text="❌ Palavra-passe obrigatória")
            valido = False
        else:
            eh_forte, mensagem = self.validar_forca_senha(senha)
            if not eh_forte:
                self.senha.configure(border_color="#EF4444", border_width=2)
                self.label_erro_senha.configure(text=mensagem)
                valido = False
            else:
                self.senha.configure(border_color="#E5E7EB", border_width=1)

        # Validar confirmação de senha
        if not confirmar:
            self.confirmar_senha.configure(border_color="#EF4444", border_width=2)
            self.label_erro_confirmar_senha.configure(text="❌ Confirmação obrigatória")
            valido = False
        elif senha != confirmar:
            self.confirmar_senha.configure(border_color="#EF4444", border_width=2)
            self.label_erro_confirmar_senha.configure(text="❌ Palavras-passe não coincidem")
            valido = False
        else:
            self.limpar_erro_confirmar_senha()

        # Validar termos
        if self.termos_var.get() != 1:
            self.label_erro_termos.configure(text="❌ Deve aceitar os termos")
            valido = False
        else:
            self.label_erro_termos.configure(text="")

        return valido

    # ==================================================
    # REGRAS DE NEGÓCIO E FLUXO
    # ==================================================
    def criar_conta(self):
        if not self.validar_formulario():
            return

        if self.criando_conta:
            return

        self.criando_conta = True
        self.btn_criar.configure(state="disabled", text="A processar...")
        self.root.update()

        nome = self.nome.get().strip()
        email = self.email.get().strip()
        senha = self.senha.get().strip()

        try:
            sucesso = registar_novo_estudante(nome=nome, email=email, senha=senha)

            if sucesso:
                messagebox.showinfo("Sucesso", "Conta de estudante criada com sucesso!\nAgora pode fazer login com o seu email.")
                self.abrir_login()
            else:
                self.email.configure(border_color="#EF4444", border_width=2)
                self.label_erro_email.configure(text="❌ Este email já está registado")
                messagebox.showerror("Erro", "Este email já se encontra registado no sistema.")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível interagir com a base de dados:\n{e}")

        finally:
            self.criando_conta = False
            self.btn_criar.configure(state="normal", text="Criar Conta")
            self.root.update()

    def abrir_login(self):
        # Limpa o ecrã atual destruindo o frame principal
        self.main.destroy()

        # Limpa qualquer login anteriormente "lembrado" (ex.: admin), para que o
        # ecrã de login abra em branco e o utilizador introduza as credenciais
        # da conta que acabou de criar, sem confusão com outra conta guardada.
        try:
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            with open(config_file, "w") as f:
                json.dump({"email": "", "lembrar": 0}, f, indent=4)
        except Exception:
            pass

        # Importa localmente para evitar problemas de importação circular
        from login import Login

        # Reconstrói a interface de login sobre a mesma janela root
        Login(self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    app = CriarConta(root)
    root.mainloop()
