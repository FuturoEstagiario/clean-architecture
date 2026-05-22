import os
from flask import Flask, render_template
from src.infrastructure.database.database import inicializar
from src.interface_adapters.controllers.aluno_controller import aluno_bp
from src.interface_adapters.controllers.nota_controller import nota_bp

_template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def create_app() -> Flask:
    app = Flask(__name__, template_folder=_template_dir)

    inicializar()

    app.register_blueprint(aluno_bp)
    app.register_blueprint(nota_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/cadastrar-aluno")
    def pagina_cadastrar_aluno():
        return render_template("cadastrar_aluno.html")

    @app.route("/lancar-nota")
    def pagina_lancar_nota():
        return render_template("lancar_nota.html")

    @app.route("/consultar-desempenho")
    def pagina_consultar_desempenho():
        return render_template("consultar_desempenho.html")

    return app
