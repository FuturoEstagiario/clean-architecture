from src.application.dtos.aprovacao_dto import AprovacaoDTO

class AprovacaoPresenter:
    def apresentar(self, dto: AprovacaoDTO) -> dict:
        return {
            "aluno": {
                "matricula": dto.aluno_matricula,
                "nome": dto.aluno_nome,
            },
            "disciplina": {
                "codigo": dto.disciplina_codigo,
                "nome": dto.disciplina_nome,
            },
            "resultado": {
                "media": round(dto.media, 2),
                "frequencia_percentual": f"{dto.percentual_frequencia:.1f}%",
                "status": dto.status,
                "media_minima": 6.0,
                "frequencia_minima": "75.0%",
            },
        }
