#ifndef BUFFER_H_   /* Include guard */
#define BUFFER_H_



typedef struct lista{
    int tam;
    void* info;
    struct lista* prox;
}Lista;



typedef struct buffer{
    int tam;
    int usado;
    struct lista* prim;
}Buffer;



Buffer *buffer_cria(int tam);
void buffer_destroi(Buffer* buf);
bool buffer_insere(Buffer *buf, void *info, int tam);
int buffer_remove(Buffer *buf, void *p, int tam);
bool buffer_cabe(Buffer* buf, int tam);




#endif // BUFFER_H_