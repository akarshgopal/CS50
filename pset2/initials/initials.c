#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include <string.h>
#include <stdlib.h>
int main(void)
{
    char *name = get_string();
    char initials[15];
    int i = 0;
    //printf("%s",name);
    int j=0;
    while(name[i] && name !=NULL)
    {
        if((i==0 && name[0]!=' ') || (name[i-1]==' ' && name[i]!=' '))
        {
            initials[j] = name[i];
            initials[j] = toupper(initials[j]);
            //if(initials[j]>='a' && initials[j]<='z')
            //    initials[j] = (initials[j] - 32 );
            printf("%c",initials[j]);
            j++;
        }
        i++;
    }
    printf("\n");
}