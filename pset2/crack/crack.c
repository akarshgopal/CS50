#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include <string.h>
#include <stdlib.h>
#define _XOPEN_SOURCE
#include <unistd.h>
#include<crypt.h>
#define PSWDSIZE 4

char *crack(string salt,string hash);

//char check[PSWDSIZE]="\n";
char dict[] = "\0\0\0\0";




int main(int argc, string argv[])
{
    if ( argc == 2 ) /* argc should be 2 for correct execution */
    {
        char *salt ="50";
        printf("%s\n",crack(salt,argv[1]));
    }


    else
    {
        printf( "Usage: %s hash\n", argv[0] );
        exit(1);
    }
    return 0;
}



char *crack(string salt,string hash)
{
    int l=0;
    int k=0;
    int j=0;
    for(int i=0;i<53;i++)
    {
        if(i==0)
            dict[3]='\0';
        if(i>0 && i<27)
            dict[3] = (char)(i+64);
        if(i>26)
            dict[3] = (char)(i+70);

        for(j=0;j<53;j++)
        {
            if(i==0 && j==0)
                    dict[2]='\0';
            if(j>0 && j<27)
                dict[2]= (char)(j+64);
            if(j>26)
                dict[2] = (char)(j+70);

            for(k=0;k<53;k++)
            {
                if(k==0 && j==0 && i==0)
                    dict[1]='\0';
                if(k>0 && k<27)
                    dict[1]= (char)(k+64);
                if(k>26)
                    dict[1] = (char)(k+70);

                for(l=0;l<52;l++)
                {

                    if(l>=0 && l<26)
                        dict[0] = (char)(l+65);
                    if(l>25)
                        dict[0] = (char)(l+71);

                    char *crypt1 = crypt(dict,salt);
                    //printf("%s ",dict);

                    if(strcmp(hash,crypt1)==0)
                        {
                            return dict;
                        }
                }
            }
        }
    }




    return "Failed to Crack";
}


