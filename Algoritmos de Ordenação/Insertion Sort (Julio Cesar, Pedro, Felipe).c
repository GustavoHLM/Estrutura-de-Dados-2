#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Função de comparação para qsort
int rand_comparison(const void *a, const void *b) {
  return (*(int *)a - *(int *)b);
}

// Função para embaralhar o vetor
void shuffle(int *array, size_t n) {
  srand(time(NULL)); // Inicializa a semente de forma mais aleatória
  for (size_t i = n - 1; i > 0; i--) {
    size_t j = rand() % (i + 1);
    // Troca array[i] com array[j]
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

void insertion_sort(int *array, size_t n) {
  for (int i = 1; i < n; i++) {
    int key = array[i];
    int j = i - 1;

    // Enquanto j for maior ou igual a zero e o elemento anterior for maior que a chave
    while (j >= 0 && array[j] > key) {
      // Desloca o elemento para a direita
      array[j + 1] = array[j];
      j--;
    }

    // Insere a chave na posição correta
    array[j + 1] = key;
  }
}

int main() {
  const int SIZE = 100000;
  int vec1[SIZE];

  // Inicializa o vetor com números sequenciais
  for (int i = 0; i < SIZE; i++) {
    vec1[i] = i + 1;
  }

  // Embaralha o vetor
  shuffle(vec1, SIZE);

  // Imprime os elementos embaralhados
  printf("Vetor Aleatório:\n");
  for (int j = 0; j < SIZE; j++) {
    printf("%d ", vec1[j]);
  }
  printf("\n\n");

  insertion_sort(vec1, SIZE);

  // Imprime os elementos ordenados
  printf("\nVetor Ordenado:\n");
  for (int j = 0; j < SIZE; j++) {
    printf("%d ", vec1[j]);
  }
  printf("\n");


  return 0;
}

