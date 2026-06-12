from abc import ABC, abstractmethod
from src.domain.entities.professor import Professor

class IProfessorRepository(ABC):
    @abstractmethod
    def salvar(self, professor: Professor) -> None:
        pass

    @abstractmethod
    def buscar_por_registro(self, registro: str) -> Professor | None:
        pass

    @abstractmethod
    def listar(self) -> list[Professor]:
        pass
