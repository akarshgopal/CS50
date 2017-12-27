#include<stdio.h>
#include<cs50.h>
int main(void)
{

  printf("Please enter number of minutes:");
   int minutes = get_int();
  //scanf("%d",&minutes);
  int bottles = minutes*12;
  printf("%d\n",bottles);

}