import random

# Função para transformar um array em um heap
def heapify(arr, n, i):
    largest = i  # Inicializa o maior como raiz
    left = 2 * i + 1  # Filho à esquerda
    right = 2 * i + 2  # Filho à direita

    # Verifica se o filho à esquerda é maior que a raiz
    if left < n and arr[i] < arr[left]:
        largest = left

    # Verifica se o filho à direita é maior que o maior até agora
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Se o maior não for a raiz
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Troca

        # Heapify a raiz
        heapify(arr, n, largest)

# Função principal para realizar o heap sort
def heap_sort(arr):
    n = len(arr)

    # Constrói o heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extrai os elementos um por um
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Troca
        heapify(arr, i, 0)

# Gera uma lista de 100.000 elementos aleatórios
arr = [random.randint(0, 1000000) for _ in range(100000)]

# Salva todos os elementos antes de serem ordenados
with open(r"C:\Users\tubin\OneDrive\Documentos\Codigos\Seminarios de ED II\Seminario 3 - Heap Sort\unsorted_elements.txt", "w") as file:
    for element in arr:
        file.write(f"{element}\n")

# Realiza a ordenação
heap_sort(arr)

# Salva todos os elementos ordenados em um arquivo
with open(r"C:\Users\tubin\OneDrive\Documentos\Codigos\Seminarios de ED II\Seminario 3 - Heap Sort\sorted_elements.txt", "w") as file:
    for element in arr:
        file.write(f"{element}\n")
