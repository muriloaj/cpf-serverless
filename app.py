from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def validate_cpf(cpf: str) -> bool:
    """
    Valida um CPF.
    O CPF deve conter 11 dígitos (desconsiderando formatações como pontos e hífens).
    A função remove caracteres não numéricos, verifica o tamanho, checa se todos os dígitos
    são iguais e valida os dígitos verificadores.
    """
    # Remove qualquer caractere que não seja dígito
    cpf = re.sub(r'\D', '', cpf)
    
    # CPF precisa ter 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (ex.: '11111111111' é inválido)
    if cpf == cpf[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10) % 11
    if primeiro_digito == 10:
        primeiro_digito = 0
    if primeiro_digito != int(cpf[9]):
        return False

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10) % 11
    if segundo_digito == 10:
        segundo_digito = 0
    if segundo_digito != int(cpf[10]):
        return False

    return True

@app.route('/validate', methods=['POST'])
def validate():
    """
    Endpoint para validação de CPF.
    Espera receber um JSON com a chave "cpf".
    Retorna um JSON informando se o CPF é válido ou não.
    """
    data = request.get_json()
    if not data or 'cpf' not in data:
        return jsonify({'error': 'CPF não informado'}), 400

    cpf = data['cpf']
    resultado = validate_cpf(cpf)
    return jsonify({'cpf': cpf, 'valid': resultado}), 200

if __name__ == '__main__':
    # Em um ambiente serverless, este bloco não é necessário.
    app.run(host='0.0.0.0', port=5000, debug=True)
