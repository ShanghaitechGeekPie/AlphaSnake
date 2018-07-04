#include <stdio.h>
#include "AlphaSnakeIO.h"

int main() {
  // Get the config of this game. call once in your program is enough.
  alpha_snake_conf conf = get_game_conf();

  // YOUR ALGORITHM

  // Submit one step and get result of this step. call it to finish one step.
  // If your program died this function will kill the program.
  // If you have no choice but die, please at lease submit one step.
  alpha_snake_step_result resault = submit_step(GoUp);

  return 0;
}
