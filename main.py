import os
import sys
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

# --- SISTEMA DE LOG DE EMERGÊNCIA ---
def capturar_erros():
    """Redireciona erros para um arquivo de texto no Android"""
    if platform == 'android':
        from android.storage import app_storage_path
        log_path = os.path.join(app_storage_path(), "erro_log.txt")
        sys.stderr = open(log_path, "w")
        sys.stdout = open(log_path, "w")

# Executa o log antes de qualquer outra coisa
capturar_erros()

# Importando banco de dados
from database import criar_tabela, criar_tabela_metas

# Importando suas classes
from dashboard import Dashboard
from transacoes import TelaTransacoes
from metas import MetasPage

class AppFinancas(MDApp):
    def build(self):
        # 1. Ajuste de Permissões para Android 11+
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])

        # 2. Configuração do Banco de Dados Persistente
        self.configurar_banco()
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        root = MDScreen()
        self.nav = MDBottomNavigation()

        # Item 1: Dashboard
        item_dash = MDBottomNavigationItem(name='item_dash', text='Início', icon='home')
        self.dashboard = Dashboard()
        item_dash.add_widget(self.dashboard)

        # Item 2: Adicionar
        item_add = MDBottomNavigationItem(name='item_add', text='Novo', icon='plus-circle')
        self.tela_transacoes = TelaTransacoes(
            atualizar_dashboard=lambda: self.finalizar_cadastro()
        )
        item_add.add_widget(self.tela_transacoes)

        # Item 3: Metas
        item_metas = MDBottomNavigationItem(name='item_metas', text='Metas', icon='target')
        self.tela_metas = MetasPage()
        item_metas.add_widget(self.tela_metas)

        self.nav.add_widget(item_dash)
        self.nav.add_widget(item_add)
        self.nav.add_widget(item_metas)
        
        root.add_widget(self.nav)
        return root

    def configurar_banco(self):
        """Define o local correto do banco de dados no Android"""
        if platform == 'android':
            from android.storage import app_storage_path
            os.chdir(app_storage_path()) 
            
        criar_tabela()
        criar_tabela_metas()

    def finalizar_cadastro(self, *args):
        # Atualiza os dados nas outras abas
        self.dashboard.atualizar()
        if hasattr(self.tela_metas, 'atualizar_lista_metas'):
            self.tela_metas.atualizar_lista_metas()
        
        # Volta para a tela inicial automaticamente após cadastrar
        Clock.schedule_once(lambda dt: self.nav.switch_tab('item_dash'), 0.2)

if __name__ == "__main__":
    try:
        AppFinancas().run()
    except Exception as e:
        # Se der erro fatal no PC ou Android, printa no terminal/log
        print(f"ERRO FATAL: {e}")
