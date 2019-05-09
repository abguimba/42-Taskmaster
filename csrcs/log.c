/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mjose <mjose@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/05/08 21:39:19 by mjose             #+#    #+#             */
/*   Updated: 2019/05/09 02:51:41 by mjose            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

typedef struct	log_stat
{
	int		fd;
	char	*job;
	char	*job_status;
	char	*jason_status;
	char	*yymmdd;
	char	*hhmmss;
}				t_log_stat;

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

int		ft_putstr_fd(char const *s, int fd)
{
	return (write(fd, s, ft_strlen(s)));
}

int		ft_putstr(char const *s)
{
	return (ft_putstr_fd(s, 1));
}

void	ft_putendl(char const *s)
{
	if (s)
		ft_putendl_fd(s, 1);
}

void	ft_putendl_fd(char const *s, int fd)
{
	if (s)
	{
		ft_putstr_fd(s, fd);
		ft_putchar_fd('\n', fd);
	}
}

void	ft_putchar_fd(char c, int fd)
{
	write(fd, &c, 1);
}

void	ft_putchar(char c)
{
	ft_putchar_fd(c, 1);
}

int		init_file(char *file, t_log_stat *inf)
{
	struct stat		inf_file;

	if (inf_file.st_mode & S_IWUSR && inf_file.st_mode & S_IFREG)
		inf->fd = open(file, O_RDWR | O_CREAT | O_APPEND);
	else
	{
		ft_putstr("TASKAMSTER: Error accessing: ");
		ft_putstr(file);
		ft_putendl("-- No READ WRITE permissions.");
		return (1);
	}
	return (0);
}

int		insert_line(t_log_stat *inf)
{
	ft_putstr_fd(inf->job, inf->fd);
	ft_putstr_fd(": has changed his status to:", inf->fd);
	ft_putstr_fd(inf->job_status, inf->fd);
	ft_putstr_fd("at: ")
}

int		insert_in_log(char *file, char *job, char *job_status, char *jason_status)
{

	t_log_stat	inf;

	inf.fd = -1;
	inf.job = job;
	inf.job_status = job_status;
	inf.jason_status = jason_status;
	if (!init_file(file, &inf))
	{
		insert_line(&inf);
	}
}

int		main(int ac, char **av)
{
	if (ac < 1)
	{
		
	}
}
