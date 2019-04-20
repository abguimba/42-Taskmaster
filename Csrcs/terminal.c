# include <stdlib.h>
# include <termcap.h>
# include <stdio.h>
# include <termios.h>
# include <unistd.h>

int			my_putchar(int c)
{
	return (write(STDERR_FILENO, &c, 1));
	return (1);
}

int			refresh_screen(int nb)
{
	char	buf[1024];
	char	*envname;

	envname = getenv("TERM");
	tgetent(buf, envname);
	tputs(tgetstr("cl", NULL), 1, my_putchar);
	return (nb);
}
