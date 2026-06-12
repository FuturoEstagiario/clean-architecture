from src.application.use_cases.cadastrar_aluno import CadastrarAluno
from src.application.use_cases.listar_alunos import ListarAlunos
from src.interface_adapters.presenters.aluno_lista_presenter import AlunoListaPresenter

class AlunoController:
    def __init__(
        self,
        cadastrar_aluno_use_case: CadastrarAluno,
        listar_alunos_use_case: ListarAlunos,
        presenter: AlunoListaPresenter,
    ):
        self.cadastrar_use_case = cadastrar_aluno_use_case
        self.listar_use_case = listar_alunos_use_case
        self.presenter = presenter

    def cadastrar(self, matricula: str, nome: str) -> dict:
        try:
            self.cadastrar_use_case.executar(matricula, nome)
            return {"status": "sucesso", "mensagem": f"Aluno '{nome}' cadastrado com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        try:
            dtos = self.listar_use_case.executar()
            return {"status": "sucesso", "dados": self.presenter.apresentar_lista(dtos)}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
