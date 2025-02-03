#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int commend_line_checker(int count, string a[]);
int ciphering(char lc[], char uc[], char t, int l, int r, int k);


int main(int argc, char* key[])
{
    const int arry_start = 0;
    const int alph = 26;
    char lower_case[alph];
    char upper_case[alph];
    int step;
    step = commend_line_checker(argc, key);
    if (step < 0)
    {
        return 1;
    }

    for (int i = 0; i < alph; i++)
    {
        lower_case[i] = 'a' + i;

        upper_case[i] = 'A' + i;
    }

    char *plaintext = get_string("Enter a plaintext: ");
    int n = strlen(plaintext);
    printf("ciphertext: ");

    for (int i = 0; i < n; i++)
    {
        ciphering(lower_case, upper_case, plaintext[i], arry_start, alph - 1, step);
    }
    printf("\n");
}

int ciphering(char lc[], char uc[], char t, int l, int r, int k)
{
    int index;

    if (isalpha(t) && islower(t))
    {
        int mid = l + (r - l) / 2;
        if (l > r)
            return 1;
        if (lc[mid] == t)
        {
            index = mid;
            int c = (index + k) % 26;
            printf("%c", lc[c]);
            return 0;
        }
        else if (lc[mid] > t)
        {
            return ciphering(lc, uc, t, l, mid - 1, k);
        }
        else
        {
            return ciphering(lc, uc, t, mid + 1, r, k);
        }
    }
    else if (isalpha(t) && isupper(t))
    {
        int mid = l + (r - l) / 2;
        if (l > r)
            return 23;
        if (uc[mid] == t)
        {
            index = mid;
            int c = (index + k) % 26;
            printf("%c", uc[c]);
            return 0;
        }
        else if (uc[mid] > t)
        {
            return ciphering(lc, uc, t, l, mid - 1, k);
        }
        else if (uc[mid] < t)
        {
            return ciphering(lc, uc, t, mid + 1, r, k);
        }
    }

    if (isblank(t))
    {
        printf(" ");
    }
    else if (t >= '!' && t <= '@')
    {
        printf("%c", t);
    }

    return 0;
}

int commend_line_checker(int count, string a[])
{
    int key;
    if (count >= 2)
    {
        key = strlen(a[1]);
        for (int i = 0; i < key; i++)
        {
            if (isalpha(a[1][i]) || (a[1][i] >= '!' && a[1][i] <= '.'))
            {
                count++;
            }
        }
    }

    if (count != 2 || count < 2)
    {
        printf("Usage: ./caesar key\n");
        return -1;
    }
    else if (count == 2)
    {
        key = atoi(a[1]);
    }
    return key;
}
