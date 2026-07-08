# utilizadores.py
import customtkinter as ctk
from tkinter import messagebox

class UtilizadoresPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.criar_interface()

    def criar_interface(self):
        card_topo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        card_topo.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(card_topo, text="👥 Controlo de Utilizadores e Permissões", font=("Segoe UI", 22, "bold"), text_color="#1E293B").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_topo, text="Filtre e configure quem tem autorização para auditar, avaliar e submeter candidaturas.", font=("Segoe UI", 13), text_color="#64748B").pack(anchor="w", padx=20, pady=(0, 20))

        # Tabela / Lista fictícia de Utilizadores
        conteudo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        conteudo.pack(fill="both", expand=True)

        headers = ctk.CTkFrame(conteudo, fg_color="#F1F5F9")
        headers.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(headers, text="Nome Completo", font=("Segoe UI", 12, "bold"), width=200, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(headers, text="Função / Cargo", font=("Segoe UI", 12, "bold"), width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(headers, text="Estado", font=("Segoe UI", 12, "bold"), width=100, anchor="w").pack(side="left", padx=10)

        # Exemplo de Utilizador Cadastrado
        row = ctk.CTkFrame(conteudo, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(row, text="Dr. António Silva", font=("Segoe UI", 13), width=200, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(row, text="Presidente do Júri", font=("Segoe UI", 13), text_color="#2563EB", width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(row, text="Ativo", font=("Segoe UI", 13), text_color="#10B981", width=100, anchor="w").pack(side="left", padx=10)
        ctk.CTkButton(row, text="Revogar Acesso", fg_color="#334155", width=100, height=28, command=self.revogar).pack(side="right", padx=10)

    def revogar(self):
        messagebox.showwarning("Permissões", "A alteração de acessos de cargos estruturais requer dupla verificação de segurança.")