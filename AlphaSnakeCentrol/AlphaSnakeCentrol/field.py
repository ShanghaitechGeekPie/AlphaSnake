import numpy as np
'''
    This part controls the update of the field. Defining field matrix as follows:
        x means the row index, y means the column index
            +------------------------------------------->(y)
            |
            |
            |
            |                   0
            |                   |
            |              3 ---*--- 1
            |                   |
            |                   2
            |
            |
            |
            |
            V(x)
'''

class Field():
    '''
        The object Field update it state by calling 'go' method, which takes in the movement of each participant
    and return the whole map and the users' state after this iteration.
        Using 'enroll' method to add one or a list of participants into the field.
    '''
    def __init__(self, num_users, map_size=(100, 100)):
        '''
            Given information to setup the field to start the game.
        '''
        # The map contains 100*100 bytes which represents the state of the pixel (occupied by user or food or
        # unoccupied)
        self.map = np.zeros(map_size, dtype=np.int8)

        # A dictionary using user ID (a non-negative number) as index, a tuple as value which contains the state
        # of the user and the body (a list of coordinates) of the snake. index 0 gets the head coordinate.
        self.users = [] #TODO (initialize users info later in this function)

    def go(self, moves=None):
        '''
            Given the movement of each participant, return the whole map and a dictionary of participants' states.
            moves: a dictionary with participants' ID as key and a number (0,1,2,3) as value indicates the moving
        direction.
            return: a matrix represented in a 2D-list (index using [i][j])
                and a dictionary with participants' ID as key and a number representing state (0: dead, 1: alive)
        '''
        pass