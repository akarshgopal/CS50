#include<stdio.h>
#include<cs50.h>
int main(void)
{
    int size =  -1;
    while(size<0 || size>23)
    {
        printf("Height:");
        size = get_int();
    }
    for(int i=1; i<=size; i+=1)
    {
        for(int j=size-i-1;j>=0;j-=1)
            printf(" ");
        for(int k=0;k<=i;k+=1)
            printf("#");
        printf("\n");
    }
}