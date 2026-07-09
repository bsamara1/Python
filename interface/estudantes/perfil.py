# interface/admin/perfilUtilizador.py
import customtkinter as ctk
from tkinter import messagebox
from database.database import conectar 

class PerfilUtilizador(ctk.CTkFrame):
    """Página de Perfil do Utilizador integrada com a Base de Dados"""

    def __init__(self, master, id_utilizador_logado):
        super().__init__(master, fg_color="#F4F6FB")

        self.id_utilizador = id_utilizador_logado
        self.dados_utilizador = {"nome": "", "email": "", "perfil": "", "telefone": ""}
        
        self.carregar_dados_bd()
        self.criar_main()

    def carregar_dados_bd(self):
        """Busca as informações reais do utilizador logado na Base de Dados"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Query ajustada: vai buscar o telefone diretamente da tabela de utilizadores (u.telefone)
            cursor.execute("""
                SELECT u.nome, u.email, u.perfil, u.telefone 
                FROM utilizadores u
                WHERE u.id = ?
            """, (self.id_utilizador,))
            
            linha = cursor.fetchone()
            conn.close()

            if linha:
                self.dados_utilizador = {
                    "nome": linha[0] if linha[0] else "",
                    "email": linha[1] if linha[1] else "",
                    "perfil": linha[2] if linha[2] else "",
                    "telefone": linha[3] if linha[3] else "" 
                }
        except Exception as e:
            print(f"Erro ao carregar dados do perfil: {e}")

    def salvar_alteracoes(self):
        """Recolhe as modificações dos campos de texto e atualiza na Base de Dados"""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome or not email:
            messagebox.showerror("Erro", "Os campos Nome e Email não podem ficar vazios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # 1. Atualiza os dados na tabela de utilizadores
            cursor.execute("""
                UPDATE utilizadores 
                SET nome = ?, email = ?, telefone = ? 
                WHERE id = ?
            """, (nome, email, telefone, self.id_utilizador))

            # 2. Se o utilizador também tiver um registo correspondente na tabela de estudantes, atualiza lá também
            cursor.execute("""
                UPDATE estudantes 
                SET nome = ?, email = ?, telefone = ? 
                WHERE email = ? OR telefone = ?
            """, (nome, email, telefone, self.dados_utilizador["email"], self.dados_utilizador["telefone"]))

            conn.commit()
            conn.close()

            # Atualiza os dados em memória do programa
            self.dados_utilizador["nome"] = nome
            self.dados_utilizador["email"] = email
            self.dados_utilizador["telefone"] = telefone

            messagebox.showinfo("Sucesso", "As informações do perfil foram updated com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar as alterações:\n{e}")

    def alterar_senha(self):
        """Valida a palavra-passe atual e atualiza para a nova palavra-passe"""
        senha_atual = self.entry_senha_atual.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()
        conf_senha = self.entry_conf_senha.get().strip()

        if not senha_atual or not nova_senha or not conf_senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos de palavra-passe.")
            return

        if nova_senha != conf_senha:
            messagebox.showerror("Erro", "A nova palavra-passe e a confirmação não coincidem.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Verifica se a palavra-passe atual está correta
            cursor.execute("SELECT senha FROM utilizadores WHERE id = ?", (self.id_utilizador,))
            resultado = cursor.fetchone()

            if not resultado or resultado[0] != senha_atual:
                messagebox.showerror("Erro", "A palavra-passe atual digitada está incorreta.")
                conn.close()
                return

            # Atualiza para a nova palavra-passe
            cursor.execute("UPDATE utilizadores SET senha = ? WHERE id = ?", (nova_senha, self.id_utilizador))
            conn.commit()
            conn.close()

            # Limpa os campos após o sucesso
            self.entry_senha_atual.delete(0, 'end')
            self.entry_nova_senha.delete(0, 'end')
            self.entry_conf_senha.delete(0, 'end')

            messagebox.showinfo("Segurança", "Palavra-passe alterada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar a palavra-passe:\n{e}")

    def criar_main(self):
        """Gera a interface gráfica do perfil com os inputs ampliados e maior preenchimento vertical"""
        # 1. CABEÇALHO DA PÁGINA
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(25, 20))

        lbl_titulo = ctk.CTkLabel(frame_topo, text="Meu Perfil", font=("Segoe UI", 24, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_topo, text="Gerir informações da sua conta e preferências de segurança.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(4, 0))

        # 2. CONTAINER DAS DUAS COLUNAS
        container_split = ctk.CTkFrame(self, fg_color="transparent")
        container_split.pack(fill="both", expand=True, padx=20, pady=10)
        container_split.grid_columnconfigure(0, weight=1, uniform="col")
        container_split.grid_columnconfigure(1, weight=1, uniform="col")
        container_split.grid_rowconfigure(0, weight=1)

        # Configurações globais de tamanho para preenchimento do espaço vazio
        ALTURA_INPUT = 48
        TAMANHO_FONTE = 14
        DISTANCIA_VERTICAL = 16

        # ----------------------------------------------------
        # COLUNA ESQUERDA: INFORMAÇÕES PESSOAIS
        # ----------------------------------------------------
        card_esquerdo = ctk.CTkFrame(container_split, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_esquerdo.grid(row=0, column=0, sticky="nsew", padx=12, pady=5)

        ctk.CTkLabel(card_esquerdo, text="Informações Pessoais", font=("Segoe UI", 18, "bold"), text_color="#111827").pack(anchor="w", padx=30, pady=(30, 20))

        # Nome Completo
        ctk.CTkLabel(card_esquerdo, text="Nome Completo", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_nome = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", TAMANHO_FONTE), fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8)
        self.entry_nome.pack(fill="x", padx=30, pady=(0, DISTANCIA_VERTICAL))
        self.entry_nome.insert(0, self.dados_utilizador["nome"])

        # E-mail
        ctk.CTkLabel(card_esquerdo, text="Email", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_email = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", TAMANHO_FONTE), fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8)
        self.entry_email.pack(fill="x", padx=30, pady=(0, DISTANCIA_VERTICAL))
        self.entry_email.insert(0, self.dados_utilizador["email"])
        
        # Tipo de Utilizador (Bloqueado)
        ctk.CTkLabel(card_esquerdo, text="Tipo de Utilizador", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_perfil = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", TAMANHO_FONTE), fg_color="#F3F4F6", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8, state="disabled")
        self.entry_perfil.pack(fill="x", padx=30, pady=(0, DISTANCIA_VERTICAL))
        self.entry_perfil.configure(state="normal")
        self.entry_perfil.insert(0, self.dados_utilizador["perfil"])
        self.entry_perfil.configure(state="disabled")

        # Telefone
        ctk.CTkLabel(card_esquerdo, text="Telefone", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_telefone = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", TAMANHO_FONTE), fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8)
        self.entry_telefone.pack(fill="x", padx=30, pady=(0, 30))
        self.entry_telefone.insert(0, self.dados_utilizador["telefone"])

        # Botão Editar Informações
        btn_editar = ctk.CTkButton(
            card_esquerdo, text="Salvar Alterações do Perfil", font=("Segoe UI", 14, "bold"),
            fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white",
            height=50, corner_radius=8, command=self.salvar_alteracoes
        )
        btn_editar.pack(fill="x", padx=30, pady=(0, 30))

        # ----------------------------------------------------
        # COLUNA DIREITA: ALTERAR PALAVRA-PASSE
        # ----------------------------------------------------
        card_direito = ctk.CTkFrame(container_split, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_direito.grid(row=0, column=1, sticky="nsew", padx=12, pady=5)

        ctk.CTkLabel(card_direito, text="Segurança e Palavra-passe", font=("Segoe UI", 18, "bold"), text_color="#111827").pack(anchor="w", padx=30, pady=(30, 20))

        # Palavra-passe atual
        ctk.CTkLabel(card_direito, text="Palavra-passe Atual", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_senha_atual = ctk.CTkEntry(card_direito, font=("Segoe UI", TAMANHO_FONTE), show="*", fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8, placeholder_text="Digite a sua palavra-passe atual")
        self.entry_senha_atual.pack(fill="x", padx=30, pady=(0, DISTANCIA_VERTICAL))

        # Nova Palavra-passe
        ctk.CTkLabel(card_direito, text="Nova Palavra-passe", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_nova_senha = ctk.CTkEntry(card_direito, font=("Segoe UI", TAMANHO_FONTE), show="*", fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8, placeholder_text="Crie uma nova palavra-passe")
        self.entry_nova_senha.pack(fill="x", padx=30, pady=(0, DISTANCIA_VERTICAL))

        # Confirmar Nova Palavra-passe
        ctk.CTkLabel(card_direito, text="Confirmar Nova Palavra-passe", font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", padx=30, pady=(5, 4))
        self.entry_conf_senha = ctk.CTkEntry(card_direito, font=("Segoe UI", TAMANHO_FONTE), show="*", fg_color="white", border_color="#E5E7EB", height=ALTURA_INPUT, corner_radius=8, placeholder_text="Repita a nova palavra-passe")
        
        # Espaçamento de compensação aumentado no último input para empurrar o botão de senha para o fundo
        self.entry_conf_senha.pack(fill="x", padx=30, pady=(0, 118))

        # Botão Alterar Palavra-passe
        btn_alterar_senha = ctk.CTkButton(
            card_direito, text="Atualizar Palavra-passe", font=("Segoe UI", 14, "bold"),
            fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white",
            height=50, corner_radius=8, command=self.alterar_senha
        )
        btn_alterar_senha.pack(fill="x", padx=30, pady=(0, 30))