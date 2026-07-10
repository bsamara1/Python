import customtkinter as ctk
import os
import sys
import sqlite3
import re
from tkinter import messagebox

# =========================================================================
# RESOLUÇÃO DINÂMICA DE PATHS PARA O MÓDULO DATABASE
# =========================================================================
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Sobe até encontrar a raiz onde reside a pasta 'database'
# Testa subir 1 nível, 2 níveis e 3 níveis consecutivamente
possiveis_raizes = [
    os.path.abspath(os.path.join(diretorio_atual, "..")),
    os.path.abspath(os.path.join(diretorio_atual, "..", "..")),
    os.path.abspath(os.path.join(diretorio_atual, "..", "..", "..")),
    diretorio_atual
]

conectado = False
for raiz in possiveis_raizes:
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    try:
        from database.database import conectar
        conectado = True
        break
    except (ImportError, ModuleNotFoundError):
        continue

if not conectado:
    # Fallback caso a estrutura esteja fora dos padrões testados
    try:
        from database import conectar
    except (ImportError, ModuleNotFoundError):
        def conectar():
            # Cria uma ligação direta local se o módulo não for descoberto de todo
            caminho_local_db = os.path.join(diretorio_atual, "database", "sibes.db")
            if not os.path.exists(os.path.dirname(caminho_local_db)):
                caminho_local_db = os.path.join(os.path.dirname(diretorio_atual), "database", "sibes.db")
            return sqlite3.connect(caminho_local_db)

# =========================================================================
# CLASSE PRINCIPAL
# =========================================================================
class BolsasPage(ctk.CTkFrame):
    """Página de Visualização/Gestão de Bolsas adaptada dinamicamente ao tipo de utilizador"""
    # (O restante código da classe permanece idêntico)
    def __init__(self, master, role="estudante"):  # Adicionado o parâmetro 'role'
        super().__init__(master, fg_color="#F4F6FB")
        self.role = role.lower()
        self.bolsas_data = []
        self.coluna_ordenada = None
        self.ordem_ascendente = True
        self.carregar_bolsas()
        self.criar_interface()

    def carregar_bolsas(self):
        """Carrega as bolsas da BD (Apenas 'Ativo' se for estudante)"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Se for estudante, filtra apenas pelas bolsas Ativas diretamente na Query
            if self.role == "estudante":
                cursor.execute("SELECT id, nome, tipo, valor, estado, media_minima, rendimento_maximo FROM bolsas WHERE estado = 'Ativo'")
            else:
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

        # Texto adaptado ao Estudante
        titulo_texto = "Bolsas Disponíveis" if self.role == "estudante" else "Bolsas"
        subtitulo_texto = "Consulte as bolsas e editais de candidatura abertos." if self.role == "estudante" else "Gerir todas as bolsas e editais registados."

        ctk.CTkLabel(frame_titulos, text=titulo_texto, font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(frame_titulos, text=subtitulo_texto, font=("Segoe UI", 13), text_color="#6B7280").pack(anchor="w", pady=(2, 0))

        # Botão "Nova Bolsa" visível APENAS para Admin
        if self.role != "estudante":
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

        # Filtro de Estado visível APENAS para Admin (Estudante só vê bolsas Ativas)
        if self.role != "estudante":
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
        if self.role != "estudante":
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

        # Headers dinâmicos com base no role (Estudante não precisa da coluna 'Estado' nem 'Ações' administrativas)
        if self.role == "estudante":
            colunas = ["ID", "Nome", "Tipo", "Valor", "Média Mín.", "Ações"]
        else:
            colunas = ["ID", "Nome", "Tipo", "Valor", "Estado", "Ações"]

        for i, col in enumerate(colunas):
            self.tabela_container.grid_columnconfigure(i, weight=1)

            texto_col = col
            if self.coluna_ordenada and col != "Ações":
                colunas_ord = ["id", "nome", "tipo", "valor", "estado" if self.role != "estudante" else "media_minima"]
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

        # Filtros internos
        termo = self.entry_pesquisa.get().strip().lower()
        tipo_selecionado = self.combo_tipo.get()
        estado_selecionado = "Ativo" if self.role == "estudante" else self.combo_estado.get()
        
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
            colunas_ord = ["id", "nome", "tipo", "valor", "estado" if self.role != "estudante" else "media_minima"]
            if self.coluna_ordenada in colunas_ord:
                col_idx = colunas_ord.index(self.coluna_ordenada)
                bolsas_filtradas.sort(key=lambda x: x[col_idx] if x[col_idx] is not None else "", reverse=not self.ordem_ascendente)

        if not bolsas_filtradas:
            ctk.CTkLabel(
                self.tabela_container, text="Nenhuma bolsa encontrada com os filtros aplicados.",
                font=("Segoe UI", 13), text_color="#9CA3AF"
            ).grid(row=1, column=0, columnspan=len(colunas), padx=15, pady=30)
            return

        for row_idx, bolsa in enumerate(bolsas_filtradas, start=1):
            id_b, nome, tipo, valor, estado, media_min, rend_max = bolsa

            ctk.CTkLabel(self.tabela_container, text=str(id_b), font=("Segoe UI", 13)).grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=nome, font=("Segoe UI", 13, "bold"), text_color="#1F2937").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=str(tipo or "N/A"), font=("Segoe UI", 13)).grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.tabela_container, text=f"{valor:,.0f}$", font=("Segoe UI", 13, "bold")).grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")

            # Coluna 4 & 5 mudam dependendo do perfil
            if self.role == "estudante":
                # Mostra a Média Mínima exigida em vez do Estado
                ctk.CTkLabel(self.tabela_container, text=f"{media_min:.1f} val.", font=("Segoe UI", 13)).grid(row=row_idx, column=4, padx=15, pady=10, sticky="w")
                
                # Ação para o estudante: Botão "Candidatar"
                frame_acoes = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
                frame_acoes.grid(row=row_idx, column=5, padx=15, pady=10, sticky="w")
                
                ctk.CTkButton(
                    frame_acoes, text="Candidatar", width=85, height=28, corner_radius=6,
                    fg_color="#EBF0FF", text_color="#1A5CFF", hover_color="#D6E4FF",
                    font=("Segoe UI", 11, "bold"), command=lambda b=bolsa: self.candidatar_bolsa(b)
                ).pack(side="left", padx=4)
            else:
                # Layout Admin original
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

    def candidatar_bolsa(self, bolsa):
        """Ação executada quando um estudante clica em Candidatar"""
        id_b, nome, *rest = bolsa
        messagebox.showinfo("Candidatura", f"Iniciando processo de candidatura para:\n👉 {nome}\n(Implemente a sua lógica de submissão aqui)")

    # (Os métodos abrir_formulario, validar_campo_decimal, salvar_bolsa e eliminar_bolsa permanecem iguais)