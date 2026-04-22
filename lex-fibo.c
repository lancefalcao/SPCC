%option noyywrap
%{
#include <stdio.h>
#include <stdlib.h>

/* Function to calculate and print the Fibonacci series */
void print_fibonacci(int n) {
    int a = 0, b = 1, next;
    printf("Fibonacci Series (first %d terms): ", n);
    for (int i = 1; i <= n; ++i) {
        printf("%d ", a);
        next = a + b;
        a = b;
        b = next;
    }
    printf("\n\nEnter the number of terms: ");
}
%}

/* Rules Section */
%%
[0-9]+      { 
                /* Convert matched string to integer and call the function */
                int n = atoi(yytext); 
                print_fibonacci(n); 
            }

%%

/* User Subroutines Section */
int main() {
    printf("Enter the number of terms: ");
    yylex(); /* Start lexical analysis */
    return 0;
}