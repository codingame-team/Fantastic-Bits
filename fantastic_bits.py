import sys
import math

from scipy.optimize import linear_sum_assignment
import numpy as np


def idebug(*args):
    # return
    print(*args, file=sys.stderr)


def debug(*args):
    # return
    print(*args, file=sys.stderr)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_mh_distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


class Speed:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class Entity(Pos):
    def __init__(self, id, x, y, vx, vy, state):
        super().__init__(x, y)
        self.id = id
        self.pos = Pos(x, y)
        self.speed = Speed(vx, vy)
        self.state = state


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
debug(my_team_id)

# game loop
while True:
    line = input()
    idebug(line)
    my_score, my_magic = [int(i) for i in line.split()]
    line = input()
    idebug(line)
    opponent_score, opponent_magic = [int(i) for i in line.split()]
    entities = int(input())  # number of entities still in game
    idebug(entities)
    my_wizards = []
    op_wizards = []
    snaffles = []
    snaffles_count = 0
    my_wizards_count = 0
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        line = input()
        idebug(line)
        entity_id, entity_type, x, y, vx, vy, state = line.split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        if entity_type == 'SNAFFLE':
            snaffles.append(Entity(snaffles_count, x, y, vx, vy, state))
            snaffles_count += 1
        elif entity_type == 'WIZARD':
            my_wizards.append(Entity(my_wizards_count, x, y, vx, vy, state))
            my_wizards_count += 1
        elif entity_type == 'OPPONENT_WIZARD':
            op_wizards.append(Entity(entity_id, x, y, vx, vy, state))

    goal = Pos(16000, 3750) if my_team_id == 0 else Pos(0, 3750)

    cost = np.zeros(shape=(my_wizards_count, snaffles_count))
    debug(f'cost: {cost}')
    for wiz in my_wizards:
        for snaffle in snaffles:
            snaffle_to_goal_distance = snaffle.distance(goal) + 1
            wizard_to_snaffle_distance = wiz.distance(snaffle) + 1
            cost[wiz.id, snaffle.id] = wizard_to_snaffle_distance / snaffle_to_goal_distance
    debug(f'cost matrix - SciPy: {cost}')
    row_ind, col_ind = linear_sum_assignment(cost)
    best_move = tuple(row_ind), tuple(col_ind)
    debug(f'best_move - SciPy: {best_move}')

    thrust = 500
    for i in range(2):
        wiz = my_wizards[i]
        if wiz.state == 1:
            action = f'THROW {goal.x} {goal.y} {thrust}'
        else:
            if len(snaffles) > 1:
                index = best_move[i][1]
                snaffle = snaffles[index]
            else:
                snaffle = snaffles[-1]
            action = f'MOVE {snaffle.pos.x} {snaffle.pos.y} 150'
        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        print(action)
