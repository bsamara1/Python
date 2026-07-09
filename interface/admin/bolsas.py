import customtkinter as ctk
import os
import sys
import sqlite3
import re
from tkinter import messagebox

try:
    from database.database import conectar
except ImportError:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(BASE_DIR)
    from database.database import conectar

class BolsasPage(ctk.CTkFrame):
    """Página de Gestão de Bolsas com filtros avançados, ordenação e validação"""

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.bolsas_data = []
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.carregar_bolsas()
        self.criar_interface()

    def carregar_bolsas(self):
        """Carrega todas as bolsas da BD"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, tipo, valor, estado, media_minima, rendimento_maximo FROM bolsas")
            self.bolsas_data = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar bolsas: {e}")
            self.bolsas_data = []

    def criar_interface(self):
        # =========================================================================
        # 1. CABEÇALHO
        # =========================================================================
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(20, 10))

        frame_titulos = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_titulos.pack(side="left", fill="y", anchor="w")

        ctk.CTkLabel(frame_titulos, text="Bolsas", font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(frame_titulos, text="Gerir todas as bolsas e editais registados.", font=("Segoe UI", 13), text_color="#6B7280").pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(
            frame_topo, text="➕ Nova Bolsa", font=("Segoe UI", 13, "bold"),
            fg_color="#1A5CFF", hover_color="#1046CD", height=35, corner_radius=8,
            command=lambda: self.abrir_formulario()
        ).pack(side="right", anchor="center")

        ctk.CTkFrame(self, height=1, fg_color="#E5E7EB").pack(fill="x", pady=(10, 20))

        # =========================================================================
        # 2. FILTROS - LINHA 1
        # =========================================================================
        filtros1 = ctk.CTkFrame(self, fg_color="transparent")
        filtros1.pack(fill="x", pady=(0, 10))

        self.entry_pesquisa = ctk.CTkEntry(
            filtros1, placeholder_text="🔍 Pesquisar por nome ou tipo...", height=38,
            fg_color="white", border_color="#E5E7EB"
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # =========================================================================
        # 3. FILTROS - LINHA 2
        # =========================================================================
        filtros2 = ctk.CTkFrame(self, fg_color="transparent")
        filtros2.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(filtros2, text="Tipo:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_tipo = ctk.CTkComboBox(
            filtros2, values=["Todos", "Mérito", "Social", "Estudo Integral", "Desporto", "Cultural"],
            height=35, fg_color="white", width=150, command=lambda e: self.atualizar_tabela()
        )
        self.combo_tipo.pack(side="left", padx=(0, 15))
        self.combo_tipo.set("Todos")

        ctk.CTkLabel(filtros2, text="Estado:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.combo_estado = ctk.CTkComboBox(
            filtros2, values=["Todos", "Ativo", "Inativo"],
            height=35, fg_color="white", width=120, command=lambda e: self.atualizar_tabela()
        )
        self.combo_estado.pack(side="left", padx=(0, 15))
        self.combo_estado.set("Todos")

        ctk.CTkLabel(filtros2, text="Valor Mín:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 5))
        self.entry_valor_min = ctk.CTkEntry(
            filtros2, placeholder_text="0", height=35, width=80,
            fg_color="white", border_color="#E5E7EB"
        )
        self.entry_valor_min.pack(side="left", padx=(0, 15))
        self.entry_valor_min.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        ctk.CTkButton(
            filtros2, text="🔄 Limpar", fg_color="#6B7280", hover_color="#4B5563",
            height=35, width=100, font=("Segoe UI", 11, "bold"),
            command=self.limpar_filtros
        ).pack(side="right")

        # =========================================================================
        # 4. TABELA
        # =========================================================================
        self.tabela_container = ctk.CTkScrollableFrame(
            self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB"
        )
        self.tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.atualizar_tabela()

    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.entry_pesquisa.delete(0, "end")
        self.combo_tipo.set("Todos")
        self.combo_estado.set("Todos")
        self.entry_valor_min.delete(0, "end")
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.atualizar_tabela()

    def aplicar_ordenacao(self, coluna_idx):
        """Alterna ordenação por coluna"""
        colunas_ord = ["id", "nome", "tipo", "valor", "estado"]
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

        # Headers
        colunas = ["ID", "Nome", "Tipo", "Valor", "Estado", "Ações"]
        for i, col in enumerate(colunas):
            self.tabela_container.grid_columnconfigure(i, weight=1)

            texto_col = col
            if self.coluna_ordenada and col != "Ações":
                colunas_ord = ["id", "nome", "tipo", "valor", "estado"]
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

        # Filtros
        termo = self.entry_pesquisa.get().strip().lower()
        tipo_selecionado = self.combo_tipo.get()
        estado_selecionado = self.combo_estado.get()
        try:
            valor_min = float(self.entry_valor_min.get()) if self.entry_valor_min.get() else 0
        except ValueError:
            valor_min = 0

        bolsas_filtradas = []
        for bolsa in self.bolsas_data:
            id_b, nome, tipo, valor, estado, media_min, rend_max = bolsa

            corresponde_termo = termo in str(nome).lower() or termo in str(tipo).lower()
            corresponde_tipo = tipo_selecionado == "Todos" or tipo == tipo_selecionado
            corresponde_estado = estado_selecionado == "Todos" or estado == estado_selecionado
            corresponde_valor = valor >= valor_min

            if corresponde_termo and corresponde_tipo and corresponde_estado and corresponde_valor:
                bolsas_filtradas.append(bolsa)

        # Ordenação
        if self.coluna_ordenada:
            colunas_ord = ["id", "nome", "tipo", "valor", "estado"]
            if self.coluna_ordenada in colunas_ord:
                col_idx = colunas_ord.index(self.coluna_ordenada)
                bolsas_filtradas.sort(key=lambda x: x[col_idx] if x[col_idx] is not None else "", reverse=not self.ordem_ascendente)

        if not bolsas_filtradas:
            ctk.CTkLabel(
                self.tabela_container, text="Nenhuma bolsa encontrada com os filtros aplicados.",
                font=("Segoe UI", 13), text_color="#9CA3AF"
            ).grid(row=1, column=0, columnspan=6, padx=15, pady=30)
            return

        for row_idx, bolsa in enumerate(bolsas_filtradas, start=1):
            id_b, nome, tipo, valor, estado, media_min, rend_max = bolsa

            ctk.CTkLabel(self.tabela_container, text=str(id_b), font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome, font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(tipo or "N/A"), font=("Segoe UI", 13)).grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{valor:,.0f}$", font=("Segoe UI", 13, "bold")).grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")

            cor_estado = "#10B981" if estado == "Ativo" else "#EF4444"
            ctk.CTkLabel(self.tabela_container, text=estado, font=("Segoe UI", 13, "bold"), text_color=cor_estado).grid(row=row_idx, column=4, padx=15, pady=10, sticky="w")

            frame_acoes = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
            frame_acoes.grid(row=row_idx, column=5, padx=15, pady=10, sticky="w")

            ctk.CTkButton(
                frame_acoes, text="Editar", width=60, height=28, corner_radius=6,
                fg_color="#EBF0FF", text_color="#1A5CFF", hover_color="#D6E4FF",
                font=("Segoe UI", 11), command=lambda b=bolsa: self.abrir_formulario(b)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                frame_acoes, text="Eliminar", width=60, height=28, corner_radius=6,
                fg_color="#FFEAEA", text_color="#FF4D4D", hover_color="#FFD1D1",
                font=("Segoe UI", 11), command=lambda id_b=id_b: self.eliminar_bolsa(id_b)
            ).pack(side="left", padx=4)

    def abrir_formulario(self, dados_bolsa=None):
        janela_form = ctk.CTkToplevel(self)
        janela_form.title("Formulário de Bolsa")
        janela_form.geometry("600x900")
        janela_form.grab_set()
        janela_form.resizable(False, False)

        titulo = "✏️ Editar Bolsa" if dados_bolsa else "➕ Adicionar Nova Bolsa"
        ctk.CTkLabel(janela_form, text=titulo, font=("Segoe UI", 22, "bold"), text_color="#142850").pack(pady=(20, 5))

        if dados_bolsa:
            ctk.CTkLabel(janela_form, text=f"ID: {dados_bolsa[0]}", font=("Segoe UI", 11), text_color="#6B7280").pack(pady=(0, 20))

        form_scroll = ctk.CTkScrollableFrame(janela_form, fg_color="transparent", width=550, height=700)
        form_scroll.pack(padx=20, pady=5, fill="both", expand=True)

        campos_info = [
            ("Nome da Bolsa", "Ex: Bolsa de Mérito", "text"),
            ("Tipo", "Mérito, Social, Estudo Integral, Desporto, Cultural", "text"),
            ("Valor do Benefício", "Em CVE", "decimal"),
            ("Média Mínima", "0.0-20.0", "decimal"),
            ("Rendimento Máximo", "Em CVE (0 = sem limite)", "decimal"),
            ("Estado", "Ativo ou Inativo", "combo"),
        ]

        entries = {}
        label_erros = {}

        for campo, placeholder, tipo in campos_info:
            ctk.CTkLabel(form_scroll, text=campo, font=("Segoe UI", 12, "bold"), text_color="#142850").pack(anchor="w", padx=15, pady=(12, 3))

            if tipo == "combo":
                combo = ctk.CTkComboBox(
                    form_scroll, values=["Ativo", "Inativo"],
                    height=40, fg_color="white", width=500
                )
                combo.pack(padx=15, pady=(0, 2))
                entries[campo] = combo
                if dados_bolsa:
                    combo.set(dados_bolsa[4])
                else:
                    combo.set("Ativo")
            else:
                entry = ctk.CTkEntry(
                    form_scroll, width=500, height=40,
                    placeholder_text=placeholder, border_width=1, border_color="#E5E7EB"
                )
                entry.pack(padx=15, pady=(0, 2))
                entries[campo] = entry

                if tipo == "decimal":
                    entry.bind("<KeyRelease>", lambda e, c=campo: self.validar_campo_decimal(e, entry, label_erros.get(c)))

            label_erro = ctk.CTkLabel(form_scroll, text="", font=("Segoe UI", 10), text_color="#EF4444")
            label_erro.pack(anchor="w", padx=15, pady=(0, 0))
            label_erros[campo] = label_erro

        # Preencher dados
        if dados_bolsa:
            entries["Nome da Bolsa"].insert(0, dados_bolsa[1])
            entries["Tipo"].insert(0, dados_bolsa[2] or "")
            entries["Valor do Benefício"].insert(0, str(f"{dados_bolsa[3]:.0f}" if dados_bolsa[3] else "0"))
            entries["Média Mínima"].insert(0, str(f"{dados_bolsa[5]:.1f}" if dados_bolsa[5] else "0.0"))
            entries["Rendimento Máximo"].insert(0, str(f"{dados_bolsa[6]:.0f}" if dados_bolsa[6] else "0"))

        # Botões
        frame_botoes = ctk.CTkFrame(janela_form, fg_color="transparent")
        frame_botoes.pack(pady=20, fill="x", padx=20)

        if not dados_bolsa:
            ctk.CTkButton(
                frame_botoes, text="✓ Guardar", fg_color="#10B981", hover_color="#059669",
                font=("Segoe UI", 13, "bold"), height=40,
                command=lambda: self.salvar_bolsa(entries, janela_form)
            ).pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(
                frame_botoes, text="✕ Cancelar", fg_color="#6B7280", hover_color="#4B5563",
                font=("Segoe UI", 13, "bold"), height=40, command=janela_form.destroy
            ).pack(side="left", fill="x", expand=True, padx=(5, 0))
        else:
            ctk.CTkButton(
                frame_botoes, text="✓ Atualizar", fg_color="#10B981", hover_color="#059669",
                font=("Segoe UI", 13, "bold"), height=40,
                command=lambda: self.salvar_bolsa(entries, janela_form, dados_bolsa[0])
            ).pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(
                frame_botoes, text="🗑️ Eliminar", fg_color="#EF4444", hover_color="#DC2626",
                font=("Segoe UI", 13, "bold"), height=40,
                command=lambda: self.eliminar_bolsa(dados_bolsa[0], janela_form)
            ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def validar_campo_decimal(self, event, entry, label_erro):
        """Valida decimais em tempo real"""
        valor = entry.get().strip()
        if not valor:
            if label_erro:
                label_erro.configure(text="")
            entry.configure(border_color="#E5E7EB", border_width=1)
            return

        try:
            v = float(valor)
            if v >= 0:
                if label_erro:
                    label_erro.configure(text="✓ Válido", text_color="#10B981")
                entry.configure(border_color="#10B981", border_width=2)
            else:
                if label_erro:
                    label_erro.configure(text="✗ Não pode ser negativo", text_color="#EF4444")
                entry.configure(border_color="#EF4444", border_width=2)
        except ValueError:
            if label_erro:
                label_erro.configure(text="✗ Deve ser um número decimal", text_color="#EF4444")
            entry.configure(border_color="#EF4444", border_width=2)

    def salvar_bolsa(self, entries, janela, id_bolsa=None):
        nome = entries["Nome da Bolsa"].get().strip()
        tipo = entries["Tipo"].get().strip()
        valor_str = entries["Valor do Benefício"].get().strip()
        media_min_str = entries["Média Mínima"].get().strip()
        rend_max_str = entries["Rendimento Máximo"].get().strip()
        estado = entries["Estado"].get()

        erros = []

        if not nome:
            erros.append("✗ Nome é obrigatório")
        elif len(nome) < 3:
            erros.append("✗ Nome deve ter mínimo 3 caracteres")

        if not tipo:
            erros.append("✗ Tipo é obrigatório")

        try:
            valor = float(valor_str) if valor_str else 0
            if valor < 0:
                erros.append("✗ Valor não pode ser negativo")
        except ValueError:
            erros.append("✗ Valor deve ser um número decimal")

        try:
            media_min = float(media_min_str) if media_min_str else 0
            if media_min < 0 or media_min > 20:
                erros.append("✗ Média mínima deve estar entre 0 e 20")
        except ValueError:
            erros.append("✗ Média mínima deve ser um número decimal")

        try:
            rend_max = float(rend_max_str) if rend_max_str else 0
            if rend_max < 0:
                erros.append("✗ Rendimento máximo não pode ser negativo")
        except ValueError:
            erros.append("✗ Rendimento máximo deve ser um número decimal")

        if erros:
            messagebox.showerror("Validação Falhou", "\n".join(erros))
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            if id_bolsa is None:
                cursor.execute("""
                    INSERT INTO bolsas (nome, tipo, valor, media_minima, rendimento_maximo, estado)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nome, tipo, valor, media_min, rend_max, estado))
                messagebox.showinfo("Sucesso", f"Bolsa '{nome}' criada com sucesso!")
            else:
                cursor.execute("""
                    UPDATE bolsas
                    SET nome=?, tipo=?, valor=?, media_minima=?, rendimento_maximo=?, estado=?
                    WHERE id=?
                """, (nome, tipo, valor, media_min, rend_max, estado, id_bolsa))
                messagebox.showinfo("Sucesso", f"Bolsa '{nome}' atualizada com sucesso!")

            conn.commit()
            conn.close()

            janela.destroy()
            self.carregar_bolsas()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar bolsa:\n{str(e)}")

    def eliminar_bolsa(self, id_bolsa, janela_form=None):
        if messagebox.askyesno("Confirmar Eliminação", "Tem a certeza que deseja eliminar esta bolsa?\n\nEsta ação não pode ser desfeita!"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bolsas WHERE id=?", (id_bolsa,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Bolsa eliminada com sucesso!")
                if janela_form:
                    janela_form.destroy()
                self.carregar_bolsas()
                self.atualizar_tabela()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao eliminar bolsa:\n{str(e)}")