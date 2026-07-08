# avaliacao.py
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import sys
import os
# avaliacao.py
class AvaliacaoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.criar_interface()

    def criar_interface(self):
        ctk.CTkLabel(self, text="Avaliação Inteligente", font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w", pady=(10, 20))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Esquerda: Formulário
        form = ctk.CTkFrame(container, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(form, text="Selecionar Candidatura", font=("Segoe UI", 16, "bold")).pack(pady=20)
        ctk.CTkComboBox(form, values=["João Silva", "Ana Santos"], width=300, height=40).pack(pady=10)
        ctk.CTkButton(form, text="Avaliar Elegibilidade", fg_color="#1A5CFF", height=40).pack(pady=30)

        # Direita: Resultado
        res = ctk.CTkFrame(container, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        res.grid(row=0, column=1, sticky="nsew")
        
        # Simulação de selo de aprovação
        ctk.CTkLabel(res, text="✔️ Estudante Elegível", text_color="#10B981", font=("Segoe UI", 20, "bold")).pack(pady=40)
        ctk.CTkLabel(res, text="Motivos: Média > 15.0\nRendimento < 50.000$", justify="left").pack()