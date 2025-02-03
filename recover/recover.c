#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
#define BZ 512
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: recover [File Name]\n");
        return 1;
    }

    FILE *MC = fopen(argv[1], "r");

    BYTE buffer[BZ];
    int count = 0;
    FILE *image = NULL;
    char filename[8];
    bool startjpeg = false;

    while (fread(&buffer, 1, BZ, MC) == 512)
    {
        if ((buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff) &&
            ((buffer[3] & 0xf0) == 0xe0))
        {
            startjpeg = true;
        }
        if (startjpeg == true)
        {

            if (count != 0)
            {
                fclose(image);
            }

            sprintf(filename, "%03i.jpg", count);
            image = fopen(filename, "w");
            fwrite(buffer, 1, BZ, image);
            count++;
            startjpeg = false;
        }
        else if (count != 0)
        {
            fwrite(buffer, 1, BZ, image);
        }
    }

    fclose(image);
    fclose(MC);
}
