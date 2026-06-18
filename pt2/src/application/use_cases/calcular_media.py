from src.application.repositories.aluno_repository import IAlunoRepository
from src.application.repositories.disciplina_repository import IDisciplinaRepository
from src.application.repositories.matricula_repository import IMatriculaRepository
from src.application.repositories.nota_repository import INotaRepository
from src.application.dtos.media_dto import MediaDTO
from src.domain.services.criterio_aprovacao import CriterioAprovacao

class CalcularMedia:
    def __init__(
        self,
        aluno_repository: IAlunoRepository,
        disciplina_repository: IDisciplinaRepository,
        matricula_repository: IMatriculaRepository,
        nota_repository: INotaRepository,
    ):
        self.aluno_repository = aluno_repository
        self.disciplina_repository = disciplina_repository
        self.matricula_repository = matricula_repository
        self.nota_repository = nota_repository

    def executar(self, aluno_matricula: str, disciplina_codigo: str) -> MediaDTO:
        aluno = self.aluno_repository.buscar_por_matricula(aluno_matricula)
        if aluno is None:
            raise ValueError(f"Aluno com matrícula {aluno_matricula} não encontrado.")

        disciplina = self.disciplina_repository.buscar_por_codigo(disciplina_codigo)
        if disciplina is None:
            raise ValueError(f"Disciplina com código {disciplina_codigo} não encontrada.")

        matricula = self.matricula_repository.buscar_por_aluno_e_disciplina(aluno_matricula, disciplina_codigo)
        if matricula is None:
            raise ValueError(f"Aluno {aluno_matricula} não está matriculado na disciplina {disciplina_codigo}.")

        notas = self.nota_repository.buscar_por_aluno_e_disciplina(aluno_matricula, disciplina_codigo)
        if not notas:
            return MediaDTO(
                aluno_matricula=aluno.matricula,
                aluno_nome=aluno.nome,
                disciplina_codigo=disciplina.codigo,
                disciplina_nome=disciplina.nome,
                notas=[],
                media=0.0,
                status="Sem notas lançadas",
            )

        valores = [n.valor for n in notas]
        media = CriterioAprovacao.calcular_media(valores)
        status = CriterioAprovacao.situacao_nota(media)

        return MediaDTO(
            aluno_matricula=aluno.matricula,
            aluno_nome=aluno.nome,
            disciplina_codigo=disciplina.codigo,
            disciplina_nome=disciplina.nome,
            notas=valores,
            media=media,
            status=status,
        )
