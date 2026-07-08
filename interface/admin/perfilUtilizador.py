# perfilUtilizador.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
import json

class PerfilUtilizador(ctk.CTkFrame):
    """Página do Perfil adaptada sem autopackamento"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.carregar_imagens()
        self.carregar_dados()
        self.criar_main()

    def carregar(self, caminho, tamanho):
        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)
        return None

    def carregar_imagens(self):
        self.avatar = self.carregar("assets/perfil.png", (80, 80))
        self.edit_icon = self.carregar("assets/editar.png", (16, 16))

    def carregar_dados(self):
        try:
            if os.path.exists("dados_utilizador.json"):
                with open("dados_utilizador.json", "r", encoding="utf-8") as f:
                    self.dados = json.load(f)
            else:
                raise FileNotFoundError
        except Exception:
            # Fallback seguro para evitar que a UI quebre se o JSON falhar
            self.dados = {
                "nome": "Administrador Principal",
                "email": "admin@sibes.pt",
                "cargo": "Gestor Geral de Sistemas"
            }

    def criar_main(self):
        card_topo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        card_topo.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(card_topo, text="👤 Configurações da Conta", font=("Segoe UI", 22, "bold"), text_color="#1E293B").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_topo, text="Gerencie as suas credenciais de acesso, e-mail institucional e palavra-passe.", font=("Segoe UI", 13), text_color="#64748B").pack(anchor="w", padx=20, pady=(0, 20))

        conteudo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        conteudo.pack(fill="both", expand=True, padx=0, pady=0)

        frame_info = ctk.CTkFrame(conteudo, fg_color="transparent")
        frame_info.pack(padx=30, pady=30, fill="x")

        ctk.CTkLabel(frame_info, text=f"Nome: {self.dados.get('nome', 'N/A')}", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=5)
        ctk.CTkLabel(frame_info, text=f"E-mail: {self.dados.get('email', 'N/A')}", font=("Segoe UI", 14), text_color="#475569").pack(anchor="w", pady=5)
        ctk.CTkLabel(frame_info, text=f"Função: {self.dados.get('cargo', 'N/A')}", font=("Segoe UI", 14), text_color="#475569").pack(anchor="w", pady=5)