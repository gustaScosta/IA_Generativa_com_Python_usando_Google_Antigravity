"""Módulo Gerador de Senhas Seguras.

Este script fornece uma funcionalidade para gerar senhas aleatórias e seguras.
O usuário pode definir o tamanho da senha (mínimo de 8 caracteres).
O código implementa boas práticas de programação em Python, incluindo:
- Divisão em funções.
- Tratamento de exceções (try-except).
- Loop de validação de entrada (while).
- Bloco condicional de execução (if __name__ == "__main__").
"""

import secrets
import string

def gerar_senha_segura(tamanho=8):
    """Gera uma senha segura com o tamanho especificado.

    Garante que a senha gerada contenha pelo menos:
    - 1 letra maiúscula
    - 1 letra minúscula
    - 1 dígito (número)
    - 1 caractere especial (pontuação)

    Args:
        tamanho (int): O comprimento da senha. Deve ser de pelo menos 8 caracteres.

    Returns:
        str: A senha segura gerada.

    Raises:
        ValueError: Se o tamanho fornecido for menor do que 8.
    """
    # Valida se o tamanho atende aos requisitos mínimos de segurança
    if tamanho < 8:
        raise ValueError("O tamanho mínimo da senha deve ser de 8 caracteres.")
    
    # Define os conjuntos de caracteres que serão utilizados na senha
    letras_maiusculas = string.ascii_uppercase
    letras_minusculas = string.ascii_lowercase
    digitos = string.digits
    caracteres_especiais = string.punctuation
    
    # Garante a inclusão de pelo menos um caractere de cada tipo essencial na senha
    senha = [
        secrets.choice(letras_maiusculas),
        secrets.choice(letras_minusculas),
        secrets.choice(digitos),
        secrets.choice(caracteres_especiais)
    ]
    
    # Junta todos os grupos de caracteres para preencher o restante da senha
    todos_caracteres = letras_maiusculas + letras_minusculas + digitos + caracteres_especiais
    
    # Preenche as posições restantes da senha até atingir o tamanho definido
    for _ in range(tamanho - len(senha)):
        senha.append(secrets.choice(todos_caracteres))
    
    # Mistura os caracteres de forma segura para não expor a posição dos obrigatórios
    secrets.SystemRandom().shuffle(senha)
    
    # Junta a lista de caracteres em uma única string e retorna
    return "".join(senha)

def main():
    """Função principal que gerencia o fluxo de entrada e saída do programa."""
    # Loop contínuo até que o usuário digite um valor de tamanho válido
    while True:
        try:
            # Solicita o tamanho desejado da senha ao usuário
            tamanho = int(input("Digite a quantidade de caracteres para a senha (mínimo 8): "))
            
            # Verifica se o tamanho digitado é menor que o limite aceitável de 8
            if tamanho < 8:
                raise ValueError("Não é possível gerar a senha: a quantidade de caracteres deve ser de no mínimo 8.")
            
            # Se for um valor válido, quebra o loop para prosseguir com a geração
            break
        except ValueError as e:
            # Trata entradas não numéricas e erros de tamanho menor que 8
            if "Não é possível" in str(e):
                print(f"Erro: {e}\n")
            else:
                print("Erro: Entrada inválida. Por favor, digite um número inteiro.\n")

    try:
        # Chama a função para gerar a senha segura com o tamanho validado
        senha = gerar_senha_segura(tamanho)
        print("\nSenha segura gerada com sucesso!")
        print(f"Senha: {senha}")
    except Exception as e:
        # Captura eventuais erros inesperados durante a geração
        print(f"\nOcorreu um erro inesperado ao gerar a senha: {e}")

# Ponto de entrada oficial para execução do script
if __name__ == "__main__":
    main()
