from src.application.dtos.autenticacao_dto import AutenticacaoDTO

class AutenticacaoPresenter:
    def apresentar(self, dto: AutenticacaoDTO) -> dict:
        if not dto.autenticado:
            return {"autenticado": False, "mensagem": "Login ou senha inválidos."}
        return {
            "autenticado": True,
            "login": dto.login,
            "nome": dto.nome,
            "perfil": dto.perfil,
            "token": dto.token,
        }
