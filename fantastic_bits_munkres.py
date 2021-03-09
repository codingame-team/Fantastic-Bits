import sys
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_mh_distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def get_distance(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2


class Speed:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class Entity:
    def __init__(self, id, x, y, vx, vy, state):
        self.id = id
        self.pos = Point(x, y)
        self.speed = Speed(vx, vy)
        self.state = state


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game
    my_wizards = []
    op_wizards = []
    snaffles = []
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        if entity_type == 'SNAFFLE':
            snaffles.append(Entity(entity_id, x, y, vx, vy, state))
        elif entity_type == 'WIZARD':
            my_wizards.append(Entity(entity_id, x, y, vx, vy, state))
        elif entity_type == 'OPPONENT_WIZARD':
            op_wizards.append(Entity(entity_id, x, y, vx, vy, state))

    # Aim each wizard to closest snaffles and throw them
    matrix = []
    for wiz in my_wizards:
        row = []
        for snaffle in snaffles:
            col = wiz.pos.get_mh_distance(snaffle.pos)
            row.append(col)
        matrix.append(row)
    print(matrix, file=sys.stderr)
    if len(snaffles) > 1:
        costs = {}
        for i in range(len(snaffles)):
            for j in range(len(snaffles)):
                if j != i:
                    costs[(0, i), (1, j)] = matrix[0][i] + matrix[1][j]
        best_move = min(costs)
        print(best_move, file=sys.stderr)

    for i in range(2):
        wiz = my_wizards[i]
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        if wiz.state == 1:
            if my_team_id == 0:
                action = "THROW 16000 3750 500"
            else:
                action = "THROW 0 3750 500"
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
