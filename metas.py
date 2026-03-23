from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, IconLeftWidget, TwoLineAvatarListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from database import definir_meta, obter_metas, listar_transacoes

class MetasPage(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)
        
        self.scroll = ScrollView()
        self.lista_metas = MDList()
        self.scroll.add_widget(self.lista_metas)
        self.add_widget(self.scroll)
        
        Clock.schedule_once(lambda dt: self.atualizar_lista_metas())

    def atualizar_lista_metas(self, *args):
        self.lista_metas.clear_widgets()
        
        # Recupera dados do banco blindado
        metas_definidas = obter_metas()
        transacoes = listar_transacoes()
        
        categorias = ["Alimentação", "Transporte", "Lazer", "Casa", "Saúde", "Outros"]
        icones = {
            "Alimentação": "food", "Transporte": "car", 
            "Lazer": "controller-classic", "Casa": "home", 
            "Saúde": "medical-bag", "Outros": "dots-horizontal"
        }

        for cat in categorias:
            limite = metas_definidas.get(cat, 0.0)
            # Soma despesas usando a lógica do listar_transacoes
            gasto_atual = sum(t['valor'] for t in transacoes if t['categoria'] == cat and t['tipo'].lower() == 'despesa')
            
            # Alerta visual se ultrapassar o limite
            cor_icone = (1, 0.3, 0.3, 1) if gasto_atual > limite and limite > 0 else (0, 0.8, 0.4, 1)
            
            item = TwoLineAvatarListItem(
                text=f"{cat}",
                secondary_text=f"Gasto: R$ {gasto_atual:.2f} / Limite: R$ {limite:.2f}",
                on_release=lambda x, c=cat, l=limite: self.abrir_dialogo_meta(c, l)
            )
            
            icone = IconLeftWidget(
                icon=icones.get(cat, "tag"),
                theme_text_color="Custom",
                text_color=cor_icone
            )
            item.add_widget(icone)
            self.lista_metas.add_widget(item)

    def abrir_dialogo_meta(self, categoria, limite_atual):
        # Campo customizado para o diálogo
        self.campo_limite = MDTextField(
            text=str(limite_atual) if limite_atual > 0 else "", 
            hint_text=f"Definir limite para {categoria}",
            input_filter="float",
            mode="rectangle"
        )
        
        self.dialogo = MDDialog(
            title="Ajustar Meta Mensal",
            type="custom",
            content_cls=self.campo_limite,
            size_hint=(0.8, None),
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
                MDFlatButton(
                    text="DEFINIR", 
                    theme_text_color="Custom", 
                    text_color=(0, 0.8, 0.4, 1),
                    on_release=lambda x: self.salvar_meta(categoria)
                )
            ]
        )
        self.dialogo.open()

    def salvar_meta(self, categoria):
        novo_valor = self.campo_limite.text
        if novo_valor:
            try:
                definir_meta(categoria, float(novo_valor))
                self.dialogo.dismiss()
                self.atualizar_lista_metas()
                Snackbar(text=f"Meta de {categoria} atualizada!").open()
            except ValueError:
                Snackbar(text="Digite um valor numérico válido.").open()
