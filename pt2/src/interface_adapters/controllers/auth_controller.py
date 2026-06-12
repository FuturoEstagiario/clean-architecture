from src.application.use_cases.autenticar_usuario import AutenticarUsuario

class AuthController:
    def __init__(self, autenticar_usuario_use_case: AutenticarUsuario):
        self.use_case = autenticar_usuario_use_case

    def autenticar(self, login: str, senha: str) -> dict:
        try:
            usuario = self.use_case.executar(login, senha)
            return {"status": "sucesso", "dados": {"login": usuario.login, "perfil": usuario.perfil}}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}
