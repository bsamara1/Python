import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from database.database import conectar, registar_novo_estudante, DATABASE

class EstudantesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):
        # =========================================================================
        # 1. TOPO DEDICADO DA PÁGINA (Título, Descrição e Botão alinhados)
        # =========================================================================
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", pady=(20, 10))
        
        # Bloco de Texto (Alinhado à Esquerda)
        titulo_frame = ctk.CTkFrame(topo, fg_color="transparent")
        titulo_frame.pack(side="left", fill="y", anchor="w")
        
        ctk.CTkLabel(
            titulo_frame, 
            text="Estudantes", 
            font=("Segoe UI", 24, "bold"), 
            text_color="#142850"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titulo_frame, 
            text="Gerir todos os estudantes registados.", 
            font=("Segoe UI", 13), 
            text_color="#6B7280"
        ).pack(anchor="w", pady=(2, 0))
        
        # Botão de Ação "+ Adicionar Estudante" (Alinhado à Direita)
        ctk.CTkButton(
            topo, 
            text="+ Adicionar Estudante", 
            fg_color="#1A5CFF", 
            hover_color="#1046CD",
            font=("Segoe UI", 13, "bold"), 
            height=35, 
            corner_radius=8,
            command=self.abrir_formulario
        ).pack(side="right", anchor="center")

        # =========================================================================
        # 2. LINHA DIVISÓRIA BRANCA/CINZA (Separação visual do cabeçalho)
        # =========================================================================
        linha_divisoria = ctk.CTkFrame(self, height=1, fg_color="#E5E7EB")
        linha_divisoria.pack(fill="x", pady=(10, 20))

        # --- SECÇÃO DE FILTROS ---
        filtros = ctk.CTkFrame(self, fg_color="transparent")
        filtros.pack(fill="x", pady=(0, 15))
        
        self.entry_pesquisa = ctk.CTkEntry(
            filtros, 
            placeholder_text="Pesquisar por nome, email ou curso...", 
            height=35, 
            fg_color="white", 
            border_color="#E5E7EB"
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        self.combo_uni = ctk.CTkComboBox(
            filtros, 
            values=["Todos", "UniCV", "JeanPiaget", "UniMindelo", "U.S", "ISCEE"], 
            height=35, 
            fg_color="white", 
            command=lambda e: self.atualizar_tabela()
        )
        self.combo_uni.pack(side="right")

        # --- CONTAINER DA TABELA (Card Branco Arredondado) ---
        self.tabela_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="white", 
            corner_radius=12, 
            border_width=1, 
            border_color="#E5E7EB"
        )
        self.tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

    def atualizar_tabela(self):
        for widget in self.tabela_container.winfo_children():
            widget.destroy()

        colunas = ["ID", "Nome", "Email", "Universidade", "Curso", "Média", "Rendimento", "Ações"]
        for i, col in enumerate(colunas):
            self.tabela_container.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(self.tabela_container, text=col, font=("Segoe UI", 12, "bold"), text_color="#6B7280").grid(row=0, column=i, padx=15, pady=15, sticky="w")

        termo = f"%{self.entry_pesquisa.get()}%"
        uni_selecionada = self.combo_uni.get()

        conn = conectar()
        cursor = conn.cursor()

        query = "SELECT id, nome, email, telefone, universidade, curso, ano, media, rendimento FROM estudantes WHERE (nome LIKE ? OR email LIKE ? OR curso LIKE ?)"
        parametros = [termo, termo, termo]

        if uni_selecionada != "Todos":
            query += " AND universidade = ?"
            parametros.append(uni_selecionada)

        cursor.execute(query, tuple(parametros))
        estudantes = cursor.fetchall()
        conn.close()

        for row_idx, est in enumerate(estudantes, start=1):
            id_est, nome, email, telefone, universidade, curso, ano, media, rendimento = est
            
            ctk.CTkLabel(self.tabela_container, text=str(id_est), font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome, font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=email, font=("Segoe UI", 13), text_color="#4B5563").grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(universidade or ""), font=("Segoe UI", 13)).grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(curso or ""), font=("Segoe UI", 13)).grid(row=row_idx, column=4, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{media:.1f}" if media else "0.0", font=("Segoe UI", 13)).grid(row=row_idx, column=5, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{rendimento:,.0f}$" if rendimento else "0$", font=("Segoe UI", 13)).grid(row=row_idx, column=6, padx=15, pady=10, sticky="w")

            frame_acoes = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
            frame_acoes.grid(row=row_idx, column=7, padx=15, pady=10, sticky="w")

            btn_editar = ctk.CTkButton(
                frame_acoes, text="Editar", width=28, height=28, corner_radius=6,
                fg_color="#EBF0FF", text_color="#1A5CFF", hover_color="#D6E4FF",
                font=("Segoe UI", 12), command=lambda e=est: self.abrir_formulario(e)
            )
            btn_editar.pack(side="left", padx=4)

            btn_eliminar = ctk.CTkButton(
                frame_acoes, text="Eliminar", width=28, height=28, corner_radius=6,
                fg_color="#FFEAEA", text_color="#FF4D4D", hover_color="#FFD1D1",
                font=("Segoe UI", 12), command=lambda id_e=id_est: self.eliminar_estudante(id_e)
            )
            btn_eliminar.pack(side="left", padx=4)

    def abrir_formulario(self, dados_estudante=None):
        janela_form = ctk.CTkToplevel(self)
        janela_form.title("Formulário do Estudante")
        janela_form.geometry("450x650")
        janela_form.grab_set() 

        titulo = "Editar Estudante" if dados_estudante else "Adicionar Estudante"
        ctk.CTkLabel(janela_form, text=titulo, font=("Segoe UI", 18, "bold")).pack(pady=10)

        campos = ["Nome", "Email", "Telefone", "Universidade", "Curso", "Ano", "Média", "Rendimento Familiar"]
        entries = {}

        form_scroll = ctk.CTkScrollableFrame(janela_form, fg_color="transparent", width=400, height=480)
        form_scroll.pack(padx=10, pady=5, fill="both", expand=True)

        for campo in campos:
            ctk.CTkLabel(form_scroll, text=campo, font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=(5, 0))
            entry = ctk.CTkEntry(form_scroll, width=360)
            entry.pack(padx=20, pady=(0, 5))
            entries[campo] = entry

        if not dados_estudante:
            ctk.CTkLabel(form_scroll, text="Senha de Acesso (Nova conta)", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=(5, 0))
            entry_senha = ctk.CTkEntry(form_scroll, width=360, show="*")
            entry_senha.insert(0, "1234")
            entry_senha.pack(padx=20, pady=(0, 5))
            entries["Senha"] = entry_senha

        if dados_estudante:
            entries["Nome"].insert(0, str(dados_estudante[1]))
            entries["Email"].insert(0, str(dados_estudante[2]))
            entries["Telefone"].insert(0, str(dados_estudante[3] or ""))
            entries["Universidade"].insert(0, str(dados_estudante[4] or ""))
            entries["Curso"].insert(0, str(dados_estudante[5] or ""))
            entries["Ano"].insert(0, str(dados_estudante[6] or "1"))
            entries["Média"].insert(0, str(dados_estudante[7] or "0.0"))
            entries["Rendimento Familiar"].insert(0, str(dados_estudante[8] or "0.0"))

        frame_botoes = ctk.CTkFrame(janela_form, fg_color="transparent")
        frame_botoes.pack(pady=15)

        if not dados_estudante:
            ctk.CTkButton(frame_botoes, text="Guardar", fg_color="#1A5CFF", font=("Segoe UI", 13, "bold"), command=lambda: self.salvar_dados(entries, janela_form)).pack(side="left", padx=10)
        else:
            ctk.CTkButton(frame_botoes, text="Atualizar", fg_color="#1A5CFF", font=("Segoe UI", 13, "bold"), command=lambda: self.salvar_dados(entries, janela_form, dados_estudante[0])).pack(side="left", padx=10)
            ctk.CTkButton(frame_botoes, text="Eliminar", fg_color="#EF4444", font=("Segoe UI", 13, "bold"), command=lambda: [self.eliminar_estudante(dados_estudante[0]), janela_form.destroy()]).pack(side="left", padx=10)

    def salvar_dados(self, entries, janela, id_estudante=None):
        nome = entries["Nome"].get()
        email = entries["Email"].get()
        telefone = entries["Telefone"].get()
        universidade = entries["Universidade"].get()
        curso = entries["Curso"].get()
        ano = entries["Ano"].get()
        media = entries["Média"].get()
        rendimento = entries["Rendimento Familiar"].get()

        if not (nome and email and curso):
            messagebox.showwarning("Aviso", "Por favor, preencha pelo menos Nome, Email e Curso!")
            return

        try:
            v_ano = int(ano) if ano else 1
            v_media = float(media) if media else 0.0
            v_rendimento = float(rendimento) if rendimento else 0.0
            
            if id_estudante is None:
                senha = entries["Senha"].get() or "1234"
                sucesso = registar_novo_estudante(
                    nome, email, senha, telefone, universidade, curso, v_ano, v_media, v_rendimento
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Estudante registado com sucesso!")
                else:
                    messagebox.showerror("Erro", "O email já se encontra registado!")
                    return
            else:
                conn = conectar()
                cursor = conn.cursor()
                
                cursor.execute("SELECT email FROM estudantes WHERE id=?", (id_estudante,))
                email_antigo = cursor.fetchone()[0]
                
                cursor.execute("""
                    UPDATE estudantes 
                    SET nome=?, email=?, telefone=?, universidade=?, curso=?, ano=?, media=?, rendimento=? 
                    WHERE id=?
                """, (nome, email, telefone, universidade, curso, v_ano, v_media, v_rendimento, id_estudante))
                
                cursor.execute("""
                    UPDATE utilizadores 
                    SET nome=?, email=? 
                    WHERE email = ?
                """, (nome, email, email_antigo))
                
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

            janela.destroy()
            self.atualizar_tabela()

        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser Inteiro. Média e Rendimento devem ser Decimais (ex: 15.4)!")

    def eliminar_estudante(self, id_estudante):
        if messagebox.askyesno("Confirmar", "Tem a certeza que deseja eliminar este estudante do SIBES?"):
            conn = conectar()
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM estudantes WHERE id=?", (id_estudante,))
            res = cursor.fetchone()
            
            if res:
                email_est = res[0]
                cursor.execute("DELETE FROM estudantes WHERE id=?", (id_estudante,))
                cursor.execute("DELETE FROM utilizadores WHERE email=?", (email_est,))
                
            conn.commit()
            conn.close()
            self.atualizar_tabela()