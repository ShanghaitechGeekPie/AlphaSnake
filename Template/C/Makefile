CC = gcc

AlphaSnakeIO: AlphaSnake.c AlphaSnakeIO.h AlphaSnakeIO.o
	$(CC) -O2 -o AlphaSnake AlphaSnake.c AlphaSnakeIO.o -lm

AlphaSnakeIO.o: AlphaSnakeIO.c
	$(CC) -O2 -o AlphaSnakeIO.o AlphaSnakeIO.c -c -lm

clean:
	rm -f *.o AlphaSnake
