from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from datetime import datetime

# Importações das funções do banco de dados
from database import (
    calcular_saldo, resumo_transacoes, listar_transacoes, 
    deletar_transacao, exportar_para_excel, limpar_banco_dados, atualizar_transacao
)

class Dashboard(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        # 1. CARD DE SALDO
        self.card = MDCard(
            orientation="vertical", padding=20, size_hint=(1, None),
            height="150dp", radius=[20], md_bg_color=(0.12, 0.12, 0.18, 1), elevation=2
        )
        
        topo_card = MDBoxLayout(size_hint_y=None, height="30dp")
        topo_card.add_widget(MDLabel(text="SALDO ATUAL", theme_text_color="Hint", font_style="Overline"))
        
        btn_relatorio = MDIconButton(
            icon="file-excel", theme_text_color="Custom", text_color=(0, 0.8, 0.4, 1),
            on_release=self.exportar_dados
        )
        topo_card.add_widget(btn_relatorio)
        
        self.card.add_widget(topo_card)
        self.label_saldo = MDLabel(text="R$ 0,00", halign="center", font_style="H4", theme_text_color="Custom", bold=True)
        self.card.add_widget(self.label_saldo)
        self.add_widget(self.card)

        # 2. RESUMO VISUAL (Substitui o Gráfico Matplotlib)
        self.resumo_box = MDCard(
            orientation="vertical", padding=15, size_hint=(1, None),
            height="120dp", radius=[15], md_bg_color=(0.15, 0.15, 0.22, 1)
        )
        self.label_rec = MDLabel(text="Receitas: R$ 0,00", font_style="Caption", theme_text_color="Custom", text_color=(0, 1, 0.5, 1))
        self.bar_rec = MDProgressBar(value=0, color=(0, 1, 0.5, 1), size_hint_y=None, height="8dp")
        
        self.label_desp = MDLabel(text="Despesas: R$ 0,00", font_style="Caption", theme_text_color="Custom", text_color=(1, 0.3, 0.3, 1))
        self.bar_desp = MDProgressBar(value=0, color=(1, 0.3, 0.3, 1), size_hint_y=None, height="8dp")

        self.resumo_box.add_widget(self.label_rec)
        self.resumo_box.add_widget(self.bar_rec)
        self.resumo_box.add_widget(MDLabel(size_hint_y=None, height="10dp")) # Espaço
        self.resumo_box.add_widget(self.label_desp)
        self.resumo_box.add_widget(self.bar_desp)
        self.add_widget(self.resumo_box)

        # 3. LISTA
        self.add_widget(MDLabel(text="HISTÓRICO RECENTE", font_style="Overline", size_hint_y=None, height="30dp"))
        self.scroll = ScrollView()
        self.lista = MDList()
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        Clock.schedule_once(lambda dt: self.atualizar())

    def atualizar(self, *args):
        saldo = calcular_saldo()
        self.label_saldo.text = self.formatar(saldo)
        self.label_saldo.text_color = (0, 0.8, 0.4, 1) if saldo >= 0 else (1, 0.3, 0.3, 1)
        
        # Atualiza Resumo Visual
        rec, desp = resumo_transacoes()
        total = rec + desp if (rec + desp) > 0 else 1
        self.label_rec.text = f"Receitas: {self.formatar(rec)}"
        self.label_desp.text = f"Despesas: {self.formatar(desp)}"
        self.bar_rec.value = (rec / total) * 100
        self.bar_desp.value = (desp / total) * 100
        
        self.carregar_transacoes()

    def carregar_transacoes(self):
        self.lista.clear_widgets()
        for t in listar_transacoes():
            item = TwoLineAvatarIconListItem(
                text=t["descricao"],
                secondary_text=f"{t['data']} | {t['categoria']} | {self.formatar(t['valor'])}",
                on_release=lambda x, trans=t: self.confirmar_exclusao(trans['id'])
            )
            cor = (0, 1, 0.5, 1) if t["tipo"] == "receita" else (1, 0.3, 0.3, 1)
            item.add_widget(IconLeftWidget(icon="circle", theme_text_color="Custom", text_color=cor))
            self.lista.add_widget(item)

    def confirmar_exclusao(self, id_item):
        self.dialog = MDDialog(
            title="Excluir?", text="Apagar esta transação?",
            buttons=[
                MDFlatButton(text="NÃO", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="SIM", on_release=lambda x: self.executar_exclusao(id_item))
            ]
        )
        self.dialog.open()

    def executar_exclusao(self, id_item):
        deletar_transacao(id_item)
        self.dialog.dismiss()
        self.atualizar()

    def exportar_dados(self, *args):
        try:
            exportar_para_excel("Financas_2026.xlsx", "Geral")
            Snackbar(text="Excel gerado com sucesso!").open()
        except:
            Snackbar(text="Erro ao exportar").open()

    def formatar(self, valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
