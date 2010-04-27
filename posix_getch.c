/*
 * Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>
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
    struct termios tc_attrib;
    if (tcgetattr(STDIN_FILENO, &tc_attrib))
        return -1;

    tcflag_t lflag = tc_attrib.c_lflag;
    tc_attrib.c_lflag &= ~ICANON & ~ECHO;

    if (tcsetattr(STDIN_FILENO, TCSANOW, &tc_attrib))
        return -1;

    ch = getchar();

    tc_attrib.c_lflag = lflag;
    tcsetattr (STDIN_FILENO, TCSANOW, &tc_attrib);
    return ch;
}


int main(void) {
    printf("Enter a character: ");
    fflush(stdout);
    int input = getch();
    printf("\n");
    if (!input)
        fprintf(stderr, "Could not read character");
    else
        printf("Read character '%c'\n", input);
    return 0;
}
