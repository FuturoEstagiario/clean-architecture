import uuid
from src.application.repositories.usuario_repository import IUsuarioRepository
from src.application.dtos.autenticacao_dto import AutenticacaoDTO

class AutenticarUsuario:
    def __init__(self, repository: IUsuarioRepository):
        self.repository = repository

    def executar(self, login: str, senha: str) -> AutenticacaoDTO:
        usuario = self.repository.buscar_por_login(login)
        if usuario is None or not usuario.verificar_senha(senha):
            return AutenticacaoDTO(login=login, nome="", perfil="", autenticado=False)
        return AutenticacaoDTO(
            login=usuario.login,
            nome=usuario.nome,
            perfil=usuario.perfil,
            autenticado=True,
            token=str(uuid.uuid4()),
        )
