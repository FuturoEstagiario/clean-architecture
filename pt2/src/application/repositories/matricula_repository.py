from abc import ABC, abstractmethod
from src.domain.entities.matricula import Matricula

class IMatriculaRepository(ABC):
    @abstractmethod
    def salvar(self, matricula: Matricula) -> None:
        pass

    @abstractmethod
    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> Matricula | None:
        pass

    @abstractmethod
    def listar_por_aluno(self, aluno_matricula: str) -> list[Matricula]:
        pass
