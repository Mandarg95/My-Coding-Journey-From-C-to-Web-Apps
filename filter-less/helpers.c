#include "helpers.h"
#include <math.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, blue
            int A =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.00);

            // Update pixle values
            image[i][j].rgbtRed = A;
            image[i][j].rgbtGreen = A;
            image[i][j].rgbtBlue = A;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int max_rgb = 255;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia Values
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
          int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
          int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            if(sepiaRed > max_rgb)
            {
                sepiaRed = max_rgb;
            }
            if(sepiaGreen > max_rgb)
            {
                sepiaGreen = max_rgb;
            }
            if(sepiaBlue > max_rgb)
            {
                sepiaBlue = max_rgb;
            }

            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen= sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {

            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;



        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red_A = 0, green_A = 0, blue_A = 0;
            float sum_r = 0, sum_g = 0, sum_b = 0, sum_t = 0;

            for (int r = i - 1; r < i + 2; r++)
            {
                for (int c = j - 1; c < j + 2; c++)
                {
                    if ((r < height && c < width) && (r >= 0 && c >= 0))
                    {
                    sum_r += copy[r][c].rgbtRed;
                    sum_g += copy[r][c].rgbtGreen;
                    sum_b += copy[r][c].rgbtBlue;
                    sum_t++;
                    }
                }
            }

            if (sum_r >= 0)
            {
                red_A = round(sum_r / sum_t);
            }
            if (sum_g >= 0)
            {
                green_A = round(sum_g / sum_t);
            }
            if (sum_b >= 0.)
            {
                blue_A = round(sum_b / sum_t);
            }

            image[i][j].rgbtRed = red_A;
            image[i][j].rgbtGreen = green_A;
            image[i][j].rgbtBlue = blue_A;

        }
    }
    return;
}
