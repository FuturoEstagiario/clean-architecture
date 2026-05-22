import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "academico.db")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def inicializar() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            matricula TEXT PRIMARY KEY,
            nome      TEXT NOT NULL,
            situacao  TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_matricula TEXT    NOT NULL,
            disciplina      TEXT    NOT NULL,
            valor           REAL    NOT NULL
        )
    """)
    conn.commit()
    conn.close()
