#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// void letters_checker(char *text, int *l);
// void words_checker(char *text, int *w);
// void sentences_checker(char *text, int *s);
void counting(char *text, int *letters, int *words, int *sentances);

int main(void)
{
    char *text = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentances = 0;

    counting(text, &letters, &words, &sentances);

    float L = (float) letters / (float) words * 100;
    float S = (float) sentances / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index > 1 && index < 16)
    {
        printf("Grade %i\n", index);
    }
    else
    {
        printf("Before Grade 1\n");
    }
}

void counting(char *text, int *letters, int *words, int *sentances)
{
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            *letters += 1;
        }
        else if (isblank(text[i]))
        {
            *words += 1;
        }
        else if (text[i] == '?' || text[i] == '.' || text[i] == '!')
        {
            *sentances += 1;
        }
    }
}
