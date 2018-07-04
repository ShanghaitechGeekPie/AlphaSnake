#include "AlphaSnakeIO.h"

alpha_snake_conf get_game_conf() {
  alpha_snake_conf response;
  response.map_max_x = 99;
  response.map_max_y = 99;
  response.id = 0;
  response.num = 2;
  response.start_position[0][0] = 10;
  response.start_position[0][1] = 10;
  return response;
};

alpha_snake_step_result submit_step(int step) {
  printf("[Step Submitted] %d\n", step);
  alpha_snake_step_result response;
  response.status[0] = 0;
  response.step[0] = step;
  return response;
};
