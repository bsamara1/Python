# interface/admin/relatorios.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from database.database import conectar

class RelatoriosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F4F6FB")
        self.caminho_db = "database.db"  # <- Adicione esta linha no __init__
        self.metricas = {}
        self.atualizar_dados()
        self.criar_interface()

    def obter_metricas(self):
        """Extrai métricas reais da BD"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            # Total de estudantes
            cursor.execute("SELECT COUNT(*) FROM estudantes")
            total_estudantes = cursor.fetchone()[0]

            # Total de bolsas
            cursor.execute("SELECT COUNT(*) FROM bolsas")
            total_bolsas = cursor.fetchone()[0]

            # Total de candidaturas
            cursor.execute("SELECT COUNT(*) FROM candidaturas")
            total_candidaturas = cursor.fetchone()[0]

            # Candidaturas aprovadas
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE estado = 'Aprovada'")
            aprovadas = cursor.fetchone()[0]

            # Taxa de aprovação
            taxa_aprovacao = (aprovadas / total_candidaturas * 100) if total_candidaturas > 0 else 0

            # Total investido
            cursor.execute("SELECT SUM(valor) FROM bolsas WHERE estado = 'Ativo'")
            total_investido = cursor.fetchone()[0] or 0

            conn.close()

            return {
                "total_estudantes": total_estudantes,
                "total_bolsas": total_bolsas,
                "total_candidaturas": total_candidaturas,
                "aprovadas": aprovadas,
                "taxa_aprovacao": f"{taxa_aprovacao:.1f}%",
                "total_investido": f"{total_investido:,.0f}$"
            }
        except Exception as e:
            print(f"Erro ao obter métricas: {e}")
            return {}

    def atualizar_dados(self):
        """Atualiza os dados de métricas"""
        self.metricas = self.obter_metricas()

    def criar_interface(self):
        # CABEÇALHO
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(frame_topo, text="Relatórios & Estatísticas", font=("Segoe UI", 24, "bold"), text_color="#142850").pack(anchor="w")
        ctk.CTkLabel(frame_topo, text="Análise de dados, métricas em tempo real e exportação de relatórios.", font=("Segoe UI", 13), text_color="#6B7280").pack(anchor="w", pady=(4, 0))

        # MÉTRICAS
        frame_metricas = ctk.CTkFrame(self, fg_color="transparent")
        frame_metricas.pack(fill="x", padx=20, pady=15)
        frame_metricas.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_card0 = ctk.CTkLabel(frame_metricas, text="---", font=("Segoe UI", 16, "bold"))
        self.lbl_card1 = ctk.CTkLabel(frame_metricas, text="---", font=("Segoe UI", 16, "bold"))
        self.lbl_card2 = ctk.CTkLabel(frame_metricas, text="---", font=("Segoe UI", 16, "bold"))
        self.lbl_card3 = ctk.CTkLabel(frame_metricas, text="---", font=("Segoe UI", 16, "bold"))

        self.criar_mini_card_ref(frame_metricas, 0, "Taxa Aprovação", self.lbl_card0, "#ECFFF0", "#03543F")
        self.criar_mini_card_ref(frame_metricas, 1, "Total Investido", self.lbl_card1, "#EEF4FF", "#1E40AF")
        self.criar_mini_card_ref(frame_metricas, 2, "Candidaturas", self.lbl_card2, "#FFF8EA", "#92400E")
        self.criar_mini_card_ref(frame_metricas, 3, "Bolsas Ativas", self.lbl_card3, "#F6EEFF", "#6B21A8")

        # Atualizar labels com dados reais
        self.lbl_card0.configure(text=self.metricas.get("taxa_aprovacao", "---"))
        self.lbl_card1.configure(text=self.metricas.get("total_investido", "---"))
        self.lbl_card2.configure(text=str(self.metricas.get("total_candidaturas", "---")))
        self.lbl_card3.configure(text=str(self.metricas.get("total_bolsas", "---")))

        # GRÁFICOS
        container_graficos = ctk.CTkFrame(self, fg_color="transparent")
        container_graficos.pack(fill="both", expand=True, padx=20, pady=15)
        container_graficos.grid_columnconfigure((0, 1), weight=1)
        container_graficos.grid_rowconfigure(0, weight=1)

        # Gráfico de pizza (estados das candidaturas)
        card_esq = ctk.CTkFrame(container_graficos, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_esq.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        ctk.CTkLabel(card_esq, text="Candidaturas por Estado", font=("Segoe UI", 14, "bold"), text_color="#142850").pack(padx=15, pady=(15, 5))

        self.fig_pizza = Figure(figsize=(4, 3), dpi=80, facecolor='white')
        self.criar_grafico_pizza()
        self.canvas_pizza = FigureCanvasTkAgg(self.fig_pizza, master=card_esq)
        self.canvas_pizza.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(
            card_esq, text="Exportar PDF", fg_color="#1D4ED8", hover_color="#1E40AF",
            font=("Segoe UI", 11, "bold"), height=35, command=self.exportar_pdf
        ).pack(fill="x", padx=15, pady=(0, 15))

        # Gráfico de linha (candidaturas por mês)
        card_dir = ctk.CTkFrame(container_graficos, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        card_dir.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        ctk.CTkLabel(card_dir, text="Candidaturas por Mês", font=("Segoe UI", 14, "bold"), text_color="#142850").pack(padx=15, pady=(15, 5))

        self.fig_linha = Figure(figsize=(4, 3), dpi=80, facecolor='white')
        self.criar_grafico_linha()
        self.canvas_linha = FigureCanvasTkAgg(self.fig_linha, master=card_dir)
        self.canvas_linha.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(
            card_dir, text="Exportar Excel", fg_color="#10B981", hover_color="#059669",
            font=("Segoe UI", 11, "bold"), height=35, command=self.exportar_excel
        ).pack(fill="x", padx=15, pady=(0, 15))

    def criar_mini_card_ref(self, parent, col, titulo, label_ref, cor_fundo, cor_texto):
        """Cria um card com referência a label para atualização dinâmica"""
        card = ctk.CTkFrame(parent, fg_color=cor_fundo, corner_radius=12, height=85)
        card.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
        card.pack_propagate(False)

        label_ref.configure(text_color=cor_texto, font=("Segoe UI", 18, "bold"))
        label_ref.place(in_=card, relx=0.5, rely=0.35, anchor="center")

        lbl_tit = ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 11, "bold"), text_color="#6B7280")
        lbl_tit.place(relx=0.5, rely=0.75, anchor="center")

    def criar_grafico_pizza(self):
        """Cria gráfico de pizza com candidaturas por estado"""
        try:
            conn = sqlite3.connect(self.caminho_db)
            cursor = conn.cursor()
            cursor.execute("SELECT estado, COUNT(*) FROM candidaturas GROUP BY estado")
            dados = cursor.fetchall()
            conn.close()

            if dados:
                estados = [d[0] for d in dados]
                valores = [d[1] for d in dados]
                cores = ["#10B981", "#F59E0B", "#EF4444"]

                ax = self.fig_pizza.add_subplot(111)
                ax.pie(valores, labels=estados, autopct='%1.1f%%', colors=cores[:len(estados)], startangle=90)
                ax.set_title("")
            else:
                ax = self.fig_pizza.add_subplot(111)
                ax.text(0.5, 0.5, "Sem dados", ha='center', va='center', transform=ax.transAxes)

        except Exception as e:
            print(f"Erro ao criar gráfico de pizza: {e}")

    def criar_grafico_linha(self):
        """Cria gráfico de linha com candidaturas por mês"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT strftime('%Y-%m', data_candidatura), COUNT(*)
                FROM candidaturas
                WHERE data_candidatura IS NOT NULL
                GROUP BY strftime('%Y-%m', data_candidatura)
                ORDER BY strftime('%Y-%m', data_candidatura) DESC
                LIMIT 6
            """)
            dados = sorted(cursor.fetchall())
            conn.close()

            if dados:
                meses = [d[0][-2:] for d in dados]
                valores = [d[1] for d in dados]

                ax = self.fig_linha.add_subplot(111)
                ax.plot(range(len(meses)), valores, marker='o', color='#1A5CFF', linewidth=2, markersize=6)
                ax.fill_between(range(len(meses)), valores, alpha=0.3, color='#1A5CFF')
                ax.set_xticks(range(len(meses)))
                ax.set_xticklabels(meses, rotation=45)
                ax.set_title("")
                ax.grid(True, alpha=0.3)
            else:
                ax = self.fig_linha.add_subplot(111)
                ax.text(0.5, 0.5, "Sem dados", ha='center', va='center', transform=ax.transAxes)

        except Exception as e:
            print(f"Erro ao criar gráfico de linha: {e}")

    def exportar_pdf(self):
        """Exporta relatório em PDF"""
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Relatório_Candidaturas_{datetime.now().strftime('%Y%m%d')}.pdf"
            )

            if not caminho:
                return

            doc = SimpleDocTemplate(caminho, pagesize=letter)
            story = []

            story.append(Paragraph("RELATÓRIO DE CANDIDATURAS", getSampleStyleSheet()['Heading1']))
            story.append(Spacer(1, 0.3*inch))

            metricas_data = [
                ["Métrica", "Valor"],
                ["Total de Estudantes", str(self.metricas.get("total_estudantes", "N/A"))],
                ["Total de Bolsas", str(self.metricas.get("total_bolsas", "N/A"))],
                ["Total de Candidaturas", str(self.metricas.get("total_candidaturas", "N/A"))],
                ["Candidaturas Aprovadas", str(self.metricas.get("aprovadas", "N/A"))],
                ["Taxa de Aprovação", str(self.metricas.get("taxa_aprovacao", "N/A"))],
                ["Total Investido", str(self.metricas.get("total_investido", "N/A"))]
            ]

            table = Table(metricas_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(table)
            doc.build(story)

            messagebox.showinfo("Sucesso", f"Relatório PDF exportado com sucesso!\n{caminho}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF: {str(e)}")

    def exportar_excel(self):
        """Exporta relatório em Excel"""
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"Relatório_Candidaturas_{datetime.now().strftime('%Y%m%d')}.xlsx"
            )

            if not caminho:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório"

            # Estilo
            header_fill = PatternFill(start_color="1A5CFF", end_color="1A5CFF", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # Headers
            headers = ["Métrica", "Valor"]
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = border
                cell.alignment = Alignment(horizontal="center")

            # Dados
            dados = [
                ["Total de Estudantes", self.metricas.get("total_estudantes", "N/A")],
                ["Total de Bolsas", self.metricas.get("total_bolsas", "N/A")],
                ["Total de Candidaturas", self.metricas.get("total_candidaturas", "N/A")],
                ["Candidaturas Aprovadas", self.metricas.get("aprovadas", "N/A")],
                ["Taxa de Aprovação", self.metricas.get("taxa_aprovacao", "N/A")],
                ["Total Investido", self.metricas.get("total_investido", "N/A")]
            ]

            for row_idx, row_data in enumerate(dados, 2):
                for col_idx, value in enumerate(row_data, 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border
                    cell.alignment = Alignment(horizontal="center")

            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 20

            wb.save(caminho)
            messagebox.showinfo("Sucesso", f"Relatório Excel exportado com sucesso!\n{caminho}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar Excel: {str(e)}")