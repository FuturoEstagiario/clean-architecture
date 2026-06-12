from src.application.use_cases.cadastrar_usuario import CadastrarUsuario
from src.application.use_cases.autenticar_usuario import AutenticarUsuario
from src.interface_adapters.presenters.autenticacao_presenter import AutenticacaoPresenter

class AutenticacaoController:
    def __init__(
        self,
        cadastrar_use_case: CadastrarUsuario,
        autenticar_use_case: AutenticarUsuario,
        presenter: AutenticacaoPresenter,
    ):
        self.cadastrar_use_case = cadastrar_use_case
        self.autenticar_use_case = autenticar_use_case
        self.presenter = presenter

    def cadastrar(self, login: str, nome: str, senha: str, perfil: str) -> dict:
        try:
            self.cadastrar_use_case.executar(login, nome, senha, perfil)
            return {"status": "sucesso", "mensagem": f"Usuário '{login}' cadastrado com perfil '{perfil}'."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def autenticar(self, login: str, senha: str) -> dict:
        try:
            dto = self.autenticar_use_case.executar(login, senha)
            resultado = self.presenter.apresentar(dto)
            status = "sucesso" if dto.autenticado else "erro"
            return {"status": status, "dados": resultado}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
