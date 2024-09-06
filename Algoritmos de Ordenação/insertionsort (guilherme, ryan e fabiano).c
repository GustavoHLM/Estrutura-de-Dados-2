//bibliotecas ultilizadas
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_NUMEROS 100000 //definindo o tamanho maximo do vetor 

void pausar() {
    getchar();
}

//funçao que imprime os vetores
void imprimirVetor(int vetor[], int tamanho) {
    for (int i = 0; i < tamanho; i++)
        printf("%d ", vetor[i]);
    printf("\n");
}

//funçao que realiza a ordenaçao
void insertionSort(int vetor[], int tamanho, int mostrar) {

    int i, aux, j;

    for (i = 1; i < tamanho; i++) {//da esquerda para direira ate achar um menor 

        aux = vetor[i];
        j = i-1;
        
        while (j >= 0 && vetor[j] > aux) {//ao achar ele percorre da direita para esquerda ate ordenar 

            vetor[j + 1] = vetor[j];
            j--;
            
            /*if (mostrar) { //if apenas para mostrar o passo a passo 
                printf("\n");pausar();
                printf("aux=%d \n", aux);
                imprimirVetor(vetor, tamanho);
            }*/

        }

        vetor[j+1] = aux;
    }
}


//funçao de geraçao do vetor com numeros aleatorios
void GeraVetor(int vetor[], int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        vetor[i] = rand() % MAX_NUMEROS; //rand e a funçao de geraçao em si
    }
}


int main() {//funçao principal

    int opcao;
    int *vetor;//declarado como ponteiro para alocaçao dinamica 

    srand(time(NULL)); // Inicializa o gerador de números aleatórios

    printf("Escolha uma opção:\n");
    printf("1. Inserir vetor manualmente.\n");
    printf("2. Gerar vetor com 100.000 números aleatórios.\n");
    
    scanf("%d", &opcao);

    if (opcao == 1) {
        
        int tamanho;
        printf("Insira o tamanho do vetor: ");
        scanf("%d", &tamanho);

        vetor = (int *)malloc(tamanho * sizeof(int));//aloca exatamente a memoria necessário

        printf("Insira %d elementos no vetor:\n", tamanho);
        for (int i = 0; i < tamanho; i++) {
            scanf("%d", &vetor[i]);
        }

        insertionSort(vetor, tamanho, 1);

        printf("Vetor ordenado:\n");
        imprimirVetor(vetor, tamanho);

    } else if (opcao == 2) {

        vetor = (int *)malloc(MAX_NUMEROS * sizeof(int));

        GeraVetor(vetor, MAX_NUMEROS);

        printf("Vetor original (primeiros n elementos):\n");
        imprimirVetor(vetor, 200); // Mostra apenas os primeiros n para facilitar a visualização

        insertionSort(vetor, MAX_NUMEROS, 0);

        printf("Vetor ordenado (primeiros n elementos):\n");
        imprimirVetor(vetor, 200); // Mostra apenas os primeiros n para facilitar a visualização

    } else {

        printf("Opção inválida!\n");

    }

    free(vetor);

    return 0;
}
