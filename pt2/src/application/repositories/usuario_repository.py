from abc import ABC, abstractmethod
from src.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def buscar_por_login(self, login: str) -> Usuario | None:
        pass
