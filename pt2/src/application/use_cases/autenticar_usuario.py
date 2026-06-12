from src.domain.entities.usuario import Usuario
from src.application.repositories.usuario_repository import IUsuarioRepository
from src.application.services.password_hasher import IPasswordHasher

class AutenticarUsuario:
    def __init__(self, usuario_repository: IUsuarioRepository, password_hasher: IPasswordHasher):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher

    def executar(self, login: str, senha: str) -> Usuario:
        usuario = self.usuario_repository.buscar_por_login(login)
        if usuario is None or not self.password_hasher.verificar(senha, usuario.senha_hash):
            raise ValueError("Login ou senha inválidos.")
        return usuario
