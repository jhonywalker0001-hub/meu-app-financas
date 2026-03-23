from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from database import (
    calcular_saldo, resumo_transacoes, listar_transacoes, 
    deletar_transacao, exportar_para_excel
)

class Dashboard(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        # CARD DE SALDO
        self.card = MDCard(
            orientation="vertical", padding=20, size_hint=(1, None),
            height="140dp", radius=[20], md_bg_color=(0.12, 0.12, 0.18, 1), elevation=2
        )
        
        topo = MDBoxLayout(size_hint_y=None, height="30dp")
        topo.add_widget(MDLabel(text="SALDO ATUAL", theme_text_color="Hint", font_style="Overline"))
        topo.add_widget(MDIconButton(icon="file-excel", on_release=self.exportar))
        
        self.card.add_widget(topo)
        self.label_saldo = MDLabel(text="R$ 0,00", halign="center", font_style="H4", theme_text_color="Custom", bold=True)
        self.card.add_widget(self.label_saldo)
        self.add_widget(self.card)

        # RESUMO SIMPLES
        self.resumo = MDLabel(text="", halign="center", theme_text_color="Hint", size_hint_y=None, height="40dp")
        self.add_widget(self.resumo)

        # LISTA
        self.add_widget(MDLabel(text="HISTÓRICO", font_style="Overline", size_hint_y=None, height="30dp"))
        self.scroll = ScrollView()
        self.lista = MDList()
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        Clock.schedule_once(lambda dt: self.atualizar())

    def atualizar(self, *args):
        saldo = calcular_saldo()
        rec, desp = resumo_transacoes()
        self.label_saldo.text = f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.label_saldo.text_color = (0, 0.8, 0.4, 1) if saldo >= 0 else (1, 0.3, 0.3, 1)
        self.resumo.text = f"Receitas: R$ {rec:,.2f}  |  Despesas: R$ {desp:,.2f}"
        self.carregar_transacoes()

    def carregar_transacoes(self):
        self.lista.clear_widgets()
        for t in listar_transacoes():
            item = TwoLineAvatarIconListItem(
                text=t["descricao"],
                secondary_text=f"{t['data']} | R$ {t['valor']:,.2f}",
                on_release=lambda x, id_t=t["id"]: self.deletar(id_t)
            )
            cor = (0, 1, 0.5, 1) if t["tipo"] == "receita" else (1, 0.3, 0.3, 1)
            item.add_widget(IconLeftWidget(icon="circle", theme_text_color="Custom", text_color=cor))
            self.lista.add_widget(item)

    def deletar(self, id_t):
        deletar_transacao(id_t)
        self.atualizar()
        Snackbar(text="Excluído!").open()

    def exportar(self, *args):
        exportar_para_excel("Financas.xlsx", "Geral")
        Snackbar(text="Excel gerado!").open()
