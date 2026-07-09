import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox

from interface.estudantes.estudante import Estudante


class Estudantes(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")

        self.pack(fill="both", expand=True)

        self.carregar_imagens()
        self.carregar_dados()
        self.criar_interface()

    # ==========================
    # IMAGENS
    # ==========================

    def carregar(self, caminho, tamanho):
        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)
        return None

    def carregar_imagens(self):

        self.add_icon = self.carregar("assets/adicionar.png", (18, 18))

        self.edit_icon = self.carregar("assets/editar.png", (18, 18))

        self.delete_icon = self.carregar("assets/eliminar.png", (18, 18))

    # ==========================
    # DADOS
    # ==========================

    def carregar_dados(self):

        self.lista_estudantes = [
            Estudante(
                1,
                "João Silva",
                "joao@email.com",
                "US",
                "Eng. Informática",
                15.5,
                "35000$",
            ),
            Estudante(
                2, "Ana Santos", "ana@email.com", "UniPiaget", "Gestão", 16.0, "28000$"
            ),
            Estudante(
                3,
                "Carlos Lima",
                "carlos@email.com",
                "UniCV",
                "Contabilidade",
                14.2,
                "40000$",
            ),
            Estudante(
                4,
                "Maria Costa",
                "maria@email.com",
                "UniMindelo",
                "Direito",
                17.1,
                "30000$",
            ),
            Estudante(
                5,
                "Pedro Borges",
                "pedro@email.com",
                "US",
                "Eng. Civil",
                13.8,
                "45000$",
            ),
        ]

    # ==========================
    # INTERFACE
    # ==========================

    def criar_interface(self):

        self.main = ctk.CTkScrollableFrame(self, fg_color="#F4F6FB")
        self.main.pack(fill="both", expand=True, padx=35, pady=25)

        # ==========================
        # TÍTULO
        # ==========================

        titulo_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            titulo_frame,
            text="Estudantes",
            font=("Segoe UI", 30, "bold"),
            text_color="#0B2A4A",
        ).pack(anchor="w")
        ctk.CTkLabel(
            titulo_frame,
            text="Gerir todos os estudantes registados.",
            font=("Segoe UI", 14),
            text_color="#6B7280",
        ).pack(anchor="w", pady=(5, 0))
        # Linha separadora
        ctk.CTkFrame(self.main, height=1, fg_color="#E5E7EB").pack(
            fill="x", pady=(20, 25)
        )

        # ==========================================
        # BARRA DE FERRAMENTAS
        # ==========================================

        toolbar = ctk.CTkFrame(self.main, fg_color="transparent")

        toolbar.pack(fill="x", pady=(0, 20))

        # Pesquisa

        self.pesquisa = ctk.CTkEntry(
            toolbar,
            width=420,
            height=38,
            placeholder_text="Pesquisar por nome, email ou curso...",
        )

        self.pesquisa.pack(side="left")
        # Filtra em tempo real enquanto o utilizador escreve
        self.pesquisa.bind("<KeyRelease>", self.filtrar)

        # Filtro

        self.filtro = ctk.CTkComboBox(
            toolbar,
            width=140,
            height=38,
            values=["Todos"],
            command=self.filtrar,
        )

        self.filtro.set("Todos")

        self.filtro.pack(side="left", padx=15)

        # Preenche o combobox com as universidades existentes nos dados
        self.atualizar_filtro_universidades()

        # Botão Adicionar

        ctk.CTkButton(
            toolbar,
            text="+ Adicionar Estudante",
            width=190,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.abrir_janela_adicionar,
        ).pack(side="right")

        # ==========================================
        # CARD DA TABELA
        # ==========================================

        card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB",
        )

        card.pack(fill="both", expand=True, pady=(20, 0))

        header = ctk.CTkFrame(card, fg_color="#FFFFFF", height=45)

        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)

        colunas = [
            ("ID", 60),
            ("Nome", 170),
            ("Email", 220),
            ("Universidade", 140),
            ("Curso", 140),
            ("Média", 70),
            ("Rendimento", 120),
            ("Ações", 100),
        ]

        for texto, largura in colunas:

            ctk.CTkLabel(
                header,
                text=texto,
                width=largura,
                anchor="w",
                font=("Segoe UI", 13, "bold"),
                text_color="#1F2937",
                fg_color="transparent",
            ).pack(side="left", padx=5)

       
        self.frame_tabela = ctk.CTkScrollableFrame(
            card, fg_color="#FFFFFF", corner_radius=0
        )

        self.frame_tabela.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.atualizar_tabela()

    # ==========================================
    # FILTRO / PESQUISA
    # ==========================================

    def atualizar_filtro_universidades(self):
        """Mantém o combobox de filtro sincronizado com as universidades existentes."""
        universidades = sorted({e.universidade for e in self.lista_estudantes})
        valores = ["Todos"] + universidades
        self.filtro.configure(values=valores)
        if self.filtro.get() not in valores:
            self.filtro.set("Todos")

    def filtrar(self, *_args):
        """Filtra a lista de estudantes pelo texto pesquisado e pela universidade escolhida."""
        texto = self.pesquisa.get().strip().lower()
        universidade_filtro = self.filtro.get()

        resultado = []
        for e in self.lista_estudantes:
            corresponde_texto = (
                texto in e.nome.lower()
                or texto in e.email.lower()
                or texto in e.curso.lower()
            )
            corresponde_universidade = (
                universidade_filtro == "Todos" or e.universidade == universidade_filtro
            )
            if corresponde_texto and corresponde_universidade:
                resultado.append(e)

        self.atualizar_tabela(resultado)

    # ==========================================
    # FORMULÁRIO (ADICIONAR / EDITAR)
    # ==========================================

    def abrir_janela_adicionar(self):
        self._abrir_janela_formulario("Adicionar Estudante")

    def abrir_janela_editar(self, estudante):
        self._abrir_janela_formulario("Editar Estudante", estudante)

    def _abrir_janela_formulario(self, titulo, estudante=None):
        """
        Janela partilhada para Adicionar/Editar.
        Usa variáveis locais (closures) em vez de atributos self.entry_x,
        para que Adicionar e Editar não colidam entre si.
        """

        janela = ctk.CTkToplevel(self)
        janela.title(titulo)
        janela.geometry("550x620")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela, text=titulo, font=("Segoe UI", 22, "bold")
        ).pack(pady=(20, 25))

        campos = {}

        def criar_campo(rotulo, valor_inicial=""):
            ctk.CTkLabel(janela, text=rotulo).pack(anchor="w", padx=40)
            entry = ctk.CTkEntry(janela, width=450)
            entry.pack(padx=40, pady=(0, 15))
            if valor_inicial != "":
                entry.insert(0, str(valor_inicial))
            campos[rotulo] = entry

        criar_campo("Nome", estudante.nome if estudante else "")
        criar_campo("Email", estudante.email if estudante else "")
        criar_campo("Universidade", estudante.universidade if estudante else "")
        criar_campo("Curso", estudante.curso if estudante else "")
        criar_campo("Média", estudante.media if estudante else "")
        criar_campo(
            "Rendimento Familiar", estudante.rendimento_familiar if estudante else ""
        )

        def guardar():
            nome = campos["Nome"].get().strip()
            email = campos["Email"].get().strip()
            universidade = campos["Universidade"].get().strip()
            curso = campos["Curso"].get().strip()
            media_texto = campos["Média"].get().strip()
            rendimento = campos["Rendimento Familiar"].get().strip()

            if not all([nome, email, universidade, curso, media_texto, rendimento]):
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            # Aceita tanto "15.5" como "15,5" (vírgula decimal em pt-CV)
            try:
                media = float(media_texto.replace(",", "."))
            except ValueError:
                messagebox.showerror(
                    "Valor inválido", "A média deve ser um número (ex: 15.5)."
                )
                return

            if estudante is None:
                # ID seguro: maior ID atual + 1 (evita duplicados)
                novo_id = max((e.id for e in self.lista_estudantes), default=0) + 1
                novo = Estudante(
                    novo_id, nome, email, universidade, curso, media, rendimento
                )
                self.lista_estudantes.append(novo)
                print("Estudante adicionado:", novo.nome)
            else:
                estudante.nome = nome
                estudante.email = email
                estudante.universidade = universidade
                estudante.curso = curso
                estudante.media = media
                estudante.rendimento_familiar = rendimento
                print("Estudante atualizado:", estudante.nome)

            self.atualizar_filtro_universidades()
            self.filtrar()
            janela.destroy()

        ctk.CTkButton(
            janela,
            text="Guardar",
            width=180,
            height=40,
            fg_color="#2563EB",
            command=guardar,
        ).pack(pady=10)

    # ==========================================
    # TABELA
    # ==========================================

    def atualizar_tabela(self, lista=None):

        lista = lista if lista is not None else self.lista_estudantes

        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        larguras = [60, 170, 220, 140, 140, 70, 120]

        if not lista:
            ctk.CTkLabel(
                self.frame_tabela,
                text="Nenhum estudante encontrado.",
                font=("Segoe UI", 13),
                text_color="#6B7280",
            ).pack(pady=20)
            return

        for estudante in lista:

            linha = ctk.CTkFrame(self.frame_tabela, fg_color="transparent", height=40)

            linha.pack(fill="x", pady=2)

            # ==========================================
            # AÇÕES (Editar / Eliminar)
            # ----------------------------------------
           

            acoes = ctk.CTkFrame(linha, fg_color="transparent", width=100)
            acoes.pack(side="right", padx=(5, 0))

            ctk.CTkButton(
                acoes,
                text="" if self.edit_icon else "Editar",
                image=self.edit_icon,
                width=32,
                height=32,
                corner_radius=8,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                command=lambda e=estudante: self.abrir_janela_editar(e),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes,
                text="" if self.delete_icon else "Eliminar",
                image=self.delete_icon,
                width=32,
                height=32,
                corner_radius=8,
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=lambda e=estudante: self.eliminar_estudante(e),
            ).pack(side="left", padx=2)

            dados = [
                estudante.id,
                estudante.nome,
                estudante.email,
                estudante.universidade,
                estudante.curso,
                estudante.media,
                self.formatar_rendimento(estudante.rendimento_familiar),
            ]

            # Colunas de dados (empacotadas depois, à esquerda)
            for valor, largura in zip(dados, larguras):

                ctk.CTkLabel(
                    linha,
                    text=str(valor),
                    width=largura,
                    anchor="w",
                    font=("Segoe UI", 12),
                    text_color="#374151",
                ).pack(side="left", padx=5)

    @staticmethod
    def formatar_rendimento(valor):
        """Formata '35000$' como '35.000$' (separador de milhar), igual ao design."""
        texto = str(valor)
        numero = texto.replace("$", "").strip()
        if numero.isdigit():
            numero_formatado = f"{int(numero):,}".replace(",", ".")
            return f"{numero_formatado}$"
        return texto

    def eliminar_estudante(self, estudante):

        resposta = messagebox.askyesno(
            "Eliminar Estudante", f"Deseja eliminar {estudante.nome}?"
        )

        if not resposta:
            return

        self.lista_estudantes.remove(estudante)

        # Reorganizar os IDs
        for i, est in enumerate(self.lista_estudantes, start=1):
            est.id = i

        self.atualizar_filtro_universidades()
        self.filtrar()


if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1500x900")

    app.title("Estudantes")

    Estudantes(app)

    app.mainloop()