from src.application.repositories.aluno_repository import IAlunoRepository
from src.domain.entities.aluno import Aluno
from src.infrastructure.database.database import get_connection


class SQLiteAlunoRepository(IAlunoRepository):
    def salvar(self, aluno: Aluno) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO alunos (matricula, nome, situacao) VALUES (?, ?, ?)",
            (aluno.matricula, aluno.nome, aluno.situacao),
        )
        conn.commit()
        conn.close()

    def buscar_por_matricula(self, matricula: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT matricula, nome, situacao FROM alunos WHERE matricula = ?",
            (matricula,),
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        aluno = Aluno(row[0], row[1])
        aluno.situacao = row[2]
        return aluno
