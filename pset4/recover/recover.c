/**
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include<ctype.h>
int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    int counter=0;
    typedef unsigned char BYTE;
    BYTE block[512];
    char filename[8];
    int open=0;

    FILE *outptr = NULL ;

    while(fread(block,512,1,inptr)==1)
    {

        if(block[0]== 0xff &&
                block[1]== 0xd8 &&
                block[2] == 0xff &&
                (block[3] & 0xf0) == 0xe0)
        {
            if(open)
            {
                fclose(outptr);
                open=0;
            }

            sprintf(filename,"%03i.jpg",counter++);
            outptr = fopen(filename, "w");
            open=1;// open output file

            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;
            }

        }

        if(open)
            fwrite(block,1,512,outptr);

    }




    // close infile
    fclose(inptr);

    // close outfile


    // success
    return 0;
}
