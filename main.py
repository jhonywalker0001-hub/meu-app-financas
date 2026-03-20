from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock # Importante para evitar travamentos em transições

# IMPORTANTE: Importar as duas funções de criação de tabela
from database import criar_tabela, criar_tabela_metas

# Importando suas classes
from dashboard import Dashboard
from transacoes import TelaTransacoes
from metas import MetasPage 

class AppFinancas(MDApp):
    def build(self):
        # 1. Garante que TODAS as tabelas existam no banco de dados ao abrir
        # O Android só permite isso agora porque o database.py usa app_storage_path()
        criar_tabela() 
        criar_tabela_metas() 
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        # Criando a estrutura principal
        root = MDScreen()
        
        from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
        
        # Criamos o componente de navegação
        self.nav = MDBottomNavigation()

        # --- Item 1: Dashboard (Início) ---
        item_dash = MDBottomNavigationItem(name='item_dash', text='Início', icon='home')
        self.dashboard = Dashboard()
        item_dash.add_widget(self.dashboard)

        # --- Item 2: Adicionar (Novo) ---
        item_add = MDBottomNavigationItem(name='item_add', text='Novo', icon='plus-circle')
        
        # Usamos a função finalizar_cadastro para atualizar dados e mudar de aba
        self.tela_transacoes = TelaTransacoes(
            atualizar_dashboard=lambda: self.finalizar_cadastro()
        )
        item_add.add_widget(self.tela_transacoes)

        # --- Item 3: Metas ---
        item_metas = MDBottomNavigationItem(name='item_metas', text='Metas', icon='target')
        self.tela_metas = MetasPage()
        item_metas.add_widget(self.tela_metas)

        # Adicionando os itens ao menu
        self.nav.add_widget(item_dash)
        self.nav.add_widget(item_add)
        self.nav.add_widget(item_metas)
        
        root.add_widget(self.nav)
        return root

    def finalizar_cadastro(self, *args):
        """Atualiza os dados em todas as telas e volta para o Início com um pequeno delay."""
        # 1. Atualiza o gráfico e a lista do Dashboard
        self.dashboard.atualizar()
        
        # 2. Atualiza as barras de progresso na tela de Metas
        if hasattr(self.tela_metas, 'atualizar_lista_metas'):
            self.tela_metas.atualizar_lista_metas()
        
        # 3. Volta para a aba de Início (usando Clock para evitar crash no Android)
        Clock.schedule_once(lambda dt: self.nav.switch_tab('item_dash'), 0.2)

if __name__ == "__main__":
    AppFinancas().run()