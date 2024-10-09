filmes = ["filme 1", "filme 2", "filme 3", "filme 4", "filme 5"]

filmes

while True:

    for filme in filmes:

        classificacao = (input(f" Como voce classifica '{
                         filme}' de 1 a 5? (ou '0' para parar):"))

        classificacao = int(classificacao)
        print(classificacao)


        if classificacao == 0:
            print(f" Classificacao do '{filme}' cancelada!. \n")
            break

        if classificacao < 0 or classificacao > 5:
            print("Por favor, digite uma classificação válida de 1 a 5. \n")
            break

        else:
            print(f" Voce classificou '{filme}' com {
                  classificacao} estrelas. \n")

    print("Obrigado por sua classificacao. \n")
    break
