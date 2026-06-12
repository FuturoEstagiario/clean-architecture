from werkzeug.security import check_password_hash, generate_password_hash
from src.application.services.password_hasher import IPasswordHasher

class WerkzeugPasswordHasher(IPasswordHasher):
    def gerar_hash(self, senha: str) -> str:
        return generate_password_hash(senha)

    def verificar(self, senha: str, senha_hash: str) -> bool:
        return check_password_hash(senha_hash, senha)
