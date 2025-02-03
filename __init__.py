import logging
import re
import json
import azure.functions as func

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando requisição para validação de CPF.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    cpf = req_body.get('cpf')
    if not cpf:
        return func.HttpResponse(
            json.dumps({"error": "CPF não informado"}),
            status_code=400,
            mimetype="application/json"
        )
    
    resultado = validate_cpf(cpf)
    response_data = {"cpf": cpf, "valid": resultado}
    
    return func.HttpResponse(
        json.dumps(response_data),
        status_code=200,
        mimetype="application/json"
    )
