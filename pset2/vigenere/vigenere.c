#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include <string.h>
#include <stdlib.h>

char *vigenere(string s,string k);

int main(int argc, string argv[])
{
    if ( argc == 2 ) /* argc should be 2 for correct execution */
    {
        int n=0;
        while(argv[1][n]){
            if(!isalpha(argv[1][n++]))
            {
                exit(1);
            }

        }

        printf("plaintext:");
        char *p = get_string();
        printf("ciphertext: %s\n", vigenere(p,argv[1]));
    }
    else if(argc==1 || argc>2 )
    {
        exit(1);
    }

    else
    {

        printf( "Usage: %s k\n", argv[0] );
    }
}


string vigenere(string s,string k)
{
    char *ciphertext= s;
    int i=0;
    int j=0;
    while(s[i])
    {
        if(s[i]!=' ' && isalpha(s[i]))
        {

            if(s[i]>='a' && s[i]<='z')
            {
                ciphertext[i] = (((s[i] + (toupper(k[j])-65))) - 97)%26 + 97;
            }
            else if(s[i]>='A' && s[i]<='Z')
            {
                ciphertext[i] = (((s[i] + (toupper(k[j])-65))) - 65)%26 + 65;
            }

            j=(j+1)%strlen(k);
        }

        i++;
    }
    return ciphertext;
}