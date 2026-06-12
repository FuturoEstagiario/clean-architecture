from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.professor import Professor

class IProfessorRepository(ABC):
    @abstractmethod
    def salvar(self, professor: Professor) -> None:
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula_funcional: str) -> Professor | None:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Professor]:
        pass
