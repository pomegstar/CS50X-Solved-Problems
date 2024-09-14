#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");

    if (card == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    bool found_jpg = false;
    int jpg_count = 0;
    uint8_t buffer[BLOCK_SIZE];
    char jpg_name[8];
    FILE *output = NULL;

    while (fread(buffer, BLOCK_SIZE, 1, card) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (found_jpg)
            {
                fclose(output);
            }
            else
            {
                found_jpg = true;
            }
            sprintf(jpg_name, "%03d.jpg", jpg_count);
            output = fopen(jpg_name, "w");
            if (output == NULL)
            {
                fclose(card);
                printf("Could not create %s.\n", jpg_name);
                return 3;
            }
            jpg_count++;
        }
        if (found_jpg)
        {
            fwrite(buffer, BLOCK_SIZE, 1, output);
        }
    }
    fclose(card);
    if (found_jpg)
    {
        fclose(output);
    }
    return 0;
}
