#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>
#include "buffer.h"



#define MAX 40
#define Buffer_Limit 100



pthread_mutex_t the_mutex;
pthread_cond_t condc, condp;




void* producer(void* ptr){
    Buffer* buf = (Buffer*)ptr;
    int p = 50;
    int tam = 4;
    int i;
    printf("produtor!");
    for(i=0;i<MAX;i++){
        pthread_mutex_lock(&the_mutex); ///obtem acesso exclusivo ao buffer
        while(!buffer_cabe(buf,tam))
            pthread_cond_wait(&condp, &the_mutex);

        buffer_insere(buf, (int)&p, tam); ///poe item no buffer
        pthread_cond_signal(&condc);///acorda o consumidor
        pthread_mutex_unlock(&the_mutex);///libera o acesso ao buffer

    }
    pthread_exit(0);
}



void* consumer(void*ptr){
	Buffer* buf = (Buffer*)ptr;
    int p = 50;
    int tam = 4;
    int i;
    printf("Consumidor!");
    for(i=0;i<MAX;i++){
        pthread_mutex_lock(&the_mutex);
        while(buffer_cabe(buf, tam))
            pthread_cond_wait(&condc, &the_mutex);

        tam = buffer_remove(buf,(int)&p, tam);
        pthread_cond_signal(&condp);
        pthread_mutex_unlock(&the_mutex);
    }
    pthread_exit(0);
}



int main(){

    ///Cria um buffer com espaço de bufferlimite
    int bufferlimite = Buffer_Limit;
    Buffer* buf = buffer_cria(bufferlimite);

    pthread_t pro, con;
    pthread_mutex_init(&the_mutex, 0);

    pthread_cond_init(&condc, 0);
    pthread_cond_init(&condp, 0);

    pthread_create(&con, 0, consumer, (void*)buf);
    pthread_create(&pro, 0, producer, (void*)buf);

    pthread_join(pro, 0);
    pthread_join(con, 0);

    pthread_cond_destroy(&condc);
    pthread_cond_destroy(&condp);

    pthread_mutex_destroy(&the_mutex);

    return 0;


}
