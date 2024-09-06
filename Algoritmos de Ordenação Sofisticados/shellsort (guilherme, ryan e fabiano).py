import random

def shell_sort(vetor):
    """
    Função que implementa o algoritmo Shell Sort para ordenar um vetor.
    
    Parâmetros:
    vetor (list): Lista de elementos a serem ordenados.
    
    Retorna:
    tuple: Vetor ordenado e o número total de trocas realizadas.
    """
    n = len(vetor)
    k = 3
    h = 1
    trocas = 0

    # Definindo a distância inicial (gap)
    while h <= n:
        h = k * h + 1

    # Realizando o Shell Sort
    while h != 1:
        h = h // k

        # Percorrendo os elementos do vetor a partir da distância h
        for idChave in range(h, n):
            chaveAtual = vetor[idChave]
            i = idChave - h

            # Comparando e trocando elementos
            while i >= 0 and vetor[i] > chaveAtual:
                vetor[i + h] = vetor[i]
                i -= h
                trocas += 1
            
            vetor[i + h] = chaveAtual

    return vetor, trocas

def shell_sort_visualizado(vetor):
    """
    Função que implementa o algoritmo Shell Sort para ordenar um vetor com visualização passo a passo.
    3
    Parâmetros:
    vetor (list): Lista de elementos a serem ordenados.
    
    Retorna:
    list: Vetor ordenado.
    """
    n = len(vetor)
    k = 3
    h = 1
    trocas = 0

    # Definindo a distância inicial (gap)
    while h <= n:
        h = k * h + 1

    print(f"Distância inicial (h): {h}")

    # Realizando o Shell Sort
    while h != 1:
        h = h // k
        print(f"\nAtualizando a distância (h): {h}")

        for idChave in range(h, n):
            chaveAtual = vetor[idChave]
            i = idChave - h
            print(f"\nComparando vetor[{i}] ({vetor[i]}) com chaveAtual ({chaveAtual})")

            while i >= 0 and vetor[i] > chaveAtual:
                print(f"Troca: vetor[{i}] ({vetor[i]}) com vetor[{i + h}] ({vetor[i + h]})")
                print_vetor(vetor, i, i + h)  # Imprime o vetor antes da troca
                vetor[i + h] = vetor[i]
                i -= h
                trocas += 1
                print_vetor(vetor, i + h, i)  # Imprime o vetor depois da troca
            
            vetor[i + h] = chaveAtual
            print_vetor(vetor, i + h, idChave)  # Imprime o vetor com chaveAtual no lugar certo

            input("Pressione Enter para continuar...")

    print(f"\nTotal de trocas realizadas: {trocas}")
    return vetor

def print_vetor(vetor, pos1, pos2):
    """
    Função que imprime o vetor destacando duas posições.
    
    Parâmetros:
    vetor (list): Lista de elementos a serem impressos.
    pos1 (int): Primeira posição a ser destacada.
    pos2 (int): Segunda posição a ser destacada.
    """
    for i, valor in enumerate(vetor):
        if i == pos1 or i == pos2:
            print(f"[{valor}]", end=" ")
        else:
            print(valor, end=" ")
    print()

def obter_vetor_personalizado():
    """
    Função que permite ao usuário inserir um vetor personalizado.
    
    Retorna:
    list: Lista de elementos inseridos pelo usuário.
    """
    vetor = []
    print("Digite os números do vetor, separados por espaços:")
    entrada = input()
    vetor = list(map(int, entrada.split()))
    return vetor

def menu():
    """
    Função que exibe o menu interativo para o usuário.
    """
    while True:
        print("\nEscolha uma opção:")
        print("1. Ordenar um vetor aleatório de 100.000 elementos")
        print("2. Inserir um vetor personalizado para ordenar")
        print("3. Visualizar passo a passo a ordenação de um vetor aleatório de 10 elementos")
        print("4. Sair")
        opcao = input("Opção: ")

        if opcao == '1':
            vetor = [random.randint(0, 1000000) for _ in range(100000)]
            vetor_ordenado, trocas = shell_sort(vetor)
            print("Vetor ordenado com sucesso!")
            print(f"Total de trocas realizadas: {trocas}")
            print("\nDeseja visualizar o vetor completo ou apenas uma parte?")
            print("1. Completo")
            print("2. Primeiros 100 elementos")
            opcao_visualizacao = input("Opção: ")
            if opcao_visualizacao == '1':
                print(vetor_ordenado)
            elif opcao_visualizacao == '2':
                print(vetor_ordenado[:100])

        elif opcao == '2':
            vetor = obter_vetor_personalizado()
            vetor_ordenado, trocas = shell_sort(vetor)
            print("Vetor ordenado: ", vetor_ordenado)
            print(f"Total de trocas realizadas: {trocas}")

        elif opcao == '3':
            vetor = [random.randint(0, 100) for _ in range(10)]
            print("Vetor inicial: ", vetor)
            print("Visualizando a ordenação...")
            shell_sort_visualizado(vetor)
            print("Vetor ordenado: ", vetor)

        elif opcao == '4':
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executando o menu interativo
menu()
