from abc import ABC, abstractmethod
from src.domain.entities.disciplina import Disciplina

class IDisciplinaRepository(ABC):
    @abstractmethod
    def salvar(self, disciplina: Disciplina) -> None:
        pass

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Disciplina | None:
        pass

    @abstractmethod
    def listar(self) -> list[Disciplina]:
        pass
