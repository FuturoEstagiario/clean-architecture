from typing import List
from src.application.dtos.professor_dto import ProfessorResumoDTO

class ProfessorListaPresenter:
    def apresentar_lista(self, dtos: List[ProfessorResumoDTO]) -> list:
        return [
            {"matricula_funcional": dto.matricula_funcional, "nome": dto.nome, "email": dto.email}
            for dto in dtos
        ]
