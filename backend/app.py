import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.conversion import conversion_bp
from utils.file_handler import cleanup_temp, ensure_temp_dir

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurar CORS - permitir todas as origens
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Garantir headers CORS em todas as respostas (incluindo erros)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

# Registrar blueprints
app.register_blueprint(conversion_bp)

# Inicializar diretórios
ensure_temp_dir()

# Servir arquivos estáticos do frontend (build do Vite)
@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('static', path)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

@app.before_request
def before_request():
    """Executar antes de cada request."""
    # Cleanup movido para job periódico - não rodar a cada request
    pass

# Periodic cleanup job
def start_cleanup_scheduler():
    import threading
    import time

    def cleanup_loop():
        while True:
            time.sleep(3600)  # Run every hour
            cleanup_temp()

    thread = threading.Thread(target=cleanup_loop, daemon=True)
    thread.start()

if __name__ == '__main__':
    # Iniciar scheduler de limpeza
    start_cleanup_scheduler()

    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
