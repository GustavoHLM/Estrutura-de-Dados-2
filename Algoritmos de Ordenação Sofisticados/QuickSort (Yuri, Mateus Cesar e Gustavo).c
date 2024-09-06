#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// trocar dois elementos
void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

//  dividir o array e encontrar o  
int partitionAsc(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Fdividir o array e encontrar o pivot Decrescente
int partitionDesc(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] > pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Função principal do QuickSort crescente
void quickSortAsc(int arr[], int low, int high) {
    if (low < high) {
        int pi = partitionAsc(arr, low, high);

        quickSortAsc(arr, low, pi - 1);
        quickSortAsc(arr, pi + 1, high);
    }
}

// Função principal do QuickSort (decrescente)
void quickSortDesc(int arr[], int low, int high) {
    if (low < high) {
        int pi = partitionDesc(arr, low, high);

        quickSortDesc(arr, low, pi - 1);
        quickSortDesc(arr, pi + 1, high);
    }
}

// Função para imprimir o array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int n = 100000;
    int arr[n];
    int choice;

    //  gerador de números aleatórios
    srand(time(0));

    // Preenche o array com números aleatórios
    for (int i = 0; i < n; i++) {
        arr[i] = rand();
    }

    // Menu de escolha
    printf("Escolha o tipo de ordenação:\n");
    printf("1. Ordem Crescente\n");
    printf("2. Ordem Decrescente\n");
    printf("Sua escolha: ");
    scanf("%d", &choice);

    // Imprime o array antes da ordenação
    printf("Array antes da ordenação:\n");
    printArray(arr, n);

    // Obtém o tempo de início
    clock_t start = clock();

    // Chama o QuickSort de acordo com a escolha do usuário
    if (choice == 1) {
        quickSortAsc(arr, 0, n - 1);
    } else if (choice == 2) {
        quickSortDesc(arr, 0, n - 1);
    } else {
        printf("Escolha inválida!\n");
        return 1;
    }

    // Obtém o tempo de término
    clock_t end = clock();

    // Calcula o tempo de execução
    double time_taken = ((double) (end - start)) / CLOCKS_PER_SEC;

    // Imprime o array depois da ordenação
    printf("Array depois da ordenação:\n");
    printArray(arr, n);

    printf("QuickSort levou %f segundos para ordenar o array de %d elementos.\n", time_taken, n);

    return 0;
}