from src.application.use_cases.cadastrar_professor import CadastrarProfessor
from src.application.use_cases.listar_professores import ListarProfessores
from src.interface_adapters.presenters.professor_presenter import ProfessorListaPresenter

class ProfessorController:
    def __init__(
        self,
        cadastrar_use_case: CadastrarProfessor,
        listar_use_case: ListarProfessores,
        presenter: ProfessorListaPresenter,
    ):
        self.cadastrar_use_case = cadastrar_use_case
        self.listar_use_case = listar_use_case
        self.presenter = presenter

    def cadastrar(self, matricula_funcional: str, nome: str, email: str) -> dict:
        try:
            self.cadastrar_use_case.executar(matricula_funcional, nome, email)
            return {"status": "sucesso", "mensagem": f"Professor '{nome}' cadastrado com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        try:
            dtos = self.listar_use_case.executar()
            return {"status": "sucesso", "dados": self.presenter.apresentar_lista(dtos)}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
