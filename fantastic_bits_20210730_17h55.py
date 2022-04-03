import cmath
import sys
import math
from typing import Tuple, List, Optional
from enum import Enum

from scipy.optimize import linear_sum_assignment
import numpy as np


def idebug(*args):
    return
    print(*args, file=sys.stderr)


def debug(*args):
    # return
    print(*args, file=sys.stderr)


class EntityType(Enum):
    WIZARD = 0
    OPPONENT_WIZARD = 1
    SNAFFLE = 2
    BLUDGER = 3


class Vector:
    def __init__(self, a=None, b=None):
        if a and b:
            self.x, self.y = b.x - a.x, b.y - a.y

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def scalar(self, o):
        return self.x * o.x + self.y * o.y

    def is_colinear(self, o):
        v1, v2 = self, o
        return v1.x * v2.y == v1.y * v2.x

    def __repr__(self):
        return "{} {}".format(self.x, self.y)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_mh_distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'pos = ({self.x}, {self.y})'


class Speed:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def scalar(self, o):
        return self.vx * o.vx + self.vy * o.vy

    def __repr__(self):
        return f'speed = ({self.vx}, {self.vy})'


class Entity(Pos):
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        super().__init__(x, y)
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.pos = Pos(x, y)
        self.speed = Speed(vx, vy)
        self.state = state

    def __repr__(self):
        if self.entity_type == EntityType.BLUDGER:
            state = None if self.state == -1 else self.state
            state = f'last victim = {state}'
        elif self.entity_type in [EntityType.WIZARD, EntityType.OPPONENT_WIZARD]:
            state = None if self.state == 0 else self.state
            if state:
                debug(f'state = {state}')
                state = [s for s in snaffles if s.distance(self) < 1e-02][0]
            state = f'grabbed snaffle = {state}'
        else:
            state = f'captured by wizard!' if self.state else f'not yet captured!'

        return f'{self.entity_type}:  id #{self.entity_id} - {self.pos} - {self.speed} - {state}'


