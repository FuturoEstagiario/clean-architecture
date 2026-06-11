from abc import ABC, abstractmethod
from src.domain.entities.frequencia import Frequencia

class IFrequenciaRepository(ABC):
    @abstractmethod
    def salvar(self, frequencia: Frequencia) -> None:
        pass

    @abstractmethod
    def buscar_por_aluno(self, aluno_matricula: str) -> list[Frequencia]:
        pass

    @abstractmethod
    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> Frequencia | None:
        pass
