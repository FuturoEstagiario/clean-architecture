from src.application.use_cases.calcular_media import CalcularMedia
from src.interface_adapters.presenters.media_presenter import MediaPresenter

class MediaController:
    def __init__(self, use_case: CalcularMedia, presenter: MediaPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def calcular(self, aluno_matricula: str, disciplina_codigo: str) -> dict:
        try:
            dto = self.use_case.executar(aluno_matricula, disciplina_codigo)
            return {"status": "sucesso", "dados": self.presenter.apresentar(dto)}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}
