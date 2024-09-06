import random

def mergeSort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista)
    if(fim - inicio > 1):
        meio = (fim + inicio)//2
        mergeSort(lista, inicio, meio)
        mergeSort(lista, meio, fim)
        merge(lista, inicio, meio, fim)
        
def merge(lista, inicio, meio, fim):
    left = lista[inicio:meio]
    right = lista[meio:fim]
    top_left, top_right = 0, 0
    for k in range(inicio, fim):
        if top_left >= len(left):
            lista[k] = right[top_right]
            top_right = top_right+1
        elif top_right >= len(right):
            lista[k] = left[top_left]
            top_left = top_left + 1
        elif left[top_left] < right[top_right]:
            lista[k] = left[top_left]
            top_left = top_left + 1
        else:
            lista[k] = right[top_right]
            top_right = top_right + 1
            

numeros_aleatoris = random.sample(range(1, 1000), 100)

numeros_ordenados = [1, 2, 3, 4, 5, 6, 9, 20, 22, 23, 28, 
                    32, 34, 39, 40, 42, 76, 87, 99, 112]

numeros_inverso = [117, 90, 88, 83, 81, 77, 74, 69, 64, 63, 51,
            50, 49, 42, 41, 34, 32, 29, 28, 22, 16, 8, 6, 5, 3, 1]

numeros_repetidos = [7, 7, 7, 7, 7, 1, 1, 9, 9, 0, 4, 4, 4, 5, 4, 5, 7, 1,]

if __name__ == "__main__":
    test_cases = {'Números aleatórios': numeros_aleatoris, 
                    'Já ordenados': numeros_ordenados, 
                    'Ordem inversa': numeros_inverso, 
                    'Elementos repetidos': numeros_repetidos
                }
    print("*******************************")
    for name, lista in test_cases.items():
        print("*****************Caso de teste*****************\n {}".format(name))
        print(lista)
        mergeSort(lista)
        print("\n Ordenado:")
        print(lista)
    print("*******************************")