/**
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdlib.h>
#include<math.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize infile outfile\n");
        return 1;
    }

    // remember filenames
    float f = atof(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    RGBTRIPLE bmphex[abs(bi.biHeight)][bi.biWidth];
    printf("%d %d %d %f %d %d",bf.bfSize, bi.biSizeImage, padding, f, bi.biWidth, bi.biHeight);
     bi.biWidth = (int)(bi.biWidth*f);
     bi.biHeight = (int)(bi.biHeight*f);
    int padding2 = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = (bi.biWidth*3+padding2)*abs(bi.biHeight);
    bf.bfSize = 54 +  bi.biSizeImage ;
    printf("\t %d %d %d %f %d %d",bf.bfSize, bi.biSizeImage, padding2, f, bi.biWidth, bi.biHeight);
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    // padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    // iterate over infile's scanlines
    for (int i = 0, biHeight = (int)abs(bi.biHeight)/f; i < biHeight; i++)
    {


        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth/f; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                bmphex[i][j]=triple;
            }
         fseek(inptr, padding, SEEK_CUR); // skip over padding, if any

        }


   // printf("\t119");
    if(f>=1)
    {
        for(int i=0;i<abs(bi.biHeight)/f;i++)
        {
            for(int h=0;h<f;h++)
            {
                for(int j=0;j<bi.biWidth/f;j++)
                {
                    for(int k=0;k<f;k++)
                        fwrite(&bmphex[i][j], sizeof(RGBTRIPLE), 1, outptr);
                }
                for (int k = 0; k < padding2; k++)
                {
                    fputc(0x00, outptr);
                }
            }

        }
     }       // then add it back (to demonstrate how)

    else
    {
        for(int i=0;i<abs(bi.biHeight)/f;i+=(int)(1/f))
        {
            for(int j=0;j<bi.biWidth/f;j+=(int)(1/f))
                {
                    fwrite(&bmphex[i][j], sizeof(RGBTRIPLE), 1, outptr);
                        //for(int h=0;h<(int)(1/f);h++)
                            //for(int l=0;l<(int)(1/f);l++)
                            //{
                              //  bmphex[i][j].rgbtBlue=(unsigned char)(bmphex[i][j].rgbtBlue+bmphex[i+h][j+l].rgbtBlue*f*f);
                             //   bmphex[i][j].rgbtRed=(unsigned char)(bmphex[i][j].rgbtRed+ bmphex[i+h][j+l].rgbtRed*f*f);
                             //   bmphex[i][j].rgbtGreen=(unsigned char)(bmphex[i][j].rgbtGreen+ bmphex[i+h][j+l].rgbtGreen*f*f);
                          //}

                }
            for (int k = 0; k < padding2; k++)
                {
                    fputc(0x00, outptr);
                }
        }
    }

    /*for(int k=0;k<f;k++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }*/
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
