# define of step choice
GoUndefined = -1    # only for player died
GoUp = 0
GoRight = 1
GoDown = 2
GoLeft = 3

# get the config of this game.
def get_game_conf():
    response = {
        'map_max_x': 99,
        'map_max_y': 99,
        'id': 0,
        'num': 2,
        'start_position': [
            [0, 0],
        ],
    }
    return response;

# Submit one step and get result of this step.
#     args: step - using GoUp | GoRight | GoDown | GoLeft.
def submit_step(step):
    print "[Step Submitted] {}".format(step);
    response = {
        'status':[
            0,
        ],
        'step': [
            step,
        ],
    }
    return response;
