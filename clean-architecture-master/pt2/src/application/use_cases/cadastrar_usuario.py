from src.domain.entities.usuario import Usuario
from src.application.repositories.usuario_repository import IUsuarioRepository

class CadastrarUsuario:
    def __init__(self, repository: IUsuarioRepository):
        self.repository = repository

    def executar(self, login: str, nome: str, senha: str, perfil: str) -> Usuario:
        if self.repository.buscar_por_login(login) is not None:
            raise ValueError(f"Usuário com login '{login}' já existe.")
        usuario = Usuario(login, nome, perfil)
        usuario.definir_senha(senha)
        self.repository.salvar(usuario)
        return usuario
