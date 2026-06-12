from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.aluno import Aluno

class IAlunoRepository(ABC):
    @abstractmethod
    def salvar(self, aluno: Aluno) -> None:
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula: str) -> Aluno | None:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Aluno]:
        pass

    @abstractmethod
    def atualizar_situacao(self, matricula: str, nova_situacao: str) -> None:
        pass