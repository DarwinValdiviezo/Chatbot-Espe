import os
from app import create_app

# Configurar la variable de entorno para evitar conflictos con OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
