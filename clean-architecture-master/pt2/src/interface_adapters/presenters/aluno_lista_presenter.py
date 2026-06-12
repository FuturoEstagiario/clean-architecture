from typing import List
from src.application.dtos.aluno_dto import AlunoResumoDTO

class AlunoListaPresenter:
    def apresentar_lista(self, dtos: List[AlunoResumoDTO]) -> list:
        return [
            {"matricula": dto.matricula, "nome": dto.nome, "situacao": dto.situacao}
            for dto in dtos
        ]
