#include<stdio.h>
#include<math.h>
#include<cs50.h>
#include <string.h>
#include <stdlib.h>
int main(void)
{


    int count = 0;
    printf("Konnichiwa! How much change is owed?\n");
     float val = get_float();
    //1,5,10,25
    int chng =  round(100*(val));
   // printf("%d\n",chng);
    if(chng>=25)
    {
        count  = count +(int)(chng/25);
        chng = chng%25;
        // printf("25:%d\t%d\n",count,chng);
    }
    if(chng>=10)
    {
        count  =count + (int)(chng/10);
        chng = chng%10;
       // printf("10:%d\t%d\n",count,chng);
    }
    if(chng>=5)
    {
        count  = count +(int)(chng/5);
        chng = chng%5;
       // printf("5:%d\t%d\n",count,chng);
    }
    if(chng>=1)
    {
        count  = count +(int)(chng/1);
        chng = chng%1;
       // printf("1:%d\t%d\n",count,chng);
    }

    printf("%d",count);

}

