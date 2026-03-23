from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from kivy.utils import platform

# Importando as funções do seu banco de dados
from database import calcular_saldo, resumo_transacoes, listar_transacoes, deletar_transacao

class Dashboard(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        # Card de Saldo
        self.card = MDCard(
            orientation="vertical", 
            padding=20, 
            size_hint=(1, None),
            height="140dp", 
            radius=[20], 
            md_bg_color=(0.12, 0.12, 0.18, 1)
        )
        
        self.card.add_widget(MDLabel(
            text="SALDO ATUAL", 
            theme_text_color="Hint", 
            font_style="Overline"
        ))
        
        self.label_saldo = MDLabel(
            text="R$ 0,00", 
            halign="center", 
            font_style="H4", 
            theme_text_color="Custom", 
            bold=True
        )
        
        self.card.add_widget(self.label_saldo)
        self.add_widget(self.card)

        # Resumo de Receitas/Despesas
        self.resumo = MDLabel(
            text="", 
            halign="center", 
            theme_text_color="Hint", 
            size_hint_y=None, 
            height="40dp"
        )
        self.add_widget(self.resumo)

        # Histórico com Scroll
        self.scroll = ScrollView()
        self.lista = MDList()
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        # Agenda a primeira atualização para garantir que o banco já foi criado no main.py
        Clock.schedule_once(self.atualizar, 0.5)

    def atualizar(self, *args):
        """Atualiza o saldo e a lista de transações na interface."""
        try:
            saldo = calcular_saldo()
            rec, desp = resumo_transacoes()
            
            # Formatação de moeda brasileira (R$ 1.234,56)
            texto_saldo = f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.label_saldo.text = texto_saldo
            
            # Muda a cor baseado no saldo (Verde para positivo, Vermelho para negativo)
            self.label_saldo.text_color = (0, 0.8, 0.4, 1) if saldo >= 0 else (1, 0.3, 0.3, 1)
            
            self.resumo.text = f"Ganhos: R$ {rec:,.2f}  |  Gastos: R$ {desp:,.2f}"
            self.carregar_transacoes()
        except Exception as e:
            print(f"Erro ao atualizar Dashboard: {e}")

    def carregar_transacoes(self):
        """Limpa e recarrega a lista de transações do banco de dados."""
        self.lista.clear_widgets()
        try:
            transacoes = listar_transacoes()
            for t in transacoes:
                # O parâmetro id_t=t["id"] no lambda é vital para não deletar sempre o último item
                item = TwoLineAvatarIconListItem(
                    text=t["descricao"],
                    secondary_text=f"{t['data']} | R$ {t['valor']:,.2f}",
                    on_release=lambda x, id_t=t["id"]: self.confirmar_delecao(id_t)
                )
                
                # Cor do ícone: Verde para receita, Vermelho para despesa
                cor = (0, 1, 0.5, 1) if t["tipo"].lower() == "receita" else (1, 0.3, 0.3, 1)
                item.add_widget(IconLeftWidget(
                    icon="circle", 
                    theme_text_color="Custom", 
                    text_color=cor
                ))
                
                self.lista.add_widget(item)
        except Exception as e:
            print(f"Erro ao carregar transações: {e}")

    def confirmar_delecao(self, id_t):
        """Deleta a transação e atualiza a tela."""
        deletar_transacao(id_t)
        self.atualizar()
        Snackbar(text="Transação removida").open()
