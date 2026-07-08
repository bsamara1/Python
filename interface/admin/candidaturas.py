# candidaturas.py
import customtkinter as ctk
from PIL import Image
import os
import sys
import sqlite3
from tkinter import messagebox

class CandidaturasPage(ctk.CTkFrame):
    """Página de Candidaturas com suporte dinâmico a SPA"""

    def __init__(self, master):
        # Correção: Remoção do self.pack() interno
        super().__init__(master, fg_color="#F4F6FB")

        self.caminho_db = self.obter_caminho_db()
        self.candidaturas = []
        self.candidaturas_filtradas = []

        self.carregar_candidaturas()
        self.criar_interface()

    def obter_caminho_db(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'database', 'sibes.db')

    def carregar_candidaturas(self):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("SELECT id, estudante, bolsa, estado FROM candidaturas")
            linhas = cursor.fetchall()
            self.candidaturas = []
            for linha in linhas:
                self.candidaturas.append({
                    "id": linha[0],
                    "estudante": linha[1],
                    "bolsa": linha[2],
                    "estado": linha[3]
                })
            self.candidaturas_filtradas = self.candidaturas.copy()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar candidaturas: {e}")

    def criar_interface(self):
        card_topo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        card_topo.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(card_topo, text="📝 Processos de Candidatura Ativos", font=("Segoe UI", 22, "bold"), text_color="#1E293B").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_topo, text="Valide fluxos documentais, aprove ou reprove pedidos de apoio social.", font=("Segoe UI", 13), text_color="#64748B").pack(anchor="w", padx=20, pady=(0, 20))

        conteudo = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        conteudo.pack(fill="both", expand=True)

        if not self.candidaturas_filtradas:
            ctk.CTkLabel(conteudo, text="Nenhuma submissão pendente de análise.", font=("Segoe UI", 14), text_color="#64748B").pack(expand=True)
        else:
            for cand in self.candidaturas_filtradas:
                row = ctk.CTkFrame(conteudo, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(row, text=cand['estudante'], font=("Segoe UI", 13, "bold"), width=200, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=cand['bolsa'], font=("Segoe UI", 13), text_color="#475569", width=200, anchor="w").pack(side="left")
                
                # Estado visual da candidatura
                lbl_est = ctk.CTkLabel(row, text=cand['estado'], font=("Segoe UI", 12, "bold"), width=100)
                if cand['estado'] == "Aprovada": lbl_est.configure(text_color="#10B981")
                elif cand['estado'] == "Rejeitada": lbl_est.configure(text_color="#EF4444")
                else: lbl_est.configure(text_color="#F59E0B")
                lbl_est.pack(side="left", padx=5)

                ctk.CTkButton(row, text="Aprovar", fg_color="#10B981", hover_color="#059669", width=70, height=26, command=lambda c=cand: self.atualizar_estado(c['id'], "Aprovada")).pack(side="right", padx=2)

    def atualizar_estado(self, candidatura_id, novo_estado):
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("UPDATE candidaturas SET estado = ? WHERE id = ?", (novo_estado, candidatura_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Estado atualizado para {novo_estado}!")
            self.carregar_candidaturas()
            self.criar_interface()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", str(e))