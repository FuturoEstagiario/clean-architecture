class AprovacaoDTO:
    def __init__(
        self,
        aluno_matricula: str,
        aluno_nome: str,
        disciplina_codigo: str,
        disciplina_nome: str,
        media: float,
        percentual_frequencia: float,
        status: str,
    ):
        self.aluno_matricula = aluno_matricula
        self.aluno_nome = aluno_nome
        self.disciplina_codigo = disciplina_codigo
        self.disciplina_nome = disciplina_nome
        self.media = media
        self.percentual_frequencia = percentual_frequencia
        self.status = status
