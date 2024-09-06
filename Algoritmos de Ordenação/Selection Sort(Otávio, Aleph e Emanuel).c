//Alunos: Aleph, Emanuel e Otávio
//Bibliotecas Utilizadas:
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
//constante global do tamanho do vetor:
#define N 100000

//Funcao que gera numeros aleatorios (0~100000):
int numRand() {
    return rand() % 100000;
}

//Funcao de Ordenacao Selection Sort:
void selectionSort(int v[]){
	int i, j, min, temp;
	for (i=0; i<N; i++){
		min=i;
		for (j=i+1; j<N; j++){
			if (v[j] <v[min]){
				min=j;
			}	
		}
		if (i!=min){
			temp= v[min];
			v[min]=v[i];
			v[i]=temp;
		} 
	}
}//fim do selectionSort()


void main(){
    srand(time(NULL));//Funcao que iniciliza a funcao rand().

    int  v[N];
    int i = 0;
    
    for (i=0; i<N; i++){
        v[i] = numRand();
    }

    for (i=0; i<N; i++) {
        printf("%d ", v[i]);
    }
    printf("\nVetor Aleatorio entre 0 e 99999 (Nao ordenado)\n\n");
    
    selectionSort(v);//chamada da funcao de ordenacao
    
    for (i=0; i<N; i++) {
        printf("%d ", v[i]);
    }
    printf("\nVetor Aleatorio Ordenado\n");
    
}//fim do main()
