import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
import json

class PerfilUtilizador(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.pack(fill="both", expand=True)

        self.carregar_imagens()
        self.carregar_dados()
        self.criar_main()
        

    
    # CARREGAR IMAGENS
    
    def carregar(self, caminho, tamanho):

        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)

        return None

    def carregar_imagens(self):

        self.avatar = self.carregar("assets/perfil.png", (80, 80))

        self.edit_icon = self.carregar("assets/editar.png", (16, 16))

    # ==========================
    # CARREGAR DADOS DO UTILIZADOR
    # ==========================
    def carregar_dados(self):
        try:
            with open("dados_utilizador.json", "r", encoding="utf-8") as f:
                self.dados = json.load(f)
        except:
            self.dados = {
                "nome": "Administrador",
                "email": "admin@sibes.cv",
                "tipo": "Administrador",
                "telefone": "+238 999 99 99"
            }    

    
    # PÁGINA PRINCIPAL
    

    def criar_main(self):

        self.main = ctk.CTkScrollableFrame(self, fg_color="#F4F6FB")

        self.main.pack(fill="both", expand=True, padx=45, pady=30)

       
        # TÍTULO
       

        titulo = ctk.CTkFrame(self.main, fg_color="transparent")

        titulo.pack(fill="x")

        ctk.CTkLabel(
            titulo,
            text="Meu Perfil",
            font=("Segoe UI", 30, "bold"),
            text_color="#0B2A4A",
        ).pack(anchor="w")

        ctk.CTkLabel(
            titulo,
            text="Gerir informações da sua conta.",
            font=("Segoe UI", 14),
            text_color="#6B7280",
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkFrame(self.main, height=1, fg_color="#E5E7EB").pack(
            fill="x", pady=(20, 30)
        )

       
        # CARD
        

        card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB",
        )

        card.pack(fill="both", expand=True)

        container = ctk.CTkFrame(card, fg_color="transparent")

        container.pack(fill="both", expand=True, padx=60, pady=40)

        container.grid_columnconfigure(0, weight=1)

        container.grid_columnconfigure(1, weight=1)

        
        # COLUNA ESQUERDA
        

        col_esquerda = ctk.CTkFrame(container, fg_color="transparent")

        col_esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 40))

        ctk.CTkLabel(
            col_esquerda,
            text="Informações Pessoais",
            font=("Segoe UI", 18, "bold"),
            text_color="#0B2A4A",
        ).pack(anchor="w", pady=(0, 20))

        # Nome
        ctk.CTkLabel(
            col_esquerda,
            text="Nome Completo",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        ctk.CTkLabel(
            col_esquerda,
            text=self.dados["nome"],
            font=("Segoe UI", 15),
            text_color="#111827",
        ).pack(anchor="w", pady=(3, 18))

        # Email
        ctk.CTkLabel(
            col_esquerda,
            text="Email",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        ctk.CTkLabel(
            col_esquerda,
           text=self.dados["email"],
            font=("Segoe UI", 15),
            text_color="#111827",
        ).pack(anchor="w", pady=(3, 18))

        # Tipo
        ctk.CTkLabel(
            col_esquerda,
            text="Tipo de Utilizador",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        ctk.CTkLabel(
            col_esquerda,
            text=self.dados["tipo"],
            font=("Segoe UI", 15),
            text_color="#111827",
        ).pack(anchor="w", pady=(3, 18))

        # Telefone
        ctk.CTkLabel(
            col_esquerda,
            text="Telefone",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        ctk.CTkLabel(
            col_esquerda,
            text="+238 999 99 99",
            font=("Segoe UI", 15),
            text_color="#111827",
        ).pack(anchor="w", pady=(3, 30))

        ctk.CTkButton(
            col_esquerda,
            text="Editar Informações",
            image=self.edit_icon,
            compound="left",
            width=190,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=8,
            command=self.editar_informacoes,
        ).pack(anchor="w")

       
        # COLUNA DIREITA
        

        col_direita = ctk.CTkFrame(container, fg_color="transparent")

        col_direita.grid(row=0, column=1, sticky="nsew", padx=(40, 0))
        ctk.CTkLabel(
            col_direita,
            text="Alterar Palavra-passe",
            font=("Segoe UI", 18, "bold"),
            text_color="#0B2A4A",
        ).pack(anchor="w", pady=(0, 20))

        # Palavra-passe Atual
        ctk.CTkLabel(
            col_direita,
            text="Palavra-passe Atual",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        self.senha_atual = ctk.CTkEntry(
            col_direita,
            height=42,
            show="*",
            placeholder_text="Digite a palavra-passe atual",
        )
        self.senha_atual.pack(fill="x", pady=(5, 18))

        # Nova Palavra-passe
        ctk.CTkLabel(
            col_direita,
            text="Nova Palavra-passe",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        self.nova_senha = ctk.CTkEntry(
            col_direita,
            height=42,
            show="*",
            placeholder_text="Digite a nova palavra-passe",
        )
        self.nova_senha.pack(fill="x", pady=(5, 18))

        # Confirmar Palavra-passe
        ctk.CTkLabel(
            col_direita,
            text="Confirmar Nova Palavra-passe",
            font=("Segoe UI", 13, "bold"),
            text_color="#374151",
        ).pack(anchor="w")

        self.confirmar_senha = ctk.CTkEntry(
            col_direita,
            height=42,
            show="*",
            placeholder_text="Confirme a nova palavra-passe",
        )
        self.confirmar_senha.pack(fill="x", pady=(5, 28))

        ctk.CTkButton(
            col_direita,
            text="Alterar Palavra-passe",
            width=220,
            height=42,
            fg_color="#16A34A",
            hover_color="#15803D",
            corner_radius=8,
            command=self.alterar_senha,
        ).pack(anchor="w")

    
    # FUNÇÕES
   

    def editar_informacoes(self):
        messagebox.showinfo("Editar Informações", "Funcionalidade em desenvolvimento.")

    def alterar_senha(self):

        atual = self.senha_atual.get()
        nova = self.nova_senha.get()
        confirmar = self.confirmar_senha.get()

        if atual == "" or nova == "" or confirmar == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        if nova != confirmar:
            messagebox.showerror("Erro", "As palavras-passe não coincidem.")
            return

        messagebox.showinfo("Sucesso", "Palavra-passe alterada com sucesso.")


if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.geometry("1400x850")
    app.title("Perfil do Utilizador")

    PerfilUtilizador(app)

    app.mainloop()
