from src.application.repositories.aluno_repository import IAlunoRepository
from src.application.repositories.matricula_repository import IMatriculaRepository
from src.application.repositories.nota_repository import INotaRepository
from src.application.repositories.frequencia_repository import IFrequenciaRepository
from src.application.repositories.disciplina_repository import IDisciplinaRepository
from src.application.dtos.desempenho_dto import DesempenhoDTO, DisciplinaDesempenhoDTO

class ConsultarDesempenho:
    def __init__(self, 
                 aluno_repository: IAlunoRepository, 
                 matricula_repository: IMatriculaRepository, 
                 nota_repository: INotaRepository, 
                 frequencia_repository: IFrequenciaRepository,
                 disciplina_repository: IDisciplinaRepository):
        self.aluno_repository = aluno_repository
        self.matricula_repository = matricula_repository
        self.nota_repository = nota_repository
        self.frequencia_repository = frequencia_repository
        self.disciplina_repository = disciplina_repository

    def executar(self, aluno_matricula: str) -> DesempenhoDTO:
        aluno = self.aluno_repository.buscar_por_matricula(aluno_matricula)
        if aluno is None:
            raise ValueError(f"Aluno com matrícula {aluno_matricula} não encontrado.")

        # Buscar matrículas do aluno para saber em quais disciplinas ele está inscrito
        matriculas = self.matricula_repository.listar_por_aluno(aluno_matricula)
        
        disciplinas_desempenho = []
        
        for matricula in matriculas:
            # Buscar informações da disciplina
            disc = self.disciplina_repository.buscar_por_codigo(matricula.disciplina_codigo)
            if disc is None:
                continue
                
            # Buscar notas para este aluno nesta disciplina
            notas = self.nota_repository.buscar_por_aluno_e_disciplina(aluno_matricula, matricula.disciplina_codigo)
            valores_notas = [n.valor for n in notas]
            media = sum(valores_notas) / len(valores_notas) if valores_notas else 0.0
            
            # Buscar frequência para este aluno nesta disciplina
            freq = self.frequencia_repository.buscar_por_aluno_e_disciplina(aluno_matricula, matricula.disciplina_codigo)
            if freq:
                aulas_presente = freq.aulas_presente
                aulas_total = freq.aulas_total
                percentual_f = freq.percentual
            else:
                aulas_presente = 0
                aulas_total = 0
                percentual_f = 100.0
                
            disciplina_dto = DisciplinaDesempenhoDTO(
                disciplina_codigo=disc.codigo,
                disciplina_nome=disc.nome,
                notas=valores_notas,
                media=media,
                aulas_presente=aulas_presente,
                aulas_total=aulas_total,
                percentual_frequencia=percentual_f
            )
            disciplinas_desempenho.append(disciplina_dto)
            
        return DesempenhoDTO(
            aluno_matricula=aluno.matricula,
            aluno_nome=aluno.nome,
            aluno_situacao=aluno.situacao,
            disciplinas=disciplinas_desempenho
        )
