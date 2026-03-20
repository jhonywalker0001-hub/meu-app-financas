from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from database import adicionar_transacao
from datetime import datetime

class TelaTransacoes(MDBoxLayout):
    def __init__(self, atualizar_dashboard, **kwargs):
        super().__init__(orientation="vertical", padding=30, spacing=15, **kwargs)
        self.atualizar_dashboard = atualizar_dashboard
        self.tipo_atual = "receita" # Começa como receita por padrão

        self.add_widget(MDLabel(
            text="Nova Movimentação", 
            font_style="H4", 
            halign="center", 
            bold=True
        ))

        # 1. CAMPO DE VALOR
        self.valor = MDTextField(
            hint_text="Valor (R$)",
            helper_text="Digite o valor da transação",
            helper_text_mode="on_focus",
            input_filter="float",
            mode="rectangle",
            icon_left="currency-usd"
        )
        self.add_widget(self.valor)

        # 2. SELETOR DE TIPO (Dois botões lado a lado)
        layout_botoes = MDBoxLayout(adaptive_height=True, spacing=10)
        
        self.btn_receita = MDFillRoundFlatButton(
            text="RECEITA",
            size_hint=(0.5, None),
            md_bg_color=(0, 0.6, 0.4, 1), # Verde ativo
            on_release=lambda x: self.mudar_tipo("receita")
        )
        
        self.btn_despesa = MDFillRoundFlatButton(
            text="DESPESA",
            size_hint=(0.5, None),
            md_bg_color=(0.2, 0.2, 0.2, 1), # Cinza inativo
            on_release=lambda x: self.mudar_tipo("despesa")
        )
        
        layout_botoes.add_widget(self.btn_receita)
        layout_botoes.add_widget(self.btn_despesa)
        self.add_widget(layout_botoes)

        # 3. BOTÃO DE CATEGORIA (Muda de cor conforme o tipo)
        self.categoria_selecionada = "Salário"
        self.btn_cat = MDRaisedButton(
            text="Categoria: Salário",
            size_hint=(1, None),
            md_bg_color=(0, 0.6, 0.4, 1), # Inicia verde
            on_release=self.abrir_menu_categorias
        )
        self.add_widget(self.btn_cat)

        # 4. BOTÃO SALVAR
        self.add_widget(MDFillRoundFlatButton(
            text="SALVAR NO BANCO",
            size_hint=(1, None),
            md_bg_color=(0, 0.7, 0.3, 1),
            on_release=self.salvar
        ))

    def mudar_tipo(self, tipo):
        """Troca visualmente entre os botões e atualiza as cores."""
        self.tipo_atual = tipo
        if tipo == "receita":
            # Cores para Receita
            self.btn_receita.md_bg_color = (0, 0.6, 0.4, 1) # Verde
            self.btn_despesa.md_bg_color = (0.2, 0.2, 0.2, 1) # Cinza
            self.btn_cat.md_bg_color = (0, 0.6, 0.4, 1) # Botão categoria fica verde
            self.categoria_selecionada = "Salário"
        else:
            # Cores para Despesa
            self.btn_receita.md_bg_color = (0.2, 0.2, 0.2, 1) # Cinza
            self.btn_despesa.md_bg_color = (0.8, 0.2, 0.2, 1) # Vermelho
            self.btn_cat.md_bg_color = (0.8, 0.2, 0.2, 1) # Botão categoria fica vermelho
            self.categoria_selecionada = "Alimentação"
        
        self.btn_cat.text = f"Categoria: {self.categoria_selecionada}"

    def abrir_menu_categorias(self, button):
        """Mostra as opções dependendo do tipo selecionado."""
        if self.tipo_atual == "receita":
            opcoes = ["Salário", "Entrada Extra", "Investimento", "Outros"]
        else:
            opcoes = ["Alimentação", "Transporte", "Lazer", "Casa", "Saúde", "Outros"]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": cat,
                "on_release": lambda x=cat: self.definir_categoria(x),
            } for cat in opcoes
        ]
        self.menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.menu.open()

    def definir_categoria(self, cat):
        self.categoria_selecionada = cat
        self.btn_cat.text = f"Categoria: {cat}"
        self.menu.dismiss()

    def salvar(self, *args):
        if not self.valor.text:
            Snackbar(text="Por favor, digite um valor!").open()
            return
        
        try:
            valor_float = float(self.valor.text)
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            
            # Salva no banco
            adicionar_transacao(
                self.tipo_atual, 
                valor_float, 
                self.categoria_selecionada, 
                self.categoria_selecionada, 
                data_hoje
            )
            
            # Limpa tudo e avisa
            self.valor.text = ""
            Snackbar(text=f"{self.tipo_atual.capitalize()} registrada!").open()
            
            # Atualiza as outras telas (Dashboard e Metas)
            self.atualizar_dashboard()
            
        except ValueError:
            Snackbar(text="Valor inválido!").open()