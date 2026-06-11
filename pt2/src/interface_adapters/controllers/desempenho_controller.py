from src.application.use_cases.consultar_desempenho import ConsultarDesempenho
from src.interface_adapters.presenters.desempenho_presenter import DesempenhoPresenter

class DesempenhoController:
    def __init__(self, use_case: ConsultarDesempenho, presenter: DesempenhoPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def consultar_json(self, matricula: str) -> dict:
        try:
            dto = self.use_case.executar(matricula)
            return {"status": "sucesso", "dados": self.presenter.apresentar_json(dto)}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def consultar_console(self, matricula: str) -> str:
        try:
            dto = self.use_case.executar(matricula)
            return self.presenter.apresentar_console(dto)
        except ValueError as e:
            return f"Erro ao consultar desempenho: {e}"
