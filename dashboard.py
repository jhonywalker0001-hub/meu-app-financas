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
from kivy.core.image import Image as CoreImage 
from datetime import datetime

# REMOVIDO: tkinter (Não funciona no Android)

from database import (
    calcular_saldo, resumo_transacoes, listar_transacoes, 
    deletar_transacao, exportar_para_excel, exportar_para_pdf,
    atualizar_transacao, limpar_banco_dados
)

class Dashboard(MDBoxLayout):
    # ... (O código do __init__ permanece igual)
    # [Mantendo toda a estrutura visual que você criou]

    def preparar_salvamento(self, mes_selecionado):
        self.dialog_mes.dismiss()
        try:
            # No Android, salvamos direto na pasta do App ou Downloads sem abrir janela extra
            nome_arq = f"Relatorio_{mes_selecionado.replace('/', '_')}.xlsx"
            
            # O database.py que corrigimos já sabe onde salvar no Android!
            caminho = exportar_para_excel(nome_arq, mes_selecionado)
            
            Snackbar(text=f"Relatório salvo em: {nome_arq}", bg_color=(0, 0.6, 0.3, 1)).open()
        except Exception as e:
            Snackbar(text="Erro ao exportar relatório").open()

    # ... (Restante das funções de gráfico e lista permanecem iguais)
