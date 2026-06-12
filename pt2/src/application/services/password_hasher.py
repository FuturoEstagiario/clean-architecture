from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def gerar_hash(self, senha: str) -> str:
        pass

    @abstractmethod
    def verificar(self, senha: str, senha_hash: str) -> bool:
        pass
