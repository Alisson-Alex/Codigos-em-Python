def calcular_imc(peso, altura):
    """Calcula o Índice de Massa Corpórea (IMC).

    Args:
        peso (float): Peso em quilogramas.
        altura (float): Altura em metros.

    Returns:
        float: Valor do IMC ou uma mensagem de erro.
    """

    if peso <= 0:
        return "Erro: O peso informado é inválido. Deve ser maior que zero."
    elif altura <= 0:
        return "Erro: A altura informada é inválida. Deve ser maior que zero."

    try:
        imc = peso / (altura ** 2)
        return imc
    except ZeroDivisionError:
        return "Erro: A altura não pode ser zero."
    except ValueError:
        return "Erro: Valores inválidos. Certifique-se de usar números."

def classificar_imc(imc):
    """Classifica o IMC de acordo com as faixas da OMS.

    Args:
        imc (float): Valor do IMC.

    Returns:
        str: Categoria de classificação.
    """

    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    elif 30 <= imc < 34.9:
        return "Obesidade Grau I"
    elif 35 <= imc < 39.9:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III ou Mórbida"

def obter_valor_valido(mensagem):
    """Obtém um valor numérico válido do usuário.

    Args:
        mensagem (str): Mensagem a ser exibida para o usuário.

    Returns:
        float: Valor numérico válido.
    """

    while True:
        try:
            valor = float(input(mensagem))
            if valor > 0:
                return valor
            else:
                print("Valor inválido. Por favor, digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

if __name__ == "__main__":
    peso = obter_valor_valido("Digite seu peso em kg: ")
    altura = obter_valor_valido("Digite sua altura em metros: ")

    imc = calcular_imc(peso, altura)
    if isinstance(imc, str):
        print(imc)
    else:
        print(f"Seu IMC é: {imc:.2f}")
        print(f"Classificação: {classificar_imc(imc)}")