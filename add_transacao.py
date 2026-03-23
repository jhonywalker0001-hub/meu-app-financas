from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from database import adicionar_transacao
from datetime import datetime

class AddTransacao(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = "receita" # Valor padrão

    def set_tipo(self, tipo):
        self.tipo = tipo
        # Atualiza o texto do botão na interface se necessário
        self.ids.btn_tipo.text = f"Tipo: {tipo.capitalize()}"

    def salvar(self, *args):
        # Captura os dados usando os IDs definidos no seu arquivo .kv
        valor_texto = self.ids.campo_valor.text
        descricao = self.ids.campo_desc.text
        categoria = self.ids.campo_categoria.text
        data_hoje = datetime.now().strftime("%Y-%m-%d")

        if not valor_texto:
            Snackbar(text="Por favor, insira um valor!").open()
            return

        try:
            # Envia todos os dados para a função do banco de dados
            adicionar_transacao(
                tipo=self.tipo, 
                valor=float(valor_texto), 
                descricao=descricao if descricao else "Sem descrição",
                categoria=categoria if categoria else "Geral",
                data=data_hoje
            )

            # Limpa os campos após salvar
            self.ids.campo_valor.text = ""
            self.ids.campo_desc.text = ""
            self.ids.campo_categoria.text = ""
            
            Snackbar(text="Transação salva com sucesso!").open()
            
            # Se tiver uma referência ao dashboard, atualize-o aqui
            # self.dashboard.atualizar()

        except Exception as e:
            Snackbar(text=f"Erro ao salvar: {e}").open()
