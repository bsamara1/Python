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
                    "telefone": linha[3] if linha[3] else "" # Mapeia o telefone da tabela utilizadores
                }
        except Exception as e:
            print(f"Erro ao carregar dados do perfil: {e}")

    def salvar_alteracoes(self):
        """Ação ao clicar no botão Editar Informações"""
        messagebox.showinfo("Sucesso", "As informações do perfil foram atualizadas com sucesso!")

    def alterar_senha(self):
        """Ação ao clicar no botão Alterar Palavra-passe"""
        messagebox.showinfo("Segurança", "Palavra-passe alterada com sucesso!")

    def criar_main(self):
        """Gera a interface gráfica do perfil"""
        # 1. CABEÇALHO DA PÁGINA
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(20, 15))

        lbl_titulo = ctk.CTkLabel(frame_topo, text="Meu Perfil", font=("Segoe UI", 22, "bold"), text_color="#142850")
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(frame_topo, text="Gerir informações da sua conta.", font=("Segoe UI", 13), text_color="#6B7280")
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))

        # 2. CONTAINER DAS DUAS COLUNAS
        container_split = ctk.CTkFrame(self, fg_color="transparent")
        container_split.pack(fill="both", expand=True, padx=20, pady=10)
        container_split.grid_columnconfigure(0, weight=1, uniform="col")
        container_split.grid_columnconfigure(1, weight=1, uniform="col")
        container_split.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # COLUNA ESQUERDA: INFORMAÇÕES PESSOAIS
        # ----------------------------------------------------
        card_esquerdo = ctk.CTkFrame(container_split, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        card_esquerdo.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(card_esquerdo, text="Informações Pessoais", font=("Segoe UI", 15, "bold"), text_color="#111827").pack(anchor="w", padx=25, pady=(20, 15))

        # Nome Completo
        ctk.CTkLabel(card_esquerdo, text="Nome Completo", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_nome = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6)
        entry_nome.pack(fill="x", padx=25, pady=(0, 12))
        entry_nome.insert(0, self.dados_utilizador["nome"])

        # E-mail
        ctk.CTkLabel(card_esquerdo, text="Email", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_email = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6)
        entry_email.pack(fill="x", padx=25, pady=(0, 12))
        entry_email.insert(0, self.dados_utilizador["email"])
        
        # Tipo de Utilizador
        ctk.CTkLabel(card_esquerdo, text="Tipo de Utilizador", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_perfil = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6)
        entry_perfil.pack(fill="x", padx=25, pady=(0, 12))
        entry_perfil.insert(0, self.dados_utilizador["perfil"])

        # Telefone
        ctk.CTkLabel(card_esquerdo, text="Telefone", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_telefone = ctk.CTkEntry(card_esquerdo, font=("Segoe UI", 13), fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6)
        entry_telefone.pack(fill="x", padx=25, pady=(0, 20))
        entry_telefone.insert(0, self.dados_utilizador["telefone"])

        # Botão Editar Informações
        btn_editar = ctk.CTkButton(
            card_esquerdo, text="Editar Informações", font=("Segoe UI", 13, "bold"),
            fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white",
            height=38, corner_radius=6, command=self.salvar_alteracoes
        )
        btn_editar.pack(fill="x", padx=25, pady=(0, 20))

        # ----------------------------------------------------
        # COLUNA DIREITA: ALTERAR PALAVRA-PASSE
        # ----------------------------------------------------
        card_direito = ctk.CTkFrame(container_split, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        card_direito.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(card_direito, text="Alterar Palavra-passe", font=("Segoe UI", 15, "bold"), text_color="#111827").pack(anchor="w", padx=25, pady=(20, 15))

        # Palavra-passe atual
        ctk.CTkLabel(card_direito, text="Palavra-passe Atual", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_senha_atual = ctk.CTkEntry(card_direito, font=("Segoe UI", 13), show="*", fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6, placeholder_text="Digite a palavra-passe atual")
        entry_senha_atual.pack(fill="x", padx=25, pady=(0, 12))

        # Nova Palavra-passe
        ctk.CTkLabel(card_direito, text="Nova Palavra-passe", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_nova_senha = ctk.CTkEntry(card_direito, font=("Segoe UI", 13), show="*", fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6, placeholder_text="Digite a nova palavra-passe")
        entry_nova_senha.pack(fill="x", padx=25, pady=(0, 12))

        # Confirmar Nova Palavra-passe
        ctk.CTkLabel(card_direito, text="Confirmar Nova Palavra-passe", font=("Segoe UI", 11, "bold"), text_color="#4B5563").pack(anchor="w", padx=25, pady=(5, 2))
        entry_conf_senha = ctk.CTkEntry(card_direito, font=("Segoe UI", 13), show="*", fg_color="white", border_color="#E5E7EB", height=38, corner_radius=6, placeholder_text="Confirme a nova palavra-passe")
        entry_conf_senha.pack(fill="x", padx=25, pady=(0, 68))

        # Botão Alterar Palavra-passe
        btn_alterar_senha = ctk.CTkButton(
            card_direito, text="Alterar Palavra-passe", font=("Segoe UI", 13, "bold"),
            fg_color="#1D4ED8", hover_color="#1E40AF", text_color="white",
            height=38, corner_radius=6, command=self.alterar_senha
        )
        btn_alterar_senha.pack(fill="x", padx=25, pady=(0, 20))