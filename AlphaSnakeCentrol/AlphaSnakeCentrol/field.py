import numpy as np
import time
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
GoUndefined = -1    # only for player died
GoUp = 0
GoRight = 1
GoDown = 2
GoLeft = 3


class Snake():
    '''
        Use to record user state, not for external use
    '''

    def __init__(self, head=None):
        if head == None:
            self.state = 0
            self.body = []
        else:
            self.state = 1
            self.body = [head]

    def head(self):
        return self.body[0]

    def tail(self):
        return self.body[-1]

    def die(self):
        self.state = 0


class Field():
    '''
        The object Field update it state by calling 'go' method, which takes in the movement of each participant
    and return the whole map and the users' state after this iteration.
        User ID start at 1
        User state: 0: dead, 1: alive
        Food: -1 on the map
        User length: access by using self.user_len(i) (i-th user)
    '''

    def __init__(self, num_users, num_foods=2, map_size=(100, 100), dead2food=False):
        '''
            Given information to setup the field to start the game.
            Set the number un-eaten food in num_foods argument
        '''
        # The map contains 100*100 bytes which represents the state of the pixel (occupied by user or food or
        # unoccupied)
        self.map = np.zeros(map_size, dtype=np.int8)

        # A list using user ID (a positive number) as index, a tuple as value which contains the state of the
        # user and the body (a list of coordinates) of the snake. index 0 gets the head coordinate.
        self.users = [Snake()]

        # setup whether needed to change dead body to food
        self.dead2food = dead2food

        # initializing map and user state
        for i in range(1, num_users + 1):
            # generate coordinates without conflict with the initial map
            x = np.random.randint(0, map_size[0])
            y = np.random.randint(0, map_size[1])
            while self.map[x, y] != 0:
                x = np.random.randint(0, map_size[0])
                y = np.random.randint(0, map_size[1])

            # set map and user info
            self.map[x, y] = 2 * i
            self.users.append(Snake(head=(x, y)))

        # set food on the map
        for i in range(num_foods):
            x = np.random.randint(0, map_size[0])
            y = np.random.randint(0, map_size[1])
            while self.map[x, y] != 0:
                x = np.random.randint(0, map_size[0])
                y = np.random.randint(0, map_size[1])
            self.map[x, y] = -1

    def eat_food(self, uid, move) -> bool:
        '''
            DO NOT call this function externally.
            It checks whether this movement will make this user eat a food.
        '''
        user_coordinate = self.users[uid].head()
        target = []
        if move == GoUp:
            target = (user_coordinate[0] - 1, user_coordinate[1])
        elif move == GoRight:
            target = (user_coordinate[0], user_coordinate[1] + 1)
        elif move == GoDown:
            target = (user_coordinate[0] + 1, user_coordinate[1])
        elif move == GoLeft:
            target = (user_coordinate[0], user_coordinate[1] - 1)
        else:
            self.users[uid].die()
            return False

        # check if the request is out side of the map
        if target[0] < 0 or target[0] >= self.map.shape[0] or target[1] < 0 or target[1] >= self.map.shape[1]:
            return False
        if self.map[target] == -1:
            return True
        else:
            return False

    def hit_body(self, uid, move, moves) -> bool:
        '''
            DO NOT call this externally.
            To check if the user hit a body of on the map, not only check the pixel to go whether is a body (odd
        value), but also check if is a head whose user_id smaller than this in terms of the body state updating
        sequence.
            Because when head crush together, it should be two user die.
        '''
        user_coordinate = self.users[uid].head()
        target = []
        if move == GoUp:
            target = (user_coordinate[0] - 1, user_coordinate[1])
        elif move == GoRight:
            target = (user_coordinate[0], user_coordinate[1] + 1)
        elif move == GoDown:
            target = (user_coordinate[0] + 1, user_coordinate[1])
        elif move == GoLeft:
            target = (user_coordinate[0], user_coordinate[1] - 1)
        else:
            self.users[uid].die()
            return True

        # check if the request is out side of the map
        if target[0] < 0 or target[0] >= self.map.shape[0] or target[1] < 0 or target[1] >= self.map.shape[1]:
            self.users[uid].die()
            return True

        if self.map[target] <= 0:
            return False

        # Could crush into other user
        crush_uid = (self.map[target] + 1) // 2
        if self.map[target] % 2 != 0:
            # This is not a head, but could be a tail
            if crush_uid < uid or not self.users[crush_uid].state:
                # a processed user or a dead user
                self.users[uid].die()
                return True
            elif target != self.users[crush_uid].tail():
                self.users[uid].die()
                return True
            elif self.eat_food(crush_uid, moves[crush_uid]):
                # Although it is a tail, but the user is going to eat
                self.users[uid].die()
                return True
            else:
                return False

        if crush_uid < uid:
            # two head crush together occasion
            self.users[crush_uid].die()
            self.users[uid].die()
            return True
        elif len(self.users[crush_uid].body) > 1 or self.eat_food(crush_uid, moves[crush_uid]):
            # hit the neck of other users 23333
            self.users[uid].die()
            return True
        else:
            # just pass the user with length 1, so close
            return False

    def move_body(self, uid, move, ate):
        '''
            DO NOT call this function externally
            move the body of given user
        '''
        user_coordinate = self.users[uid].head()
        target = []
        if move == GoUp:
            target = (user_coordinate[0] - 1, user_coordinate[1])
        elif move == GoRight:
            target = (user_coordinate[0], user_coordinate[1] + 1)
        elif move == GoDown:
            target = (user_coordinate[0] + 1, user_coordinate[1])
        elif move == GoLeft:
            target = (user_coordinate[0], user_coordinate[1] - 1)
        else:
            self.users[uid].die()
            return

        if not ate:
            if (self.map[self.users[uid].tail()] + 1) // 2 == uid:
                # in case it is just other users head (other_uid < uid)
                self.map[self.users[uid].tail()] = 0
            self.users[uid].body.pop()
        if len(self.users[uid].body) > 0:
            self.map[self.users[uid].head()] -= 1

        self.users[uid].body.insert(0, target)
        self.map[self.users[uid].head()] = 2 * uid

    def go(self, moves=None):
        '''
            Given the movement of each participant, return the whole map and a dictionary of participants' states.
            moves: a list with participants' ID as index (start from 1) and a number (0,1,2,3) as value indicates
        the moving direction.
            return: a matrix represented in a 2D array
                and a list with participants' ID (a positive number) as index and a number representing state
        '''
        # make sure the lengh of the list is the number of users
        moves = [0] + moves
        assert len(moves) == len(self.users), "Different input length as declared number of users"

        food_eaten = 0
        # iterate each users to move the snake
        for i in range(1, len(self.users)):
            if not self.users[i].state:
                continue  # if user is dead
            will_eat = self.eat_food(i, moves[i])
            died = self.hit_body(i, moves[i], moves)
            if not died:
                if will_eat:
                    food_eaten += 1
                self.move_body(i, moves[i], will_eat)
            else:
                # prevent the death distrubing the judgement
                self.map[self.users[i].head()] = 2 * i - 1

        if self.dead2food:
            # change all the dead body to food and remove the user info (length to 0)
            pass

        # check if food is less
        map_size = self.map.shape
        for i in range(food_eaten):
            # generate food at random location
            x = np.random.randint(0, map_size[0])
            y = np.random.randint(0, map_size[1])
            while self.map[x, y] != 0:
                x = np.random.randint(0, map_size[0])
                y = np.random.randint(0, map_size[1])
            self.map[(x, y)] = -1

        # return the state of the field and the users states
        states = [user.state for user in self.users][1:]
        return (self.map.reshape(-1), states)

    def user_len(self, i):
        assert i < len(self.users), "Too large index when consulting user length"
        return len(self.users[i].body)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import keyboard

    # perform self test
    refresh_period = 0.01
    num_users = 7
    field = Field(num_users, 50)

    def rand_move(num_users):
        if num_users == 1:
            try:
                value = 0
                if keyboard.is_pressed('up'):
                    value = 0
                elif keyboard.is_pressed('right'):
                    value = 1
                elif keyboard.is_pressed('down'):
                    value = 2
                elif keyboard.is_pressed('left'):
                    value = 3
                else:
                    value = -1
                return np.array([0, value])
            except:
                return [0, -1]
        else:
            return np.random.randint(4, size=(num_users + 1))

    # initializing image
    im = None
    (field_image, states) = field.go(rand_move(num_users))
    print(states, end='')
    try:
        im = plt.imshow(field_image.reshape(100, 100), cmap='nipy_spectral')
        plt.pause(refresh_period)
        plt.draw()
    except:
        pass
    plt.colorbar()
    while True:
        (field_image, states) = field.go(rand_move(num_users))

        print('\r', end='')
        print(states, end='')

        try:
            im.set_data(field_image.reshape(100, 100))
            plt.pause(refresh_period)
            plt.draw()
        except:
            print()
            break
