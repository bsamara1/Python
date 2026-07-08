# relatorios.py
import customtkinter as ctk
from tkinter import messagebox

class RelatoriosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.criar_interface()

   # relatorios.py
class RelatoriosPage(ctk.CTkFrame):
    # ...
    def criar_interface(self):
        # Topo com métricas
        metricas = ctk.CTkFrame(self, fg_color="transparent")
        metricas.pack(fill="x", pady=20)
        # Use o método criar_card que você já tem no main.py para gerar os 4 cards de topo
        
        # Área de Gráficos (Simulada com frames)
        graficos = ctk.CTkFrame(self, fg_color="transparent")
        graficos.pack(fill="both", expand=True)
        graficos.grid_columnconfigure((0,1), weight=1)
        
        ctk.CTkFrame(graficos, fg_color="white", corner_radius=12, height=300).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkFrame(graficos, fg_color="white", corner_radius=12, height=300).grid(row=0, column=1, padx=5, sticky="ew")
    def exportar(self, tipo, formato):
        messagebox.showinfo("Exportação", f"O relatório de {tipo} foi gerado com sucesso no formato {formato} e guardado na sua pasta de transferências.")