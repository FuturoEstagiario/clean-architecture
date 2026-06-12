from src.application.use_cases.cadastrar_professor import CadastrarProfessor
from src.application.use_cases.listar_professores import ListarProfessores

class ProfessorController:
    def __init__(self, cadastrar_professor_use_case: CadastrarProfessor, listar_professores_use_case: ListarProfessores):
        self.use_case = cadastrar_professor_use_case
        self.listar_use_case = listar_professores_use_case

    def cadastrar(self, registro: str, nome: str) -> dict:
        try:
            self.use_case.executar(registro, nome)
            return {"status": "sucesso", "mensagem": f"Professor '{nome}' cadastrado com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        professores = self.listar_use_case.executar()
        return {
            "status": "sucesso",
            "dados": [{"registro": p.registro, "nome": p.nome} for p in professores]
        }
