# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abe <abe@student.42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/02/26 17:04:04 by abe               #+#    #+#              #
#    Updated: 2019/04/20 21:08:31 by abe              ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

DEF =           \033[0m
GRA =           \033[1m
SOU =           \033[4m
BLI =           \033[5m
BLA =           \033[30m
RED =           \033[31m
GRE =           \033[32m
YEL =           \033[33m
BLU =           \033[34m
PUR =           \033[35m
CYA =           \033[36m
WHI =           \033[37m

C_DIR = Csrcs/

C_SRC = $(C_DIR)terminal.c

NAME = taskmaster

CC = gcc

SRCP := $(addprefix $(C_DIR)/, $(C_SRC))

LIBPATH = Pysrcs/libCtaskmaster.so

TERMLIB := termcap

FLAGS := -Wall -Wextra -Werror -fPIC -shared

all: $(NAME)

$(NAME):
		@$(CC) $(FLAGS) -o $(LIBPATH) -l $(TERMLIB) $(C_SRC)
		@echo "$(GRE)C Library and put in Pysrcs folder!$(DEF)"

clean:
		@rm -f $(LIBPATH)

.PHONY: clean all