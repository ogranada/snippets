/*
 * Copyright (c) 2009 Sebastian Wiesner <lunaryorn@gmail.com>
 *
 * This program is free software. It comes without any warranty, to
 * the extent permitted by applicable law. You can redistribute it
 * and/or modify it under the terms of the Do What The Fuck You Want
 * To Public License, Version 2, as published by Sam Hocevar. See
 * http://sam.zoy.org/wtfpl/COPYING for more details.
 */

#include <termios.h>
#include <stdio.h>
#include <unistd.h>

int getch () {
    int ch;
    struct termios tc_attrib_old;
    struct termios tc_attrib_raw;

    if (tcgetattr(STDIN_FILENO, &tc_attrib_old))
        return -1;

    tc_attrib_raw = tc_attrib_old;
    cfmakeraw(&tc_attrib_raw);

    if (tcsetattr(STDIN_FILENO, TCSANOW, &tc_attrib_raw))
        return -1;

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &tc_attrib_old);
    return ch;
}


int main(void) {
    printf("Enter a character: ");
    fflush(stdout);
    int input = getch();
    printf("\n");
    if (!input) {
        fprintf(stderr, "Could not read character");
        return 1;
    } else {
        printf("Read character '%c'\n", input);
        printf("Enter a character: ");
        fflush(stdout);
        input = getchar();
        printf("Read character '%c'\n", input);
        return 0;
    }
}
