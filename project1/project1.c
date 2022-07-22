// sm3_str.c
#pragma comment(lib, "libssl.lib")
#pragma comment(lib, "libcrypto.lib")
#define _CRT_SECURE_NO_WARNINGS
#define HASH_RESULT_LEN 32
#define Size 3
#include <openssl/evp.h>
#include<stdio.h>
#include <string.h>

unsigned int hash_str(const char* str, const size_t len,
    unsigned char* hash_result)
{
    unsigned int ret;
    const EVP_MD* alg = EVP_sm3();
    EVP_Digest(str, len, hash_result, &ret, alg, NULL);
    return ret;
}

int main(int argc, char const* argv[])
{

    unsigned char str0[HASH_RESULT_LEN] = "20190046\0";
    unsigned char str[HASH_RESULT_LEN];
    unsigned char str1[HASH_RESULT_LEN];
    strcpy(str, str0);
    strcpy(str1, str0);
    int i = 1;
    while (1)
    {
        hash_str(str, HASH_RESULT_LEN, str);
        hash_str(str1, HASH_RESULT_LEN, str1);
        hash_str(str1, HASH_RESULT_LEN, str1);
        if (memcmp(str, str1, Size)==0)//比较内存中的字节是否相同
            break;
        i++;
    }
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", str[i]);
    }
    printf("\n");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", str1[i]);
    }
    printf("\n");
    memcpy(str1, str,HASH_RESULT_LEN);
    memcpy(str, str0,HASH_RESULT_LEN);
    for (int j = 1; j <= i; j++)
    {
        unsigned char temp[HASH_RESULT_LEN];
        unsigned char temp1[HASH_RESULT_LEN];
        hash_str(str, HASH_RESULT_LEN, temp);
        hash_str(str1, HASH_RESULT_LEN, temp1);
        if (memcmp(temp, temp1, Size)==0)
            break;
        else
        {
            hash_str(str, HASH_RESULT_LEN, str);
            hash_str(str1, HASH_RESULT_LEN, str1);
        }
    }
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", str[i]);
    }
    printf("\n");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", str1[i]);
    }
    printf("\n");
    printf("check!");
    unsigned char temp[HASH_RESULT_LEN];
    unsigned char temp1[HASH_RESULT_LEN];
    hash_str(str, HASH_RESULT_LEN, temp);
    hash_str(str1, HASH_RESULT_LEN, temp1);

    if (memcmp(temp, temp1, Size) == 0)
        printf("success!");
    return 0;
}