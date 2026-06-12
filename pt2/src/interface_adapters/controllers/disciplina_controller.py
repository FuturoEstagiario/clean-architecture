from src.application.use_cases.cadastrar_disciplina import CadastrarDisciplina
from src.application.use_cases.listar_disciplinas import ListarDisciplinas

class DisciplinaController:
    def __init__(self, cadastrar_disciplina_use_case: CadastrarDisciplina, listar_disciplinas_use_case: ListarDisciplinas):
        self.use_case = cadastrar_disciplina_use_case
        self.listar_use_case = listar_disciplinas_use_case

    def cadastrar(self, codigo: str, nome: str, carga_horaria: int) -> dict:
        try:
            self.use_case.executar(codigo, nome, carga_horaria)
            return {"status": "sucesso", "mensagem": f"Disciplina '{nome}' cadastrada com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        disciplinas = self.listar_use_case.executar()
        return {
            "status": "sucesso",
            "dados": [{"codigo": d.codigo, "nome": d.nome, "carga_horaria": d.carga_horaria} for d in disciplinas]
        }
