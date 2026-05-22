from abc import ABC, abstractmethod
from src.domain.entities.aluno import Aluno


class IAlunoRepository(ABC):
    @abstractmethod
    def salvar(self, aluno: Aluno) -> None:
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula: str):
        pass