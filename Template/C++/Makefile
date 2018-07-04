CXX = g++

AlphaSnakeIO: AlphaSnake.cpp AlphaSnakeIO.h AlphaSnakeIO.o
	$(CXX) -O2 -o AlphaSnake AlphaSnake.cpp AlphaSnakeIO.o -lm

AlphaSnakeIO.o: AlphaSnakeIO.cpp
	$(CXX) -O2 -c -lm -o AlphaSnakeIO.o AlphaSnakeIO.cpp

clean:
	rm -f *.o AlphaSnake
