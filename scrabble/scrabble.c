#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>

int POINTS[] = { 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int computer_score(char *word);

int main(void)
{
    char *player1 = get_string("Player 1: ");
    char *player2 = get_string("Player 2: ");

    int score1 = computer_score(player1);
    int score2 = computer_score(player2);

    if( score1 > score2)
    {
        printf("Player 1 Wins!");
    }else if(score2 > score1)
    {
        printf("Player 2 Wins!\n");
    }else
    {
        printf("Tie\n");
    }


}

int computer_score(char *word)
{
    int score = 0;

    for(int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
            score += POINTS[word[i] - 'A'];

        if (islower(word[i]))
            score += POINTS[word[i] - 'a'];
    }

    return score;
}
