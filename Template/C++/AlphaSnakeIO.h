#ifndef ALPHASNAKE_H_
#define ALPHASNAKE_H_

#include <cstdio>

#define GoUndefined -1  // only for player died
#define GoUp 0
#define GoRight 1
#define GoDown 2
#define GoLeft 3

typedef struct alpha_snake_conf alpha_snake_conf;

typedef struct alpha_snake_step_result alpha_snake_step_result;

/* The config of this game.
*/
struct alpha_snake_conf
{
	int map_max_x;  // maximum x (start from 0)
	int map_max_y;  // maximum y (start from 0)
	int num; // the number of all players
  int id; // id of this player (start from 0)
  int start_position[4][2]; // list of start points of all players (in this order (x, y))
};

/* The result of this step.
*/
struct alpha_snake_step_result
{
  int status[4];
  int step[4];
};

/* get the config of this game.
*/
alpha_snake_conf get_game_conf();

/* Submit one step and get result of this step.
*  args: step - using GoUp | GoRight | GoDown | GoLeft.
*/
alpha_snake_step_result submit_step(int step);

#endif // ALPHASNAKE_H_
