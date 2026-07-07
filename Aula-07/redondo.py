"""Módulo para cálculo da área de um círculo.

Este script solicita o raio de um círculo ao usuário, valida a entrada
e calcula a área correspondente utilizando o módulo math.
"""

import math

def calcular_area_circulo(raio):
    """Calcula a área de um círculo a partir do raio fornecido.

    Args:
        raio (float): O raio do círculo. Deve ser um valor maior ou igual a zero.

    Returns:
        float: A área calculada do círculo.

    Raises:
        ValueError: Se o raio for negativo.
    """
    if raio < 0:
        raise ValueError("O raio não pode ser negativo.")
    # Calculando a área usando a fórmula: area = pi * r²
    return math.pi * (raio ** 2)

def main():
    """Função principal que gerencia o fluxo de entrada, processamento e saída."""
    # O bloco try-except garante que o programa não quebre caso o usuário digite um valor não numérico
    # ou caso ocorra um erro de validação (como raio negativo).
    try:
        # Solicitando o valor do raio ao usuário
        raio = float(input("Digite o valor do raio do círculo: "))
        
        # Calculando a área usando a função
        area = calcular_area_circulo(raio)
        
        # Imprimindo o resultado
        print(f"A área do círculo com raio {raio} é: {area}")
    except ValueError as e:
        # Trata especificamente o erro de raio negativo ou erro de conversão para float
        if str(e) == "O raio não pode ser negativo.":
            print(f"Erro: {e}")
        else:
            print("Erro: Entrada inválida. Por favor, digite um número para o raio.")

if __name__ == "__main__":
    main()

