from flask import Flask, request, jsonify
import subprocess
import os
import re

app = Flask(__name__)

SECRET_TOKEN = "1234"

SCRIPT_DIR = "/app/scripts"

@app.route('/executar-script', methods=['POST'])
def executar_script():

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'erro': 'Token não fornecido ou inválido'}), 401

    token = auth_header.split(" ")[1]
    if token != SECRET_TOKEN:
        return jsonify({'erro': 'Token inválido'}), 403

    # Lê o JSON
    data = request.get_json()
    script_key = data.get('script') if data else None

    if not script_key:
        return jsonify({'erro': 'Parâmetro "script" é obrigatório'}), 400

    # Segurança: permitir apenas letras, números, hífen e underline
    if not re.fullmatch(r'[\w\-]+', script_key):
        return jsonify({'erro': 'Nome de script inválido'}), 400

    # Concatena extensão .sh
    script_name = f"{script_key}.sh"
    script_path = os.path.join(SCRIPT_DIR, script_name)

    if not os.path.exists(script_path):
        return jsonify({'erro': f'Script "{script_name}" não encontrado'}), 404

    try:
        resultado = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            check=True
        )

        return jsonify({
            'mensagem': f'Script "{script_name}" executado com sucesso',
            'saida': resultado.stdout
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            'erro': f'Erro ao executar o script "{script_name}"',
            'saida': e.output,
            'erro_detalhado': e.stderr
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
