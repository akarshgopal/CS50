/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include<stdio.h>
#include "helpers.h"
#define SIZE 65536
/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    int f=0;
    int l=n-1;

   while(1){

        int m = (f+l)/2;
       // printf("m:%d %d %d %d %d ",m,f,l, values[m], value);
        if(values[m]==value)
        {
            return true;
        }

        else if(values[m]<value && m+1<=l)
        {

            f=m+1;
            //printf("check2 f: %d",f);
        }

        else if(values[m]>value && m-1>=f)
        {
            //printf("check3 l: %d",l);
            l=m-1;
        }
        else
            return false;


    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int count[SIZE];

    for(int i=0;i<SIZE;i++)
    {
        count[i]=0;
    }

    for(int i=0;i<n;i++)
    {
        count[values[i]]=count[values[i]]+1;

    }

    int j=0;
    for(int i=0;i<n;i++)
    {
        //printf("\ncount[j]: %d ",count[j]);
        while(!count[j])
        {
            //printf("j in loop 1: %d\t",j);
            j=j+1;
        }
        while(count[j])
        {
            //printf("j in loop 2: %d\t",j);
            values[i]=j;
            i=i+1;
            count[j]=count[j]-1;
            j=j+1;
        }
    }

     for(int i=0;i<n;i++)
    {
        printf("%d",values[i]);
    }


    return;
}
