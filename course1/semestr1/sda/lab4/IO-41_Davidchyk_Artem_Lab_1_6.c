#include <stdio.h>
#include <windows.h>

void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

int main() {

    int rows = 24;
    int cols = 80;

    int col_num = 0;

    while (1) {

        for (int i = 0; i < rows; i++) {

            gotoxy(col_num, rows-1-i);
            printf("*");
            Sleep(100);

            gotoxy(cols-1-col_num, i);
            printf("*");
            Sleep(100);

        }

        col_num++;

        if (col_num == cols / 2) break;

        for (int i = 0; i < rows; i++) {

            gotoxy(col_num, i);
            printf("*");
            Sleep(100);

            gotoxy(cols-1-col_num, rows-1-i);
            printf("*");
            Sleep(100);

        }

        col_num++;

        if (col_num == cols / 2) break;

    }

    return 0;

}