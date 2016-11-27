#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

char *key = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB";
char *xmmword_F54E70 = "\x7\xde\xbd\x66\x4c\xe7\x5b\xa3\x92\x60\x56\xc0\x4c\x3b\xe9\xe2\x9e\x5f\x6b\xcc\xcd\x4e\x6c\xa4\xf5\x5\x0\xfa\xfa\x24\x5b\x6";

int crypt_file_data(int a1, unsigned int a2);

int     main(void)
{
    int fd;
    char *data;
    fd = open("test.jpg.adk", O_RDONLY);

    data = malloc(45287 + 2);
    read(fd, data, 45287);
    crypt_file_data(data, 45287);
    return 0;
}

int crypt_file_data(int a1, unsigned int a2)
{
    unsigned char v2; // bl@1
    unsigned int v3; // edi@1
    unsigned int v4; // eax@1
    unsigned int v5; // esi@3
    char v6; // dl@4
    char *v7; // ecx@4
    int result; // eax@4
    unsigned char v9; // bh@5
    unsigned int v10; // esi@5
    char *v11; // edx@6
    char v12; // bl@6
    unsigned char v13; // al@6
    char *v14; // ecx@6
    int v15; // [sp+Ch] [bp-10Ch]@1
    unsigned char v16; // [sp+13h] [bp-105h]@1
    char v17[256]; // [sp+14h] [bp-104h]@2

    v2 = 0;
    v15 = a1;
    v3 = a2;
    v16 = 0;
    v4 = 0;
    do
    {
        v17[v4] = v4;
        ++v4;
    }
    while ( v4 < 0x100 );
    v5 = 0;
    do
    {
        v6 = v17[v5];
        v2 += v6 + xmmword_F54E70[v5 & 0x1F];
        v7 = &v17[v2];
        result = (unsigned char)*v7;
        v17[v5++] = result;
        *v7 = v6;
    }
    while ( v5 < 0x100 );
    v9 = 0;
    v10 = 0;
    if ( v3 )
    {
        do
        {
            ++v9;
            v11 = &v17[v9];
            v12 = *v11;
            v13 = *v11 + v16;
            v16 = v13;
            v14 = &v17[v13];
            *v11 = *v14;
            *v14 = v12;
            result = (unsigned char)v17[(unsigned char)(v12 + *v11)];
            *(char *)(v15 + v10++) ^= result;
        }
        while ( v10 < v3 );
    }
    int fd = open("flag.jpg", O_WRONLY, O_TRUNC | O_CREAT);
    write(fd, v15, a2);
    return result;
}

// flag is: ECW{6a9ce34bc683978fc40e18e4a6f308f7}
