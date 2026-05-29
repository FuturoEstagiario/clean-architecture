from src.domain.entities.disciplina import Disciplina
from src.application.repositories.disciplina_repository import IDisciplinaRepository

class CadastrarDisciplina:
    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def executar(self, codigo: str, nome: str, carga_horaria: int) -> Disciplina:
        if self.repository.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Disciplina com código {codigo} já cadastrada.")
            
        nova_disciplina = Disciplina(codigo, nome, carga_horaria)
        self.repository.salvar(nova_disciplina)
        print(f"Disciplina '{nome}' cadastrada com sucesso!")
        return nova_disciplina
