from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.nota import Nota


class INotaRepository(ABC):
    @abstractmethod
    def salvar(self, nota: Nota) -> None:
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula: str) -> List[Nota]:
        pass