def affect_moves():
    cost_matrix = np.zeros(shape=(len(my_wizards), len(snaffles)))
    # debug(f'cost: {cost_matrix}')
    for wiz_index, wiz in enumerate(my_wizards):
        other_wiz = [w for w in my_wizards if w.entity_id != wiz.entity_id][0]
        for snaffle_index, snaffle in enumerate(snaffles):
            snaffle_to_other_wizard = snaffle.distance(other_wiz) + 1
            snaffle_to_op_goal_distance = snaffle.distance(op_goal) + 1
            wizard_to_snaffle_distance = wiz.distance(snaffle) + 1
            # Version 3.0
            distance_other_snaffles_to_my_goal = sum([w.distance(my_goal) for w in op_wizards]) + sum([s.distance(my_goal) for s in snaffles if s.entity_id != snaffle.entity_id])
            # Version 3.0 (short without op_wizards)
            # distance_other_snaffles_to_my_goal = sum([s.distance(my_goal) for s in snaffles if s.entity_id != snaffle.entity_id])
            cost_matrix[wiz_index, snaffle_index] = wizard_to_snaffle_distance / (snaffle_to_op_goal_distance * snaffle_to_other_wizard * distance_other_snaffles_to_my_goal)
            # Version 2.0
            cost_matrix[wiz_index, snaffle_index] = wizard_to_snaffle_distance / (snaffle_to_other_wizard)
            # Original one: version 1.0
            cost_matrix[wiz_index, snaffle_index] = wizard_to_snaffle_distance / snaffle_to_op_goal_distance
    # debug(f'cost matrix - SciPy: {cost_matrix}')
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    best_move = tuple(row_ind), tuple(col_ind)
    # debug(f'best_move - SciPy: {best_move}')
    moves_candidates = []
    for i in range(2):
        wiz = my_wizards[i]
        if len(snaffles) > 1:
            index = best_move[i][1]
            snaffle = snaffles[index]
        else:
            snaffle = snaffles[-1]
        moves_candidates.append((wiz, snaffle))
    debug(f'moves_candidates: {moves_candidates}')
    return moves_candidates


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
    bludgers = []
    # snaffles_count = 0
    # my_wizards_count = 0
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
            snaffles.append(Entity(entity_id, EntityType.SNAFFLE, x, y, vx, vy, state))
        elif entity_type == 'WIZARD':
            my_wizards.append(Entity(entity_id, EntityType.WIZARD, x, y, vx, vy, state))
        elif entity_type == 'OPPONENT_WIZARD':
            op_wizards.append(Entity(entity_id, EntityType.WIZARD, x, y, vx, vy, state))
        else:
            bludgers.append(Entity(entity_id, EntityType.BLUDGER, x, y, vx, vy, state))

    op_goal = Pos(16000, 3750) if my_team_id == 0 else Pos(0, 3750)
    my_goal = Pos(0, 3750) if my_team_id == 0 else Pos(16000, 3750)

    wizards = my_wizards + op_wizards
    my_grabbed_snaffles = [s for s in snaffles for w in my_wizards if w.distance(s) < 1e-02]
    target_snaffles = [s for s in snaffles if s not in my_grabbed_snaffles ]
    target_bludgers = [(b, min([w for w in wizards for b in bludgers if b.state != w.entity_id], key=lambda x: x.distance(b))) for b in bludgers]

    moves_candidates = affect_moves()
    thrust = 500
    debug(f'my wizards = {my_wizards}')
    for i in range(2):
        wiz = my_wizards[i]
        if wiz.state == 1:
            my_grabbed_snaffle = [s for s in snaffles for w in my_wizards if w.pos == s.pos][0]
            debug(f'wizard {wiz.entity_id} has grabbed snaffle: {my_grabbed_snaffle}!')
            action = f'THROW {op_goal.x} {op_goal.y} {thrust}'
        else:
            snaffle_candidates = [(s, s.distance(wiz) / (s.distance(my_goal) + 1))
                                  for s in target_snaffles if s.distance(op_goal) > wiz.distance(op_goal)]
            snaffle_candidates = [(s, s.distance(wiz) / (sum([s.distance(w) for w in op_wizards]) * (s.distance(my_goal) + 1)))
                                  for s in target_snaffles if s.distance(op_goal) > wiz.distance(op_goal)]
            snaffle_candidates.sort(key=lambda w: w[1], reverse=True)
            # bludger_candidates = [(b, b.distance(wiz)) for b in target_bludgers if b.state != wiz.entity_id and b.distance(wiz) < 2000]# and b.aims_to(wiz)]
            bludgers_attacking_player = [b for b, w in target_bludgers if w.entity_id == wiz.entity_id and b.distance(wiz) < 3000]
            # bludger_candidates = [(b, b.distance(wiz)) for b in target_bludgers if b.state != wiz.entity_id and b.distance(wiz) < 4000]
            debug(f'bludgers approaching... {bludgers_attacking_player}')
            # bludger_candidates.sort(key=lambda b: b[1], reverse=True)
            if bludgers_attacking_player and my_magic > 20:
                bludger: Entity = bludgers_attacking_player[0]
                target: Entity = min(op_wizards, key=lambda w: bludger.distance(w))
                action = f'WINGARDIUM {bludger.entity_id} {target.x} {target.y} 20'
                target_bludgers.remove((bludger, wiz))
                my_magic -= 10
            elif not bludgers_attacking_player and snaffle_candidates and my_magic > 10:
                snaffle: Entity = max(snaffle_candidates, key=lambda x: x[1])[0]
                # snaffle: Entity = snaffle_candidates[0][0]
                target_snaffles.remove(snaffle)
                # action = f'WINGARDIUM {snaffle.entity_id} {wiz.x} {wiz.y} 10'
                action = f'WINGARDIUM {snaffle.entity_id} {op_goal.x} {op_goal.y} 10'
                my_magic -= 10
            else:
                snaffle = [s for w, s in moves_candidates if w.entity_id == wiz.entity_id][0]
                action = f'MOVE {snaffle.x} {snaffle.y} 150'
        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        print(action)
