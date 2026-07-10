# candidaturas.py
import customtkinter as ctk
import os
import sys
import sqlite3
from tkinter import messagebox
from datetime import datetime
import re
from database.database import conectar

class Candidaturas(ctk.CTkFrame):
    """Página de Gestão de Candidaturas com Filtros Avançados e Notificações"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.candidaturas_data = []
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.lista_estudantes = []
        self.lista_bolsas = []

        self.carregar_candidaturas()
        self.carregar_opcoes_filtro()
        self.criar_interface()

    def carregar_candidaturas(self):
        """Carrega todas as candidaturas com informações relacionadas"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
    SELECT 
        c.id, 
        c.estudante_id,
        e.nome AS estudante_nome, 
        c.bolsa_id,
        b.nome AS bolsa_nome, 
        c.estado, 
        c.data_candidatura,
        c.observacoes
    FROM candidaturas c
    INNER JOIN estudantes e ON c.estudante_id = e.id
    INNER JOIN bolsas b ON c.bolsa_id = b.id
""")

            self.candidaturas_data = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar candidaturas: {e}")
            self.candidaturas_data = []

    def carregar_opcoes_filtro(self):
        """Carrega lista de estudantes e bolsas para filtros"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT nome FROM estudantes ORDER BY nome")
            self.lista_estudantes = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT nome FROM bolsas ORDER BY nome")
            self.lista_bolsas = [row[0] for row in cursor.fetchall()]

            conn.close()
        except Exception as e:
            print(f"Erro ao carregar opções de filtro: {e}")

    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.entry_pesquisa.delete(0, "end")
        self.combo_estado.set("Todos")
        self.combo_estudante.set("Todos")
        self.combo_bolsa.set("Todos")
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.atualizar_tabela()

    def aplicar_ordenacao(self, coluna_idx):
        """Alterna ordenação por coluna"""
        colunas_ord = ["id", "estudante", "bolsa", "data", "estado"]
        if coluna_idx >= len(colunas_ord):
            return

        nome_coluna = colunas_ord[coluna_idx]
        if self.coluna_ordenada == nome_coluna:
            self.ordem_ascendente = not self.ordem_ascendente
        else:
            self.coluna_ordenada = nome_coluna
            self.ordem_ascendente = True

        self.atualizar_tabela()

    def criar_interface(self):
        # CABEÇALHO
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(20, 10))

        frame_titulos = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_titulos.pack(side="left", anchor="w")

        ctk.CTkLabel(frame_titulos, text="Candidaturas", font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(frame_titulos, text="Gestão e processamento de candidaturas com notificações.", font=("Segoe UI", 13), text_color="#6B7280").pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(self, height=1, fg_color="#E5E7EB").pack(fill="x", pady=(10, 20))

        # FILTROS - LINHA 1
        filtros1 = ctk.CTkFrame(self, fg_color="transparent")
        filtros1.pack(fill="x", pady=(0, 10))

        self.entry_pesquisa = ctk.CTkEntry(
            filtros1, placeholder_text="🔍 Pesquisar por estudante, bolsa ou ID...", height=38,
            fg_color="white", border_color="#E5E7EB"
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # FILTROS - LINHA 2
        filtros2 = ctk.CTkFrame(self, fg_color="transparent")
        filtros2.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(filtros2, text="Estado:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_estado = ctk.CTkComboBox(
            filtros2, values=["Todos", "Pendente", "Aprovada", "Rejeitada"],
            height=35, fg_color="white", width=130, command=lambda e: self.atualizar_tabela()
        )
        self.combo_estado.pack(side="left", padx=(0, 15))
        self.combo_estado.set("Todos")

        ctk.CTkLabel(filtros2, text="Estudante:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_estudante = ctk.CTkComboBox(
            filtros2, values=["Todos"] + self.lista_estudantes,
            height=35, fg_color="white", width=150, command=lambda e: self.atualizar_tabela()
        )
        self.combo_estudante.pack(side="left", padx=(0, 15))
        self.combo_estudante.set("Todos")

        ctk.CTkLabel(filtros2, text="Bolsa:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_bolsa = ctk.CTkComboBox(
            filtros2, values=["Todos"] + self.lista_bolsas,
            height=35, fg_color="white", width=150, command=lambda e: self.atualizar_tabela()
        )
        self.combo_bolsa.pack(side="left", padx=(0, 15))
        self.combo_bolsa.set("Todos")

        ctk.CTkButton(
            filtros2, text="🔄 Limpar", fg_color="#6B7280", hover_color="#4B5563",
            height=35, width=100, font=("Segoe UI", 11, "bold"),
            command=self.limpar_filtros
        ).pack(side="right")

        # TABELA
        self.tabela_container = ctk.CTkScrollableFrame(
            self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB"
        )
        self.tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.tabela_container.winfo_children():
            widget.destroy()

        # Headers com ordenação
        colunas = ["ID", "Estudante", "Bolsa", "Data", "Estado", "Ações"]
        for i, col in enumerate(colunas):
            self.tabela_container.grid_columnconfigure(i, weight=1)

            texto_col = col
            if self.coluna_ordenada and col != "Ações":
                colunas_ord = ["id", "estudante", "bolsa", "data", "estado"]
                if col.lower() in colunas_ord:
                    if self.coluna_ordenada == col.lower():
                        seta = "🔽" if self.ordem_ascendente else "🔼"
                        texto_col = f"{col} {seta}"

            btn_header = ctk.CTkButton(
                self.tabela_container, text=texto_col, font=("Segoe UI", 12, "bold"),
                fg_color="#F4F6FB", text_color="#6B7280", hover=col != "Ações",
                hover_color="#E5E7EB", height=35, border_width=1, border_color="#E5E7EB",
                command=lambda col_idx=i: self.aplicar_ordenacao(col_idx) if col != "Ações" else None
            )
            btn_header.grid(row=0, column=i, padx=15, pady=15, sticky="ew")

        # Aplicar filtros
        termo = self.entry_pesquisa.get().strip().lower()
        estado_sel = self.combo_estado.get()
        estudante_sel = self.combo_estudante.get()
        bolsa_sel = self.combo_bolsa.get()

        candidaturas_filtradas = []
        for cand in self.candidaturas_data:
            id_c, est_id, nome_est, bolsa_id, nome_bolsa, estado, data, comentarios = cand

            corresponde_termo = termo in str(nome_est).lower() or termo in str(nome_bolsa).lower() or termo in str(id_c).lower()
            corresponde_estado = estado_sel == "Todos" or estado == estado_sel
            corresponde_estudante = estudante_sel == "Todos" or nome_est == estudante_sel
            corresponde_bolsa = bolsa_sel == "Todos" or nome_bolsa == bolsa_sel

            if corresponde_termo and corresponde_estado and corresponde_estudante and corresponde_bolsa:
                candidaturas_filtradas.append(cand)

        # Aplicar ordenação
        if self.coluna_ordenada:
            colunas_ord = ["id", "estudante", "bolsa", "data", "estado"]
            if self.coluna_ordenada in colunas_ord:
                col_idx = colunas_ord.index(self.coluna_ordenada)
                candidaturas_filtradas.sort(key=lambda x: x[col_idx] if x[col_idx] is not None else "", reverse=not self.ordem_ascendente)

        if not candidaturas_filtradas:
            ctk.CTkLabel(
                self.tabela_container, text="Nenhuma candidatura encontrada com os filtros aplicados.",
                font=("Segoe UI", 13), text_color="#9CA3AF"
            ).grid(row=1, column=0, columnspan=6, padx=15, pady=30)
            return

        for row_idx, cand in enumerate(candidaturas_filtradas, start=1):
            id_c, est_id, nome_est, bolsa_id, nome_bolsa, estado, data, comentarios = cand

            ctk.CTkLabel(self.tabela_container, text=str(id_c), font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome_est, font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome_bolsa, font=("Segoe UI", 13)).grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=data or "N/A", font=("Segoe UI", 13)).grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")

            cor_estado = "#10B981" if estado == "Aprovada" else "#EF4444" if estado == "Rejeitada" else "#F59E0B"
            ctk.CTkLabel(self.tabela_container, text=estado, font=("Segoe UI", 13, "bold"), text_color=cor_estado).grid(row=row_idx, column=4, padx=15, pady=10, sticky="w")

            frame_acoes = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
            frame_acoes.grid(row=row_idx, column=5, padx=15, pady=10, sticky="w")

            ctk.CTkButton(
                frame_acoes, text="Editar", width=60, height=28, corner_radius=6,
                fg_color="#EBF0FF", text_color="#1A5CFF", hover_color="#D6E4FF",
                font=("Segoe UI", 11), command=lambda c=cand: self.abrir_editor(c)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                frame_acoes, text="Detalhes", width=60, height=28, corner_radius=6,
                fg_color="#F0F0F0", text_color="#6B7280", hover_color="#E5E7EB",
                font=("Segoe UI", 11), command=lambda c=cand: self.mostrar_detalhes(c)
            ).pack(side="left", padx=4)

    def abrir_editor(self, candidatura):
        """Abre modal para editar candidatura"""
        id_c, est_id, nome_est, bolsa_id, nome_bolsa, estado, data, comentarios = candidatura

        janela = ctk.CTkToplevel(self)
        janela.title("Editar Candidatura")
        janela.geometry("600x500")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(janela, text="✏️ Editar Candidatura", font=("Segoe UI", 20, "bold"), text_color="#142850").pack(pady=(20, 10))
        ctk.CTkLabel(janela, text=f"ID: {id_c} | {nome_est} → {nome_bolsa}", font=("Segoe UI", 11), text_color="#6B7280").pack(pady=(0, 20))

        form_frame = ctk.CTkScrollableFrame(janela, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Estado
        ctk.CTkLabel(form_frame, text="Estado", font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="w", pady=(10, 3))
        combo_estado = ctk.CTkComboBox(form_frame, values=["Pendente", "Aprovada", "Rejeitada"], height=40, fg_color="white", width=500)
        combo_estado.pack(fill="x", pady=(0, 15))
        combo_estado.set(estado)

        # Comentários
        ctk.CTkLabel(form_frame, text="Comentários/Notas", font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="w", pady=(10, 3))
        text_comentarios = ctk.CTkTextbox(form_frame, height=150, fg_color="white", border_width=1, border_color="#E5E7EB")
        text_comentarios.pack(fill="both", expand=True, pady=(0, 20))
        if comentarios:
            text_comentarios.insert("0.0", comentarios)

        # Botões
        btn_frame = ctk.CTkFrame(janela, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=20)

        ctk.CTkButton(
            btn_frame, text="✓ Guardar", fg_color="#10B981", hover_color="#059669",
            font=("Segoe UI", 13, "bold"), height=40,
            command=lambda: self.guardar_edicao(id_c, combo_estado.get(), text_comentarios.get("0.0", "end"), janela)
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            btn_frame, text="✕ Cancelar", fg_color="#6B7280", hover_color="#4B5563",
            font=("Segoe UI", 13, "bold"), height=40, command=janela.destroy
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def mostrar_detalhes(self, candidatura):
        """Mostra detalhes da candidatura"""
        id_c, est_id, nome_est, bolsa_id, nome_bolsa, estado, data, comentarios = candidatura

        janela = ctk.CTkToplevel(self)
        janela.title("Detalhes da Candidatura")
        janela.geometry("500x400")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(janela, text="📋 Detalhes da Candidatura", font=("Segoe UI", 18, "bold"), text_color="#142850").pack(pady=(20, 15))

        info_frame = ctk.CTkFrame(janela, fg_color="transparent")
        info_frame.pack(fill="x", padx=20)

        info = [
            ("ID", str(id_c)),
            ("Estudante", nome_est),
            ("Bolsa", nome_bolsa),
            ("Estado", estado),
            ("Data Candidatura", data or "N/A"),
            ("Comentários", comentarios or "Nenhum comentário")
        ]

        for label, valor in info:
            ctk.CTkLabel(info_frame, text=f"{label}:", font=("Segoe UI", 11, "bold"), text_color="#6B7280").pack(anchor="w", pady=(8, 2))
            ctk.CTkLabel(info_frame, text=valor, font=("Segoe UI", 11), text_color="#111827", wraplength=400, justify="left").pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(janela, text="Fechar", fg_color="#6B7280", hover_color="#4B5563", height=40, command=janela.destroy).pack(pady=15, padx=20, fill="x")

    def guardar_edicao(self, id_cand, novo_estado, novo_comentario, janela):
        """Salva edição com notificação"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE candidaturas
                SET estado = ?, observacoes = ?
                WHERE id = ?
            """, (novo_estado, novo_comentario.strip(), id_cand))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Candidatura atualizada para {novo_estado}!\n\nUma notificação foi enviada ao estudante.")
            janela.destroy()
            self.carregar_candidaturas()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar: {str(e)}")
