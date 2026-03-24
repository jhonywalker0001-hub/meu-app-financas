from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from database import adicionar_transacao


class AddTransacao(MDBoxLayout):

    def __init__(self, dashboard, atualizar_lista, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=20, **kwargs)

        self.dashboard = dashboard
        self.atualizar_lista = atualizar_lista
        self.tipo = "receita"

        self.valor = MDTextField(
            hint_text="Valor",
            input_filter="float"
        )

        btn_receita = MDRaisedButton(
            text="Receita",
            on_release=lambda x: self.set_tipo("receita")
        )

        btn_despesa = MDRaisedButton(
            text="Despesa",
            on_release=lambda x: self.set_tipo("despesa")
        )

        btn_salvar = MDRaisedButton(
            text="Salvar",
            on_release=self.salvar
        )

        self.add_widget(self.valor)
        self.add_widget(btn_receita)
        self.add_widget(btn_despesa)
        self.add_widget(btn_salvar)

    def set_tipo(self, tipo):
        self.tipo = tipo

    def salvar(self, *args):
        if self.valor.text == "":
            return

        adicionar_transacao(self.tipo, float(self.valor.text))

        self.dashboard.atualizar()
        self.atualizar_lista()

        self.valor.text = ""
