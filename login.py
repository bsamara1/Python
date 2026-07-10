import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os
import re
import random
import string
from datetime import datetime, timedelta
from database.database import DATABASE, conectar
from interface.admin.dashboard import App as DashboardAdmin
from interface.estudantes.dashboard1 import DashboardEstudante
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Login:

    def __init__(self, root):
        self.root = root
        self.root.title("SIBES - Sistema Inteligente de Bolsas de Estudo")
        self.root.after(100, lambda: self.root.state("zoomed"))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.configure(fg_color="#F5F7FB")

        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.email_guardado = ""
        self.lembrar_ativo = 0

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    dados = json.load(f)
                    self.email_guardado = dados.get("email", "")
                    self.lembrar_ativo = dados.get("lembrar", 0)
            except:
                pass

        self.mostrar_senha = False
        self.login_em_andamento = False
        self.criar_interface()

        if self.lembrar_ativo == 1 and self.email_guardado:
            self.email.insert(0, self.email_guardado)
            self.lembrar_var.set(1)

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

        self.label_erro_email = ctk.CTkLabel(
            self.card,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.label_erro_email.pack(anchor="w", padx=65, pady=(0, 15))

        # ==================================================
        # CAMPO SENHA
        # ==================================================
        label_senha_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        label_senha_frame.pack(anchor="w", padx=65, pady=(15, 0))

        ctk.CTkLabel(
            label_senha_frame,
            text="Palavra-passe",
            font=("Segoe UI", 14, "bold"),
            text_color="#081A3C"
        ).pack(side="left")

        self.btn_mostrar_senha = ctk.CTkButton(
            label_senha_frame,
            text="Mostrar",
            fg_color="transparent",
            hover=False,
            text_color="#2563EB",
            font=("Segoe UI", 11),
            command=self.alternar_visibilidade_senha
        )
        self.btn_mostrar_senha.pack(side="right")

        self.senha = ctk.CTkEntry(
            self.card,
            width=450,
            height=52,
            placeholder_text="Digite a sua palavra-passe",
            show="*",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.senha.pack(pady=(8, 2))
        self.senha.bind("<KeyRelease>", lambda e: self.limpar_erro_senha())

        self.label_erro_senha = ctk.CTkLabel(
            self.card,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.label_erro_senha.pack(anchor="w", padx=65, pady=(0, 15))

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
        self.btn_entrar = ctk.CTkButton(
            self.card,
            text="Entrar",
            width=450,
            height=55,
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.login
        )
        self.btn_entrar.pack(pady=(35, 25))

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
    # FUNÇÕES DE VALIDAÇÃO
    # ==================================================

    def validar_email(self, email):
        """Valida o formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    def mostrar_erro_email(self):
        """Destaca campo de email com erro"""
        self.email.configure(border_color="#EF4444", border_width=2)
        self.label_erro_email.configure(text="❌ Email inválido", text_color="#EF4444")

    def limpar_erro_email(self):
        """Remove destaque de erro do email"""
        self.email.configure(border_color="#E5E7EB", border_width=1)
        self.label_erro_email.configure(text="")

    def limpar_erro_senha(self):
        """Remove destaque de erro da senha"""
        self.senha.configure(border_color="#E5E7EB", border_width=1)
        self.label_erro_senha.configure(text="")

    def alternar_visibilidade_senha(self):
        """Alterna entre mostrar e esconder a senha"""
        self.mostrar_senha = not self.mostrar_senha
        if self.mostrar_senha:
            self.senha.configure(show="")
            self.btn_mostrar_senha.configure(text="Esconder")
        else:
            self.senha.configure(show="*")
            self.btn_mostrar_senha.configure(text="Mostrar")

    def validar_formulario_login(self):
        """Valida todo o formulário de login"""
        email = self.email.get().strip()
        senha = self.senha.get().strip()

        valido = True

        if not email:
            self.mostrar_erro_email()
            valido = False
        elif not self.validar_email(email):
            self.mostrar_erro_email()
            valido = False
        else:
            self.limpar_erro_email()

        if not senha:
            self.senha.configure(border_color="#EF4444", border_width=2)
            self.label_erro_senha.configure(text="❌ Palavra-passe obrigatória", text_color="#EF4444")
            valido = False
        else:
            self.senha.configure(border_color="#E5E7EB", border_width=1)
            self.label_erro_senha.configure(text="")

        return valido

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
        """Sistema de recuperação de password em múltiplos passos com código de verificação"""
        janela_recuperar = ctk.CTkToplevel(self.root)
        janela_recuperar.title("Recuperação de Palavra-passe")
        janela_recuperar.geometry("500x600")
        janela_recuperar.resizable(False, False)
        janela_recuperar.transient(self.root)
        janela_recuperar.grab_set()

        # ===== PASSO 1: Verificar Email =====
        def mostrar_passo1():
            for widget in frame_conteudo.winfo_children():
                widget.destroy()

            ctk.CTkLabel(frame_conteudo, text="Passo 1: Verificar Email", font=("Segoe UI", 18, "bold"), text_color="#081A3C").pack(pady=(20, 10))
            ctk.CTkLabel(frame_conteudo, text="Digite o email associado à sua conta.", font=("Segoe UI", 12), text_color="#6B7280").pack(pady=(0, 20))

            ctk.CTkLabel(frame_conteudo, text="Email", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
            entry_email = ctk.CTkEntry(frame_conteudo, width=400, height=40, placeholder_text="seu.email@example.com", border_width=1, border_color="#E5E7EB")
            entry_email.pack(pady=(5, 20), padx=30)

            def verificar_email():
                email = entry_email.get().strip()
                if not email or not self.validar_email(email):
                    messagebox.showwarning("Aviso", "Por favor, digite um email válido.", parent=janela_recuperar)
                    return

                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nome FROM utilizadores WHERE email = ?", (email,))
                    resultado = cursor.fetchone()
                    conn.close()

                    if resultado:
                        utilizador_id, nome_utilizador = resultado
                        # Gerar código de verificação
                        codigo = ''.join(random.choices(string.digits, k=6))
                        mostrar_passo2(email, utilizador_id, codigo)
                    else:
                        messagebox.showerror("Erro", "Este email não está registado no sistema.", parent=janela_recuperar)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao aceder à BD: {e}", parent=janela_recuperar)

            ctk.CTkButton(frame_conteudo, text="Continuar", font=("Segoe UI", 13, "bold"), height=40, width=400, command=verificar_email).pack(pady=(20, 0), padx=30)

        # ===== PASSO 2: Código de Verificação =====
        def mostrar_passo2(email, usuario_id, codigo_verificacao):
            for widget in frame_conteudo.winfo_children():
                widget.destroy()

            ctk.CTkLabel(frame_conteudo, text="Passo 2: Verificação", font=("Segoe UI", 18, "bold"), text_color="#081A3C").pack(pady=(20, 10))
            ctk.CTkLabel(frame_conteudo, text=f"Um código foi enviado para {email}", font=("Segoe UI", 11), text_color="#6B7280").pack(pady=(0, 15))

            ctk.CTkLabel(frame_conteudo, text="Código de Verificação", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
            entry_codigo = ctk.CTkEntry(frame_conteudo, width=400, height=40, placeholder_text="Código de 6 dígitos", border_width=1, border_color="#E5E7EB")
            entry_codigo.pack(pady=(5, 20), padx=30)

            label_info = ctk.CTkLabel(frame_conteudo, text="Simulação: código = " + codigo_verificacao, font=("Segoe UI", 10), text_color="#F59E0B")
            label_info.pack(pady=(0, 15))

            def verificar_codigo():
                codigo_digitado = entry_codigo.get().strip()
                if codigo_digitado != codigo_verificacao:
                    messagebox.showwarning("Aviso", "Código incorreto. Tente novamente.", parent=janela_recuperar)
                    return
                mostrar_passo3(email, usuario_id)

            ctk.CTkButton(frame_conteudo, text="Verificar", font=("Segoe UI", 13, "bold"), height=40, width=400, command=verificar_codigo).pack(pady=(20, 0), padx=30)

        # ===== PASSO 3: Nova Palavra-passe =====
        def mostrar_passo3(email, usuario_id):
            for widget in frame_conteudo.winfo_children():
                widget.destroy()

            ctk.CTkLabel(frame_conteudo, text="Passo 3: Nova Palavra-passe", font=("Segoe UI", 18, "bold"), text_color="#081A3C").pack(pady=(20, 10))
            ctk.CTkLabel(frame_conteudo, text="Digite uma nova palavra-passe segura.", font=("Segoe UI", 12), text_color="#6B7280").pack(pady=(0, 20))

            ctk.CTkLabel(frame_conteudo, text="Nova Palavra-passe", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
            entry_senha = ctk.CTkEntry(frame_conteudo, width=400, height=40, placeholder_text="Mínimo 6 caracteres", show="*", border_width=1, border_color="#E5E7EB")
            entry_senha.pack(pady=(5, 15), padx=30)

            ctk.CTkLabel(frame_conteudo, text="Confirmar Palavra-passe", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
            entry_confirmar = ctk.CTkEntry(frame_conteudo, width=400, height=40, placeholder_text="Confirme a palavra-passe", show="*", border_width=1, border_color="#E5E7EB")
            entry_confirmar.pack(pady=(5, 20), padx=30)

            def atualizar_senha():
                senha = entry_senha.get().strip()
                confirmar = entry_confirmar.get().strip()

                if not senha or not confirmar:
                    messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.", parent=janela_recuperar)
                    return

                if len(senha) < 6:
                    messagebox.showwarning("Aviso", "A palavra-passe deve ter mínimo 6 caracteres.", parent=janela_recuperar)
                    return

                if senha != confirmar:
                    messagebox.showwarning("Aviso", "As palavras-passe não coincidem.", parent=janela_recuperar)
                    return

                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE utilizadores SET senha = ? WHERE id = ?", (senha, usuario_id))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Sucesso", "Palavra-passe alterada com sucesso!\n\nJá pode fazer login com a nova palavra-passe.", parent=janela_recuperar)
                    janela_recuperar.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar: {e}", parent=janela_recuperar)

            ctk.CTkButton(frame_conteudo, text="Atualizar Palavra-passe", font=("Segoe UI", 13, "bold"), height=40, width=400, command=atualizar_senha).pack(pady=(20, 0), padx=30)

        # Frame principal para conteúdo dinâmico
        frame_conteudo = ctk.CTkFrame(janela_recuperar, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

        mostrar_passo1()

    def login(self):
        if not self.validar_formulario_login():
            return

        if self.login_em_andamento:
            return

        self.login_em_andamento = True
        self.btn_entrar.configure(state="disabled", text="A processar...")
        self.root.update()

        email = self.email.get().strip()
        senha = self.senha.get().strip()

        try:
            conn = conectar()
            cursor = conn.cursor()

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
                perfil = utilizador[3]

                try:
                    if self.lembrar_var.get() == 1:
                        dados_config = {"email": email, "lembrar": 1}
                    else:
                        dados_config = {"email": "", "lembrar": 0}

                    with open(self.config_file, "w") as f:
                        json.dump(dados_config, f, indent=4)
                except Exception as e:
                    print(f"Erro ao salvar config: {e}")

                messagebox.showinfo("Sucesso", f"Login efetuado! Bem-vindo, {nome_utilizador}.")
                self.root.withdraw()

                if perfil == "Administrador":
                    dashboard = DashboardAdmin(parent=self.root, id_utilizador_logado=id_utilizador)
                    dashboard.protocol("WM_DELETE_WINDOW", lambda: [dashboard.destroy(), self.root.destroy()])
                    dashboard.mainloop()
                elif perfil == "Estudante":
                    dashboard = DashboardEstudante(parent=self.root, id_utilizador_logado=id_utilizador)
                    dashboard.protocol("WM_DELETE_WINDOW", lambda: [dashboard.destroy(), self.root.destroy()])
                    dashboard.mainloop()
                else:
                    messagebox.showerror("Erro", f"Tipo de perfil não mapeado no sistema: {perfil}")
                    self.root.deiconify()
            else:
                self.email.configure(border_color="#EF4444", border_width=2)
                self.senha.configure(border_color="#EF4444", border_width=2)
                messagebox.showerror("Erro de Autenticação", "Email ou palavra-passe incorretos.")

        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao aceder à base de dados:\n{erro}")

        finally:
            self.login_em_andamento = False
            self.btn_entrar.configure(state="normal", text="Entrar")
            self.root.update()

if __name__ == "__main__":
    from database.database import criar_base
    criar_base()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = Login(root)
    root.mainloop()
