from AlphaSnakeIO import Game, STEP, STATUS


# `register` and `submit_step` will block the program until update notification is received from server.
# You may use asynchronous algorithm to keep calculation when your CPU is idle.

def main():
    # Create a game handle for server communication.
    game = Game()
    # Register an account with a username. call once in your program is enough.
    battlefield = game.register('BetaSnake')

    while True:
        # YOUR ALGORITHM
        mystep = STEP.DOWN

        # Submit one step and get result of this step. call it to finish one step.
        battlefield, status = game.submit_step(mystep)

        if status == STATUS.ALIVE:
            # Continue your algorithm for another iteration.
            continue
        elif status == STATUS.DIED:
            print('Better luck next time!')
            break
        elif status == STATUS.WIN:
            print('Winner winner, python dinner.')
            break


if __name__ == '__main__':
    main()
