import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import os
import sys
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from database.database import conectar, registar_novo_estudante, DATABASE

class EstudantesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.estudantes_data = []
        self.coluna_ordenada = None
        self.ordem_ascendente = True
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

        # --- SECÇÃO DE FILTROS - LINHA 1 ---
        filtros1 = ctk.CTkFrame(self, fg_color="transparent")
        filtros1.pack(fill="x", pady=(0, 10))

        self.entry_pesquisa = ctk.CTkEntry(
            filtros1,
            placeholder_text="🔍 Pesquisar por nome, email ou curso...",
            height=38,
            fg_color="white",
            border_color="#E5E7EB"
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # --- SECÇÃO DE FILTROS - LINHA 2 ---
        filtros2 = ctk.CTkFrame(self, fg_color="transparent")
        filtros2.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(filtros2, text="Universidade:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_uni = ctk.CTkComboBox(
            filtros2,
            values=["Todos", "UniCV", "JeanPiaget", "UniMindelo", "U.S", "ISCEE"],
            height=35,
            fg_color="white",
            width=140,
            command=lambda e: self.atualizar_tabela()
        )
        self.combo_uni.pack(side="left", padx=(0, 15))
        self.combo_uni.set("Todos")

        ctk.CTkLabel(filtros2, text="Ano:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_ano = ctk.CTkComboBox(
            filtros2,
            values=["Todos", "1", "2", "3", "4", "5"],
            height=35,
            fg_color="white",
            width=100,
            command=lambda e: self.atualizar_tabela()
        )
        self.combo_ano.pack(side="left", padx=(0, 15))
        self.combo_ano.set("Todos")

        ctk.CTkLabel(filtros2, text="Média Min:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.entry_media_min = ctk.CTkEntry(
            filtros2,
            placeholder_text="0.0",
            height=35,
            width=80,
            fg_color="white",
            border_color="#E5E7EB"
        )
        self.entry_media_min.pack(side="left", padx=(0, 15))
        self.entry_media_min.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        ctk.CTkButton(
            filtros2,
            text="🔄 Limpar Filtros",
            fg_color="#6B7280",
            hover_color="#4B5563",
            height=35,
            width=120,
            font=("Segoe UI", 11, "bold"),
            command=self.limpar_filtros
        ).pack(side="right")

        # --- CONTAINER DA TABELA (Card Branco Arredondado) ---
        self.tabela_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="white", 
            corner_radius=12, 
            border_width=1, 
            border_color="#E5E7EB"
        )
        self.tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.entry_pesquisa.delete(0, "end")
        self.combo_uni.set("Todos")
        self.combo_ano.set("Todos")
        self.entry_media_min.delete(0, "end")
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.atualizar_tabela()

    def aplicar_ordenacao(self, coluna_idx):
        """Alterna ordenação por coluna"""
        colunas_ord = ["id", "nome", "email", "universidade", "curso", "ano", "media", "rendimento"]
        if coluna_idx >= len(colunas_ord):
            return

        nome_coluna = colunas_ord[coluna_idx]

        if self.coluna_ordenada == nome_coluna:
            self.ordem_ascendente = not self.ordem_ascendente
        else:
            self.coluna_ordenada = nome_coluna
            self.ordem_ascendente = True

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.tabela_container.winfo_children():
            widget.destroy()

        colunas = ["ID", "Nome", "Email", "Universidade", "Curso", "Ano", "Média", "Rendimento", "Ações"]
        for i, col in enumerate(colunas):
            if col == "Ações":
                # Força a coluna das Ações a guardar espaço suficiente para os botões sem os esmagar
                self.tabela_container.grid_columnconfigure(i, weight=0, minsize=180)
            else:
                self.tabela_container.grid_columnconfigure(i, weight=1, minsize=80)

            texto_col = col
            if self.coluna_ordenada:
                colunas_ord = ["id", "nome", "email", "universidade", "curso", "ano", "media", "rendimento"]
                if col != "Ações" and col.lower() in colunas_ord:
                    idx = colunas_ord.index(col.lower())
                    if self.coluna_ordenada == col.lower():
                        seta = "🔽" if self.ordem_ascendente else "🔼"
                        texto_col = f"{col} {seta}"

            btn_header = ctk.CTkButton(
                self.tabela_container,
                text=texto_col,
                font=("Segoe UI", 12, "bold"),
                fg_color="#F4F6FB",
                text_color="#6B7280",
                hover=col != "Ações",
                hover_color="#E5E7EB",
                height=35,
                border_width=1,
                border_color="#E5E7EB",
                command=lambda col_idx=i: self.aplicar_ordenacao(col_idx) if col != "Ações" else None
            )
            # Reduzido padx para 5 para poupar espaço horizontal geral
            btn_header.grid(row=0, column=i, padx=5, pady=15, sticky="ew")

        termo = self.entry_pesquisa.get().strip()
        uni_selecionada = self.combo_uni.get()
        ano_selecionado = self.combo_ano.get()
        try:
            media_min = float(self.entry_media_min.get()) if self.entry_media_min.get() else 0.0
        except ValueError:
            media_min = 0.0

        conn = conectar()
        cursor = conn.cursor()

        query = "SELECT id, nome, email, telefone, universidade, curso, ano, media, rendimento FROM estudantes WHERE 1=1"
        parametros = []

        if termo:
            query += " AND (nome LIKE ? OR email LIKE ? OR curso LIKE ?)"
            parametros.extend([f"%{termo}%", f"%{termo}%", f"%{termo}%"])

        if uni_selecionada != "Todos":
            query += " AND universidade = ?"
            parametros.append(uni_selecionada)

        if ano_selecionado != "Todos":
            query += " AND ano = ?"
            parametros.append(int(ano_selecionado))

        if media_min > 0:
            query += " AND media >= ?"
            parametros.append(media_min)

        cursor.execute(query, parametros)
        self.estudantes_data = cursor.fetchall()
        conn.close()

        if self.coluna_ordenada:
            colunas_ord = ["id", "nome", "email", "universidade", "curso", "ano", "media", "rendimento"]
            col_idx = colunas_ord.index(self.coluna_ordenada)
            self.estudantes_data.sort(key=lambda x: x[col_idx] if x[col_idx] is not None else "", reverse=not self.ordem_ascendente)

        if not self.estudantes_data:
            ctk.CTkLabel(
                self.tabela_container,
                text="Nenhum estudante encontrado com os filtros aplicados.",
                font=("Segoe UI", 13),
                text_color="#9CA3AF"
            ).grid(row=1, column=0, columnspan=9, padx=15, pady=30)
            return

        for row_idx, est in enumerate(self.estudantes_data, start=1):
            id_est, nome, email, telefone, universidade, curso, ano, media, rendimento = est

            # Reduzido padx para 6 píxeis para que as colunas fiquem perfeitamente organizadas
            ctk.CTkLabel(self.tabela_container, text=str(id_est), font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome, font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=email, font=("Segoe UI", 13), text_color="#4B5563").grid(row=row_idx, column=2, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(universidade or "N/A"), font=("Segoe UI", 13)).grid(row=row_idx, column=3, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(curso or "N/A"), font=("Segoe UI", 13)).grid(row=row_idx, column=4, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(ano or 1), font=("Segoe UI", 13)).grid(row=row_idx, column=5, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{media:.1f}" if media else "0.0", font=("Segoe UI", 13)).grid(row=row_idx, column=6, padx=6, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{rendimento:,.0f}$" if rendimento else "0$", font=("Segoe UI", 13)).grid(row=row_idx, column=7, padx=6, pady=10, sticky="w")

            frame_acoes = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
            # ERRO CORRIGIDO: Removido sticky="center" que quebrava o Tkinter
            frame_acoes.grid(row=row_idx, column=8, padx=5, pady=10)

            btn_editar = ctk.CTkButton(
                frame_acoes, text="Editar", width=75, height=28, corner_radius=6,
                fg_color="#EBF0FF", text_color="#1A5CFF", hover_color="#D6E4FF",
                font=("Segoe UI", 11), command=lambda e=est: self.abrir_formulario(e)
            )
            btn_editar.pack(side="left", padx=3)

            btn_eliminar = ctk.CTkButton(
                frame_acoes, text="Eliminar", width=75, height=28, corner_radius=6,
                fg_color="#FFEAEA", text_color="#FF4D4D", hover_color="#FFD1D1",
                font=("Segoe UI", 11), command=lambda id_e=id_est: self.eliminar_estudante(id_e)
            )
            btn_eliminar.pack(side="left", padx=3)

    def abrir_formulario(self, dados_estudante=None):
        janela_form = ctk.CTkToplevel(self)
        janela_form.title("Formulário do Estudante")
        janela_form.geometry("550x850")
        janela_form.grab_set()
        janela_form.resizable(False, False)

        titulo = "✏️ Editar Estudante" if dados_estudante else "➕ Adicionar Novo Estudante"
        ctk.CTkLabel(janela_form, text=titulo, font=("Segoe UI", 22, "bold"), text_color="#142850").pack(pady=(20, 5))

        if dados_estudante:
            ctk.CTkLabel(janela_form, text=f"ID: {dados_estudante[0]}", font=("Segoe UI", 11), text_color="#6B7280").pack(pady=(0, 20))
        else:
            ctk.CTkLabel(janela_form, text="Preencha os campos para criar um novo estudante", font=("Segoe UI", 12), text_color="#6B7280").pack(pady=(0, 20))

        # Scrollable frame para os campos
        form_scroll = ctk.CTkScrollableFrame(janela_form, fg_color="transparent", width=500, height=600)
        form_scroll.pack(padx=20, pady=5, fill="both", expand=True)

        campos_info = [
            ("Nome", "Digite o nome completo", None, "text"),
            ("Email", "exemplo@email.com", None, "email"),
            ("Telefone", "(+238) 123 45 67", None, "tel"),
            ("Universidade", "UniCV, JeanPiaget, UniMindelo, U.S, ISCEE", None, "text"),
            ("Curso", "Ex: Engenharia, Direito, etc", None, "text"),
            ("Ano", "1-6", None, "number"),
            ("Média", "0.0-20.0", None, "decimal"),
            ("Rendimento Familiar", "Em CVE", None, "decimal"),
        ]

        entries = {}
        label_erros = {}

        for campo, placeholder, _, tipo in campos_info:
            ctk.CTkLabel(form_scroll, text=campo, font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="w", padx=15, pady=(12, 3))

            entry = ctk.CTkEntry(
                form_scroll,
                width=450,
                height=40,
                placeholder_text=placeholder,
                border_width=1,
                border_color="#E5E7EB"
            )
            entry.pack(padx=15, pady=(0, 2))
            entries[campo] = entry

            label_erro = ctk.CTkLabel(form_scroll, text="", font=("Segoe UI", 10), text_color="#EF4444")
            label_erro.pack(anchor="w", padx=15, pady=(0, 0))
            label_erros[campo] = label_erro

            if tipo == "email":
                entry.bind("<KeyRelease>", lambda e, c=campo: self.validar_campo_email(e, entries[c], label_erros[c]))
            elif tipo == "number":
                entry.bind("<KeyRelease>", lambda e, c=campo: self.validar_campo_numero(e, entries[c], label_erros[c], 1, 6))
            elif tipo == "decimal":
                entry.bind("<KeyRelease>", lambda e, c=campo, n=campo: self.validar_campo_decimal(e, entries[c], label_erros[c], c))

        if not dados_estudante:
            ctk.CTkLabel(form_scroll, text="Senha de Acesso", font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="w", padx=15, pady=(12, 3))
            entry_senha = ctk.CTkEntry(
                form_scroll,
                width=450,
                height=40,
                placeholder_text="Deixe em branco para usar padrão (1234)",
                show="*",
                border_width=1,
                border_color="#E5E7EB"
            )
            entry_senha.pack(padx=15, pady=(0, 2))
            entries["Senha"] = entry_senha

            label_erro_senha = ctk.CTkLabel(form_scroll, text="", font=("Segoe UI", 10), text_color="#6B7280")
            label_erro_senha.pack(anchor="w", padx=15, pady=(0, 15))
            label_erros["Senha"] = label_erro_senha

        if dados_estudante:
            entries["Nome"].insert(0, str(dados_estudante[1]))
            entries["Email"].insert(0, str(dados_estudante[2]))
            entries["Telefone"].insert(0, str(dados_estudante[3] or ""))
            entries["Universidade"].insert(0, str(dados_estudante[4] or ""))
            entries["Curso"].insert(0, str(dados_estudante[5] or ""))
            entries["Ano"].insert(0, str(dados_estudante[6] or "1"))
            entries["Média"].insert(0, str(f"{dados_estudante[7]:.1f}" if dados_estudante[7] else "0.0"))
            entries["Rendimento Familiar"].insert(0, str(f"{dados_estudante[8]:.0f}" if dados_estudante[8] else "0"))

        frame_botoes = ctk.CTkFrame(janela_form, fg_color="transparent")
        frame_botoes.pack(pady=20, fill="x", padx=20)

        if not dados_estudante:
            ctk.CTkButton(
                frame_botoes,
                text="✓ Guardar",
                fg_color="#10B981",
                hover_color="#059669",
                font=("Segoe UI", 13, "bold"),
                height=40,
                command=lambda: self.salvar_dados(entries, janela_form)
            ).pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(
                frame_botoes,
                text="✕ Cancelar",
                fg_color="#6B7280",
                hover_color="#4B5563",
                font=("Segoe UI", 13, "bold"),
                height=40,
                command=janela_form.destroy
            ).pack(side="left", fill="x", expand=True, padx=(5, 0))
        else:
            ctk.CTkButton(
                frame_botoes,
                text="✓ Atualizar",
                fg_color="#10B981",
                hover_color="#059669",
                font=("Segoe UI", 13, "bold"),
                height=40,
                command=lambda: self.salvar_dados(entries, janela_form, dados_estudante[0])
            ).pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(
                frame_botoes,
                text="🗑️ Eliminar",
                fg_color="#EF4444",
                hover_color="#DC2626",
                font=("Segoe UI", 13, "bold"),
                height=40,
                command=lambda: self.eliminar_com_confirmacao(dados_estudante[0], janela_form)
            ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def validar_campo_email(self, event, entry, label_erro):
        email = entry.get().strip()
        if not email:
            label_erro.configure(text="")
            entry.configure(border_color="#E5E7EB", border_width=1)
            return

        if self.validar_email(email):
            label_erro.configure(text="✓ Email válido", text_color="#10B981")
            entry.configure(border_color="#10B981", border_width=2)
        else:
            label_erro.configure(text="✗ Email inválido", text_color="#EF4444")
            entry.configure(border_color="#EF4444", border_width=2)

    def validar_campo_numero(self, event, entry, label_erro, min_val, max_val):
        valor = entry.get().strip()
        if not valor:
            label_erro.configure(text="")
            entry.configure(border_color="#E5E7EB", border_width=1)
            return

        try:
            v = int(valor)
            if min_val <= v <= max_val:
                label_erro.configure(text=f"✓ {min_val}-{max_val}", text_color="#10B981")
                entry.configure(border_color="#10B981", border_width=2)
            else:
                label_erro.configure(text=f"✗ Deve estar entre {min_val} e {max_val}", text_color="#EF4444")
                entry.configure(border_color="#EF4444", border_width=2)
        except ValueError:
            label_erro.configure(text="✗ Deve ser um número inteiro", text_color="#EF4444")
            entry.configure(border_color="#EF4444", border_width=2)

    def validar_campo_decimal(self, event, entry, label_erro, campo_nome):
        valor = entry.get().strip()
        if not valor:
            label_erro.configure(text="")
            entry.configure(border_color="#E5E7EB", border_width=1)
            return

        try:
            v = float(valor)
            if campo_nome == "Média":
                if 0 <= v <= 20:
                    label_erro.configure(text="✓ 0-20", text_color="#10B981")
                    entry.configure(border_color="#10B981", border_width=2)
                else:
                    label_erro.configure(text="✗ 0-20", text_color="#EF4444")
                    entry.configure(border_color="#EF4444", border_width=2)
            else:
                if v >= 0:
                    label_erro.configure(text="✓ Válido", text_color="#10B981")
                    entry.configure(border_color="#10B981", border_width=2)
                else:
                    label_erro.configure(text="✗ Não pode ser negativo", text_color="#EF4444")
                    entry.configure(border_color="#EF4444", border_width=2)
        except ValueError:
            label_erro.configure(text="✗ Deve ser um número decimal", text_color="#EF4444")
            entry.configure(border_color="#EF4444", border_width=2)

    def eliminar_com_confirmacao(self, id_estudante, janela_form):
        if messagebox.askyesno("Confirmar Eliminação", "Tem a certeza que deseja eliminar este estudante?\n\nEsta ação não pode ser desfeita!"):
            self.eliminar_estudante(id_estudante)
            janela_form.destroy()

    def validar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    def salvar_dados(self, entries, janela, id_estudante=None):
        nome = entries["Nome"].get().strip()
        email = entries["Email"].get().strip()
        telefone = entries["Telefone"].get().strip()
        universidade = entries["Universidade"].get().strip()
        curso = entries["Curso"].get().strip()
        ano = entries["Ano"].get().strip()
        media = entries["Média"].get().strip()
        rendimento = entries["Rendimento Familiar"].get().strip()

        erros = []

        if not nome:
            erros.append("✗ Nome é obrigatório")
        elif len(nome) < 3:
            erros.append("✗ Nome deve ter mínimo 3 caracteres")

        if not email:
            erros.append("✗ Email é obrigatório")
        elif not self.validar_email(email):
            erros.append("✗ Email inválido (ex: user@example.com)")

        if not curso:
            erros.append("✗ Curso é obrigatório")

        if ano:
            try:
                v_ano = int(ano)
                if v_ano < 1 or v_ano > 6:
                    erros.append("✗ Ano deve estar entre 1 e 6")
            except ValueError:
                erros.append("✗ Ano deve ser um número inteiro")
        else:
            v_ano = 1

        if media:
            try:
                v_media = float(media)
                if v_media < 0 or v_media > 20:
                    erros.append("✗ Média deve estar entre 0 e 20")
            except ValueError:
                erros.append("✗ Média deve ser um número decimal (ex: 15.5)")
        else:
            v_media = 0.0

        if rendimento:
            try:
                v_rendimento = float(rendimento)
                if v_rendimento < 0:
                    erros.append("✗ Rendimento não pode ser negativo")
            except ValueError:
                erros.append("✗ Rendimento deve ser um número decimal")
        else:
            v_rendimento = 0.0

        if erros:
            mensagem_erros = "\n".join(erros)
            messagebox.showerror("Validação Falhou", f"Por favor, corrija os seguintes erros:\n\n{mensagem_erros}")
            return

        try:
            if id_estudante is None:
                senha = entries.get("Senha").get() if "Senha" in entries else "1234"
                sucesso = registar_novo_estudante(
                    nome, email, senha, telefone, universidade, curso, v_ano, v_media, v_rendimento
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Estudante '{nome}' registado com sucesso!")
                else:
                    messagebox.showerror("Erro", "O email já se encontra registado no sistema!")
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
                messagebox.showinfo("Sucesso", f"Dados de '{nome}' atualizados com sucesso!")

            janela.destroy()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar dados:\n{str(e)}")

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