from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget, OneLineListItem
from kivy.uix.scrollview import ScrollView
import matplotlib.pyplot as plt
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
import io 
import tkinter as tk
from tkinter import filedialog
from kivy.core.image import Image as CoreImage 
from datetime import datetime

# Importações das funções do banco de dados
from database import (
    calcular_saldo, resumo_transacoes, listar_transacoes, 
    deletar_transacao, exportar_para_excel, exportar_para_pdf,
    atualizar_transacao, limpar_banco_dados
)

class Dashboard(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        # 1. CARD DE SALDO
        self.card = MDCard(
            orientation="vertical", padding=15, size_hint=(1, None),
            height="140dp", radius=[20], md_bg_color=(0.12, 0.12, 0.18, 1), elevation=2
        )
        
        topo_card = MDBoxLayout(size_hint_y=None, height="30dp")
        topo_card.add_widget(MDLabel(text="Saldo disponível", theme_text_color="Hint", font_style="Caption"))
        
        # Botão Limpar Tudo (Vassoura)
        btn_limpar = MDIconButton(
            icon="broom", 
            theme_text_color="Custom", 
            text_color=(1, 0.3, 0.3, 1),
            on_release=self.confirmar_limpeza_geral
        )
        topo_card.add_widget(btn_limpar)

        btn_relatorio = MDIconButton(
            icon="file-download-outline", 
            theme_text_color="Custom", 
            text_color=(0, 0.8, 0.4, 1),
            on_release=self.abrir_seletor_mes
        )
        topo_card.add_widget(btn_relatorio)
        
        self.card.add_widget(topo_card)
        self.label_saldo = MDLabel(text="R$ 0,00", halign="center", font_style="H4", theme_text_color="Custom", bold=True)
        self.card.add_widget(self.label_saldo)
        self.add_widget(self.card)

        # 2. CAMPO DE PESQUISA
        self.search_field = MDTextField(
            hint_text="Pesquisar transação...",
            mode="round",
            size_hint_y=None,
            height="45dp",
            icon_right="magnify"
        )
        self.search_field.bind(text=self.filtrar_transacoes)
        self.add_widget(self.search_field)

        # 3. GRÁFICO
        self.container_grafico = MDBoxLayout(size_hint=(1, None), height="200dp", padding=[0, 5, 0, 5])
        self.img_grafico = Image(allow_stretch=True)
        self.container_grafico.add_widget(self.img_grafico)
        self.add_widget(self.container_grafico)

        self.add_widget(MDLabel(text="Histórico", font_style="Subtitle2", size_hint_y=None, height="30dp", bold=True))

        # 4. LISTA DE TRANSAÇÕES
        self.scroll = ScrollView()
        self.lista = MDList()
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        Clock.schedule_once(lambda dt: self.atualizar())

    def filtrar_transacoes(self, instance, value):
        search_term = value.lower()
        self.lista.clear_widgets()
        dados = listar_transacoes()
        for t in dados:
            desc = (t["descricao"] or "").lower()
            cat = (t["categoria"] or "").lower()
            if search_term in desc or search_term in cat:
                self.adicionar_item_lista(t)

    def carregar_transacoes(self):
        self.lista.clear_widgets()
        dados = listar_transacoes()
        for t in dados:
            self.adicionar_item_lista(t)

    def adicionar_item_lista(self, t):
        item = TwoLineAvatarIconListItem(
            text=t["descricao"] or "Sem descrição",
            secondary_text=f"{t['data']}  •  {t['categoria']}  •  {self.formatar(t['valor'])}",
            theme_text_color="Custom", text_color=(1, 1, 1, 1),
            on_release=lambda x, trans=t: self.abrir_dialogo_edicao(trans)
        )
        cor = (0, 0.8, 0.4, 1) if t["tipo"] == "receita" else (1, 0.3, 0.3, 1)
        item.add_widget(IconLeftWidget(icon="cash", theme_text_color="Custom", text_color=cor))
        
        btn_del = IconRightWidget(icon="delete-outline", theme_text_color="Custom", text_color=(0.5, 0.5, 0.5, 1))
        btn_del.on_release = lambda x, id_t=t["id"]: self.confirmar_exclusao(id_t)
        item.add_widget(btn_del)
        self.lista.add_widget(item)

    def confirmar_limpeza_geral(self, *args):
        self.dialog_clear = MDDialog(
            title="Limpar tudo?",
            text="Deseja apagar permanentemente TODAS as transações?",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog_clear.dismiss()),
                MDFlatButton(text="LIMPAR", text_color=(1, 0, 0, 1), on_release=self.executar_limpeza_geral)
            ]
        )
        self.dialog_clear.open()

    def executar_limpeza_geral(self, *args):
        limpar_banco_dados()
        self.dialog_clear.dismiss()
        self.atualizar()
        Snackbar(text="O histórico foi totalmente limpo!").open()

    def confirmar_exclusao(self, id_item):
        self.dialog_confirm = MDDialog(
            title="Excluir transação?",
            text="Tem certeza que deseja apagar este registro?",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog_confirm.dismiss()),
                MDFlatButton(text="EXCLUIR", text_color=(1, 0, 0, 1), on_release=lambda x: self.executar_exclusao(id_item))
            ]
        )
        self.dialog_confirm.open()

    def executar_exclusao(self, id_item):
        deletar_transacao(id_item)
        if hasattr(self, 'dialog_confirm'): self.dialog_confirm.dismiss()
        self.atualizar()
        Snackbar(text="Transação excluída!").open()

    def abrir_dialogo_edicao(self, trans):
        layout = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="280dp")
        
        # Implementando o campo limpo: text='' e o valor antigo vai para o hint_text
        self.edit_desc = MDTextField(text=str(trans['descricao']), hint_text="Descrição")
        self.edit_valor = MDTextField(
            text="", 
            hint_text=f"Valor atual: {trans['valor']}", 
            input_filter="float",
            helper_text="Digite o novo valor",
            helper_text_mode="on_focus"
        )
        self.edit_cat = MDTextField(text=str(trans['categoria']), hint_text="Categoria")
        self.edit_data = MDTextField(text=str(trans['data']), hint_text="Data (DD/MM/AAAA)")
        
        layout.add_widget(self.edit_desc)
        layout.add_widget(self.edit_valor)
        layout.add_widget(self.edit_cat)
        layout.add_widget(self.edit_data)

        self.dialog_edit = MDDialog(
            title="Editar Transação", type="custom", content_cls=layout,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog_edit.dismiss()),
                MDFlatButton(text="SALVAR", theme_text_color="Custom", text_color=(0, 0.8, 0.4, 1),
                             on_release=lambda x: self.salvar_edicao(trans['id'], trans['tipo'], trans['valor']))
            ]
        )
        self.dialog_edit.open()

    def salvar_edicao(self, id_t, tipo_t, valor_antigo):
        try:
            # Se o campo de valor estiver vazio, mantém o valor antigo
            novo_valor = float(self.edit_valor.text) if self.edit_valor.text else valor_antigo
            
            atualizar_transacao(id_t, tipo_t, novo_valor, 
                                self.edit_desc.text, self.edit_cat.text, self.edit_data.text)
            self.dialog_edit.dismiss()
            self.atualizar()
            Snackbar(text="Alterações salvas!").open()
        except:
            Snackbar(text="Erro ao salvar. Verifique o valor.").open()

    def abrir_seletor_mes(self, *args):
        meses = []
        data_atual = datetime.now()
        for i in range(6):
            mes = data_atual.month - i
            ano = data_atual.year
            if mes <= 0: mes += 12; ano -= 1
            meses.append(f"{mes:02d}/{ano}")
        meses.append("Geral")
        
        scroll_dialogo = ScrollView(size_hint_y=None, height="300dp")
        items_lista = MDList()
        for m in meses:
            items_lista.add_widget(OneLineListItem(text=m, on_release=lambda x, mes=m: self.preparar_salvamento(mes)))
        scroll_dialogo.add_widget(items_lista)

        self.dialog_mes = MDDialog(title="Relatório de qual mês?", type="custom", content_cls=scroll_dialogo,
                                   buttons=[MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog_mes.dismiss())])
        self.dialog_mes.open()

    def preparar_salvamento(self, mes_selecionado):
        self.dialog_mes.dismiss()
        try:
            root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
            caminho = filedialog.asksaveasfilename(initialfile=f"Relatorio_{mes_selecionado.replace('/', '_')}",
                defaultextension=".pdf", filetypes=[("PDF", "*.pdf"), ("Excel", "*.xlsx")])
            root.destroy()
            if caminho:
                if caminho.endswith(".pdf"): exportar_para_pdf(caminho, mes_selecionado)
                else: exportar_para_excel(caminho, mes_selecionado)
                Snackbar(text=f"Salvo!", bg_color=(0, 0.6, 0.3, 1)).open()
        except: Snackbar(text="Erro ao exportar").open()

    def formatar(self, valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def atualizar(self, *args):
        saldo = calcular_saldo()
        # Saldo Inteligente: Verde para positivo, Vermelho para negativo
        self.label_saldo.text_color = (0, 0.8, 0.4, 1) if saldo >= 0 else (1, 0.3, 0.3, 1)
        self.label_saldo.text = self.formatar(saldo)
        self.criar_grafico()
        self.carregar_transacoes()

    def criar_grafico(self):
        rec, desp = resumo_transacoes()
        if rec == 0 and desp == 0:
            self.container_grafico.opacity = 0
            return
        self.container_grafico.opacity = 1
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#000000') 
        ax.pie([rec, desp], colors=['#00E676', '#FF5252'], startangle=90, autopct='%1.1f%%', textprops={'color': 'w'})
        ax.add_artist(plt.Circle((0,0), 0.70, fc='#12121e'))
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120)
        plt.close(fig)
        buf.seek(0)
        self.img_grafico.texture = CoreImage(buf, ext='png').texture