import os

from flask import Flask, jsonify, redirect, render_template, request, session
from src.infrastructure.di.container import Container
from src.infrastructure.web.routes.aluno_routes import aluno_bp
from src.infrastructure.web.routes.auth_routes import auth_bp
from src.infrastructure.web.routes.desempenho_routes import desempenho_bp
from src.infrastructure.web.routes.disciplina_routes import disciplina_bp
from src.infrastructure.web.routes.frequencia_routes import frequencia_bp
from src.infrastructure.web.routes.matricula_routes import matricula_bp
from src.infrastructure.web.routes.nota_routes import nota_bp
from src.infrastructure.web.routes.professor_routes import professor_bp

ROTAS_PUBLICAS = ("auth.pagina", "auth.entrar", "static")

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SGA_SECRET_KEY", "dev-secret-key-trocar-em-producao")
    app.container = Container()

    app.register_blueprint(auth_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(disciplina_bp)
    app.register_blueprint(matricula_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(frequencia_bp)
    app.register_blueprint(desempenho_bp)

    @app.before_request
    def exigir_login():
        if request.endpoint in ROTAS_PUBLICAS:
            return None
        if "usuario" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"status": "erro", "mensagem": "Autenticação necessária."}), 401
            return redirect("/login")
        return None

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    return app

def run():
    create_app().run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run()
