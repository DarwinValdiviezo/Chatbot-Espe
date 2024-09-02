from flask import Flask

def create_app():
    app = Flask(__name__)

    # Aquí podrías añadir configuraciones adicionales si es necesario

    # Registrar rutas
    from .routes import main
    app.register_blueprint(main)

    return app
