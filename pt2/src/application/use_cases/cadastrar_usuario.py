from src.domain.entities.usuario import Usuario
from src.application.repositories.usuario_repository import IUsuarioRepository
from src.application.services.password_hasher import IPasswordHasher

class CadastrarUsuario:
    def __init__(self, usuario_repository: IUsuarioRepository, password_hasher: IPasswordHasher):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher

    def executar(self, login: str, senha: str, perfil: str):
        if not senha or len(senha) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        if self.usuario_repository.buscar_por_login(login) is not None:
            raise ValueError(f"O login '{login}' já está em uso.")

        usuario = Usuario(login, self.password_hasher.gerar_hash(senha), perfil)
        self.usuario_repository.salvar(usuario)
