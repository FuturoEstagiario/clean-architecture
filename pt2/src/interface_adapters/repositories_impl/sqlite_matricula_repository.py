from src.domain.entities.matricula import Matricula
from src.application.repositories.matricula_repository import IMatriculaRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteMatriculaRepository(IMatriculaRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, matricula: Matricula) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO matriculas (aluno_matricula, disciplina_codigo) VALUES (?, ?)",
            (matricula.aluno_matricula, matricula.disciplina_codigo)
        )
        conn.commit()
        conn.close()

    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> Matricula | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo FROM matriculas WHERE aluno_matricula = ? AND disciplina_codigo = ?",
            (aluno_matricula, disciplina_codigo)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Matricula(row["aluno_matricula"], row["disciplina_codigo"])
        return None

    def listar_por_aluno(self, aluno_matricula: str) -> list[Matricula]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo FROM matriculas WHERE aluno_matricula = ?",
            (aluno_matricula,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [Matricula(r["aluno_matricula"], r["disciplina_codigo"]) for r in rows]

    def listar(self) -> list[Matricula]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT aluno_matricula, disciplina_codigo FROM matriculas ORDER BY aluno_matricula")
        rows = cursor.fetchall()
        conn.close()

        return [Matricula(r["aluno_matricula"], r["disciplina_codigo"]) for r in rows]
