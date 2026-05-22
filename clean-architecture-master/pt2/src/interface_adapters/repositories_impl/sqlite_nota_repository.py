from typing import List
from src.application.repositories.nota_repository import INotaRepository
from src.domain.entities.nota import Nota
from src.infrastructure.database.database import get_connection


class SQLiteNotaRepository(INotaRepository):
    def salvar(self, nota: Nota) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notas (aluno_matricula, disciplina, valor) VALUES (?, ?, ?)",
            (nota.aluno_matricula, nota.disciplina, nota.valor),
        )
        conn.commit()
        conn.close()

    def buscar_por_matricula(self, matricula: str) -> List[Nota]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina, valor FROM notas WHERE aluno_matricula = ?",
            (matricula,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [Nota(row[0], row[1], row[2]) for row in rows]
