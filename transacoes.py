from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

# Importamos a função de salvar do seu database.py
from database import salvar_transacao

class TelaTransacoes(MDBoxLayout):
    def __init__(self, atualizar_dashboard, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)
        self.atualizar_dashboard = atualizar_dashboard

        # Campo de Valor
        self.valor = MDTextField(
            hint_text="Valor (Ex: 50.00)",
            helper_text="Use ponto para centavos",
            helper_text_mode="on_focus",
            input_filter="float"
        )
        self.add_widget(self.valor)

        # Campo de Descrição
        self.descricao = MDTextField(hint_text="Descrição (Ex: Compras Mensais)")
        self.add_widget(self.descricao)

        # Seleção de Tipo (Receita/Despesa)
        self.tipo_selecionado = "despesa"
        self.btn_tipo = MDRaisedButton(
            text="Tipo: Despesa",
            pos_hint={'center_x': .5},
            on_release=self.abrir_menu_tipo
        )
        self.add_widget(self.btn_tipo)

        # Campo de Data
        self.data_texto = "2026-03-23" # Data padrão para o dia de hoje
        self.btn_data = MDRaisedButton(
            text=f"Data: {self.data_texto}",
            pos_hint={'center_x': .5},
            on_release=self.show_date_picker
        )
        self.add_widget(self.btn_data)

        # Botão Salvar
        self.add_widget(MDRaisedButton(
            text="SALVAR TRANSAÇÃO",
            md_bg_color=(0, 0.7, 0.3, 1),
            pos_hint={'center_x': .5},
            size_hint_x=0.8,
            on_release=self.validar_e_salvar
        ))

    def abrir_menu_tipo(self, button):
        menu_items = [
            {"text": "Receita", "viewclass": "OneLineListItem", "on_release": lambda x="receita": self.set_tipo(x)},
            {"text": "Despesa", "viewclass": "OneLineListItem", "on_release": lambda x="despesa": self.set_tipo(x)},
        ]
        self.menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.menu.open()

    def set_tipo(self, tipo):
        self.tipo_selecionado = tipo
        self.btn_tipo.text = f"Tipo: {tipo.capitalize()}"
        self.menu.dismiss()

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        self.data_texto = str(value)
        self.btn_data.text = f"Data: {self.data_texto}"

    def validar_e_salvar(self, *args):
        try:
            v = float(self.valor.text)
            d = self.descricao.text
            
            if not d:
                Snackbar(text="Por favor, preencha a descrição").open()
                return

            # Salvando no banco de dados blindado
            salvar_transacao(
                valor=v,
                descricao=d,
                categoria="Geral",
                tipo=self.tipo_selecionado,
                data=self.data_texto
            )

            # Limpa campos e avisa
            self.valor.text = ""
            self.descricao.text = ""
            Snackbar(text="✅ Salvo com sucesso!").open()
            
            # Avisa o dashboard para atualizar os números
            self.atualizar_dashboard()
            
        except ValueError:
            Snackbar(text="⚠️ Erro: Valor inválido").open()
