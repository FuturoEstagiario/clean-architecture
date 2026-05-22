from src.infrastructure.web.app import create_app

if __name__ == "__main__":
    app = create_app()
    print("Servidor a correr em http://127.0.0.1:5000")
    app.run(debug=True)
