#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE_BIG 100000
#define SIZE_SMALL 15

// Função para ordenar o vetor usando o algoritmo Selection Sort
void selectionSort(int arr[], int n, int print) {
    int i, j, k, min_idx;
    for (i = 0; i < n - 1; i++) { // Loop para percorrer todo o vetor
        min_idx = i; // Assume o indice como menor valor
        for (j = i + 1; j < n; j++) { // Loop para encontrar o menor elemento restante
            if (arr[j] < arr[min_idx]) { // Se encontrar um elemento menor
                min_idx = j; // Atualiza o indice do menor elemento
            }
        }
        // Troca o menor elemento encontrado com o primeiro elemento não ordenado
        int temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;

        if (print == 1) {
            // Printa o passo a passo
            printf("\n");
            printf("Passo %d: ", i + 1);
            for (k = 0; k < n; k++) {
                printf("%d ", arr[k]);
            }
            printf("\n");
        }
    }
}

// Função para ordenar o vetor usando o algoritmo Insertion Sort
void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

// Função para exibir os elementos do vetor
void printArray(int arr[], int n) {
    int i;
    printf("\n");
    for (i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
}

int main() {
    int choice, i;
    do {
        printf("\nMenu:\n");
        printf("1. Mostrar o tempo de execucao do Selection Sort e do Insertion Sort para um vetor grande\n");
        printf("2. Mostrar o passo a passo do Selection Sort para um vetor pequeno\n");
        printf("3. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &choice);

        int arr[SIZE_BIG];
        srand(time(NULL));
        for (i = 0; i < SIZE_BIG; i++) {
            arr[i] = rand() % 1000;
        }

        int arr_copy_selection[SIZE_BIG];
        int arr_copy_insertion[SIZE_BIG];

        for (i = 0; i < SIZE_BIG; i++) {
            arr_copy_selection[i] = arr[i];
            arr_copy_insertion[i] = arr[i];
        }

        switch (choice) {
            case 1: {
            	printf("\n\n\n");

            	printArray(arr_copy_selection, SIZE_BIG);
                clock_t start_selection = clock();
                selectionSort(arr_copy_selection, SIZE_BIG, 0);
                clock_t end_selection = clock();
                printf("Ordenando...\n");

				///
                printf("\n\n\n");
			    system("pause"); // Aguarda o usuário pressionar Enter
			    printf("Continuando...\n");
				printArray(arr_copy_selection, SIZE_BIG);
				///

                double time_taken_selection = ((double)(end_selection - start_selection)) / CLOCKS_PER_SEC;
                printf("Tempo de execucao do Selection Sort: %.5f segundos\n", time_taken_selection);

                clock_t start_insertion = clock();
                insertionSort(arr_copy_insertion, SIZE_BIG);
                clock_t end_insertion = clock();

                double time_taken_insertion = ((double)(end_insertion - start_insertion)) / CLOCKS_PER_SEC;
                printf("Tempo de execucao do Insertion Sort: %.5f segundos\n", time_taken_insertion);

                break;
            }
            case 2: {
                int arr2[SIZE_SMALL];
                srand(time(NULL));
                printf("Vetor original:\n");
                for (i = 0; i < SIZE_SMALL; i++) {
                    arr2[i] = rand() % 100;
                    printf("%d ", arr2[i]);
                }
                printf("\n");

                selectionSort(arr2, SIZE_SMALL, 1);

                printf("Vetor ordenado:\n");
                printArray(arr2, SIZE_SMALL);

                break;
            }
            case 3:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida! Tente novamente.\n");
        }
    } while (choice != 3);

    return 0;
}

