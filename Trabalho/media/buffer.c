#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>
#include "buffer.h"


Buffer *buffer_cria(int tam){
    ///Cria um buffer de tam tamanho
    Buffer *buf = malloc(sizeof(Buffer));
    buf->tam = tam;
    buf->usado = 0;
    ///Cria uma lista de espaços do buffer
    Lista *lst = malloc(sizeof(Lista));
    lst->info = 0;
    ///buffer->prim aponta para o primeiro elemento da lista
    lst->prox = NULL;
    buf->prim = lst;
    ///retorna o ponteiro para o buffer
    return buf;
}



void buffer_destroi(Buffer* buf){
    Lista* l = buf->prim;
    Lista* aux = l;
    while(l->prox != NULL){
        aux = l;
        l = l->prox;
        free(aux->info);
        free(aux);
    }
    free(l);
    free(buf);
    printf("Destruiu o seu Buffer!!");
}



bool buffer_insere(Buffer *buf, void *info, int tam){
    ///Se não passar do tamanho do buffer
    printf("entrou no insere\n");
    if(buf->tam >= buf->usado + tam){ ///insere
        Lista* aux = buf->prim;

        while(aux->prox != NULL)
            aux = aux->prox;

        Lista* novo = malloc(sizeof(Lista));
        novo->info = malloc(tam);
        novo->info = info;
        novo->tam = tam;
        novo->prox = NULL;

        aux->prox = novo;
        buf->usado = buf->usado + tam;
        printf("Inseriu!!\n");
        return true;
    }
    ///Se passar do tamanho do buffer
    else{
        printf("Buffer Cheio!\n");
        return false;
    }
}



int buffer_remove(Buffer *buf, void *p, int tam){
    Lista* l = buf->prim;
    buf->prim = l->prox;
    char* ninfo = (char*)l->info;
    char* np = (char*)p;
    int i, j=l->tam-tam;

    for(i=j;i<l->tam;i++){
        np[j] = ninfo[i];
    }
    buf->usado = buf->usado - l->tam;
    free(l);
    return tam;
}



bool buffer_cabe(Buffer* buf, int tam){
    if(buf->tam >= buf->usado + tam){
        return true;
    }
    else
        return false;
}
