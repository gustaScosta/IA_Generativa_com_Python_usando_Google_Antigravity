"""Módulo para geração de senhas seguras.

Este script gera uma senha aleatória segura de tamanho fixo de 8 caracteres,
garantindo a presença de letras maiúsculas, minúsculas, números e caracteres especiais.
"""

import secrets
import string

def gerar_senha_segura():
    """Gera uma senha segura com tamanho fixo de 8 caracteres.

    Garante que a senha gerada contenha pelo menos:
    - 1 letra maiúscula
    - 1 letra minúscula
    - 1 dígito (número)
    - 1 caractere especial (pontuação)

    Returns:
        str: A senha segura gerada de 8 caracteres.
    """
    tamanho = 8
    
    # Definindo os grupos de caracteres
    letras_maiusculas = string.ascii_uppercase
    letras_minusculas = string.ascii_lowercase
    digitos = string.digits
    caracteres_especiais = string.punctuation
    
    # Garantindo pelo menos um caractere de cada grupo essencial
    senha = [
        secrets.choice(letras_maiusculas),
        secrets.choice(letras_minusculas),
        secrets.choice(digitos),
        secrets.choice(caracteres_especiais)
    ]
    
    # Todos os caracteres possíveis para completar o tamanho restante da senha
    todos_caracteres = letras_maiusculas + letras_minusculas + digitos + caracteres_especiais
    
    # Preenche o restante da senha (mais 4 caracteres para totalizar 8)
    for _ in range(tamanho - len(senha)):
        senha.append(secrets.choice(todos_caracteres))
    
    # Mistura os caracteres de forma segura para que a posição dos obrigatórios seja aleatória
    secrets.SystemRandom().shuffle(senha)
    
    return "".join(senha)

def main():
    """Função principal que gera e exibe a senha gerada para o usuário."""
    try:
        senha = gerar_senha_segura()
        print("Senha segura gerada com sucesso!")
        print(f"Senha: {senha}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao gerar a senha: {e}")

if __name__ == "__main__":
    main()
