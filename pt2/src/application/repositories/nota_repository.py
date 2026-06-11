from abc import ABC, abstractmethod
from src.domain.entities.nota import Nota

class INotaRepository(ABC):
    @abstractmethod
    def salvar(self, nota: Nota) -> None:
        pass

    @abstractmethod
    def buscar_por_aluno(self, aluno_matricula: str) -> list[Nota]:
        pass
        
    @abstractmethod
    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> list[Nota]:
        pass
