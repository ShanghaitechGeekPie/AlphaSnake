# import AlphaSnakeIO

import requests


# def main():
#     # Get the config of this game. call once in your program is enough.
#     conf = AlphaSnakeIO.get_game_conf()

#     # YOUR ALGORITHM

#     # Submit one step and get result of this step. call it to finish one step.
#     # If your program died this function will kill the program.
#     # If you have no choice but die, please at lease submit one step.
#     resault = AlphaSnakeIO.submit_step(AlphaSnakeIO.GoUp)


# main()

res = requests.post('http://127.0.0.1:8000/init', {'name': 'rk'}).content
print(res)
