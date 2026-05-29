import sqlite3
import os

class SQLiteConnection:
    def __init__(self, db_path: str = "academico.db"):
        self.db_path = db_path
        self._criar_tabelas()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Habilitar chaves estrangeiras
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _criar_tabelas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                situacao TEXT NOT NULL
            );
        """)
        
        # Disciplinas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                codigo TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL
            );
        """)
        
        # Matriculas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                aluno_matricula TEXT NOT NULL,
                disciplina_codigo TEXT NOT NULL,
                PRIMARY KEY (aluno_matricula, disciplina_codigo),
                FOREIGN KEY (aluno_matricula) REFERENCES alunos(matricula) ON DELETE CASCADE,
                FOREIGN KEY (disciplina_codigo) REFERENCES disciplinas(codigo) ON DELETE CASCADE
            );
        """)
        
        # Notas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_matricula TEXT NOT NULL,
                disciplina_codigo TEXT NOT NULL,
                valor REAL NOT NULL,
                tipo_avaliacao TEXT NOT NULL,
                FOREIGN KEY (aluno_matricula, disciplina_codigo) REFERENCES matriculas(aluno_matricula, disciplina_codigo) ON DELETE CASCADE
            );
        """)
        
        # Frequencias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS frequencias (
                aluno_matricula TEXT NOT NULL,
                disciplina_codigo TEXT NOT NULL,
                aulas_presente INTEGER NOT NULL,
                aulas_total INTEGER NOT NULL,
                PRIMARY KEY (aluno_matricula, disciplina_codigo),
                FOREIGN KEY (aluno_matricula, disciplina_codigo) REFERENCES matriculas(aluno_matricula, disciplina_codigo) ON DELETE CASCADE
            );
        """)
        
        conn.commit()
        conn.close()
