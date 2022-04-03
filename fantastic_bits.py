#
#   fantastic_bits.py
#   Fantastic bits / Broomstick Flyers
#
#   Created by philRG on 03/04/2022
#   Copyright © 2022 philRG. All rights reserved.
#

import random
import sys
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
from numpy import array
from scipy.optimize import linear_sum_assignment


def idebug(*args):
    return
    print(*args, file=sys.stderr)


def debug(*args):
    # return
    print(*args, file=sys.stderr)


@dataclass
class Entity:
    id: int
    type: int
    x: int
    y: int
    vx: int
    vy: int
    state: int
    location: array = field(init=False)
    velocity: array = field(init=False)

    def __post_init__(self):
        self.location = array([self.x, self.y])
        self.velocity = array([self.vx, self.vy])

    def distance(self, other_location: array):
        return np.linalg.norm(other_location - self.location)

    def distance_to_goal(self, goal_x: int):
        if self.y < TOP_GOAL_Y:
            top_goal: array = array([goal_x, TOP_GOAL_Y])
            return self.distance(top_goal)
        elif self.y <= BOTTOM_GOAL_Y:
            return abs(goal_x - self.x)
        else:
            bottom_goal: array = array([goal_x, BOTTOM_GOAL_Y])
            return self.distance(bottom_goal)

    def is_aligned(self, wizard, target_goal_x: int) -> bool:
        """
            Check if a snaffle is aligned for flipendo
        :param wizard:
        :param target_goal_x:
        :return: True or False
        """
        vect: array = self.location - wizard.location
        """ a * Y + b * X + c = 0 
        """
        # debug(f'target goal: {target_goal_x}')
        # debug(f'wizard goal: {wizard.goal_x}')
        if target_goal_x == wizard.goal_x:
            return False
        if wizard.x < self.x < target_goal_x or wizard.x > self.x > target_goal_x:
            a, b = -vect[0], vect[1]
            c = -a * wizard.y - b * wizard.x
            target_y: int = (-b * target_goal_x - c) / a
            if target_y > 0 and TOP_GOAL_Y + 400 < target_y < BOTTOM_GOAL_Y - 400:
                debug(f'{wizard.type} #{wizard.id} aligned with {self.type} #{self.id} and {"LEFT_GOAL" if goal_x == 0 else "RIGHT_GOAL"}')
                return True
        return False

    def aims_to(self, entity) -> bool:
        u_x, u_y = entity.location - self.location
        v_x, v_y = self.velocity
        return u_x * v_y == u_y * v_x


@dataclass
class Wizard(Entity):
    goal_x: int
    action: str = field(init=False)
    captured_snaffle: object = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.action = None
        self.captured_snaffle = None

    def throw(self, goal_x: int) -> array:
        # goal_y: int = TOP_GOAL_Y + SNAFFLE_RADIUS if self.y < TOP_GOAL_Y else self.y if self.y <= BOTTOM_GOAL_Y else BOTTOM_GOAL_Y - SNAFFLE_RADIUS
        goal_y: int = int(FIELD_LENGTH_Y / 2)
        return array([goal_x, goal_y])


def assign_moves(player_wizards: List[Entity], snaffles: List[Entity]) -> List[Tuple[Entity, Entity]]:
    """
        Assign each wizard to a snaffle (not already captured by other wizard)
    :param player_wizards: list of player wizard without snaffle
    :param snaffles: list of available snaffles
    :return: list of (Wizard, Snaffle) assignment
    """
    cost_matrix = np.zeros(shape=(len(player_wizards), len(snaffles)))
    # debug(f'cost: {cost_matrix}')
    for wiz_index, wiz in enumerate(player_wizards):
        other_wiz: Entity = [w for w in player_wizards if w.id != wiz.id][0]
        player_goal_x: int = wiz.goal_x
        op_goal_x: int = LEFT_GOAL_X if player_goal_x == RIGHT_GOAL_X else RIGHT_GOAL_X
        for snaffle_index, snaffle in enumerate(snaffles):
            snaffle_to_other_wizard = snaffle.distance(other_wiz.location) + 1
            snaffle_to_op_goal_distance = snaffle.distance_to_goal(op_goal_x) + 1
            wizard_to_snaffle_distance = wiz.distance(snaffle.location) + 1
            # Version 3.0
            # distance_other_snaffles_to_my_goal = sum([w.distance_to_goal(player_goal_x) for w in op_wizards]) + sum([s.distance_to_goal(player_goal_x) for s in snaffles if s.id != snaffle.id])
            # Version 3.0 (short without op_wizards)
            # distance_other_snaffles_to_my_goal = sum([s.distance(my_goal) for s in snaffles if s.entity_id != snaffle.entity_id])
            # cost_matrix[wiz_index, snaffle_index] = wizard_to_snaffle_distance / (snaffle_to_op_goal_distance * snaffle_to_other_wizard * distance_other_snaffles_to_my_goal)
            # Version 2.0
            # cost_matrix[wiz_index, snaffle_index] = wizard_to_snaffle_distance / snaffle_to_other_wizard
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


""" BlitzProg: 
    My naïve strategy:
        Target the closest snaffle that was not targeted by the other wizard,
        If you have the snaffle, throw it in the direction of the goals.
        If you don’t, if it is in front of the goal (if the straight line [wizard - snaffle]) and you have at least 20 mana, use Flipendo.
        If it is far behind you and you have 40 mana, use Accio
        This naïve strategy only requires some line intersection formula to find out if you can Flipendo and goal, 
        but you can find that formula easily on wikipedia and simplify it to your needs.
"""

""" Remi:
    Une utilisation basique des sorts te fais passer en silver
        en gros, un flipendo si le snaffle est bien aligné avec les buts (faut faire un peu de maths)
        un accio si un adversaire risque de choper le snaffle avant toi (pas sûr que je l'avais fait en bronze)
        
    Remi. 06:20PM
        philRG tu t'es remis à broomstick flyers ? effectivement y a pas de touches et corners, le snaffle rebondit sur les bords ... 
        la seule chose nouvelle par rapport à ce que tu as déjà fait, c'est lancer des sorts ^^ ACCIO pour choper la baballe avant ton adversaire, 
        et FLIPENDO si tu es bien aligné avec les buts.
"""

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

# constants
FIELD_LENGTH_X = 16001
FIELD_LENGTH_Y = 7501
LEFT_GOAL_X = 0
RIGHT_GOAL_X = 16000
TOP_GOAL_Y = int((FIELD_LENGTH_Y - 4000) / 2) + 300
BOTTOM_GOAL_Y = int((FIELD_LENGTH_Y - 4000) / 2) + 4000 - 300
BLUDGER_RADIUS = 200
WIZARD_RADIUS = 400
POST_RADIUS = 300
SNAFFLE_RADIUS = 150

FLIPENDO_COST, ACCIO_COST = 20, 15

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
idebug(my_team_id)

my_goal_x, op_goal_x = (LEFT_GOAL_X, RIGHT_GOAL_X) if my_team_id == 0 else (RIGHT_GOAL_X, LEFT_GOAL_X)

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    idebug(my_score, my_magic)
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    idebug(opponent_score, opponent_magic)

    entities_count = int(input())  # number of entities still in game
    idebug(entities_count)

    my_wizards: List[Wizard] = []
    op_wizards: List[Wizard] = []
    snaffles: List[Entity] = []
    bludgers: List[Entity] = []
    for i in range(entities_count):
        line = input()
        idebug(line)
        inputs = line.split()
        entity_id = int(inputs[0])  # entity identifier
        entity_type = inputs[1]  # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        x = int(inputs[2])  # position
        y = int(inputs[3])  # position
        vx = int(inputs[4])  # velocity
        vy = int(inputs[5])  # velocity
        state = int(inputs[6])  # 1 if the wizard is holding a Snaffle, 0 otherwise
        if entity_type == 'WIZARD':
            goal_x = my_goal_x
            my_wizards.append(Wizard(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state, goal_x=goal_x))
        elif entity_type == 'OPPONENT_WIZARD':
            goal_x = op_goal_x
            op_wizards.append(Wizard(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state, goal_x=goal_x))
        else:
            goal_x = None
            if entity_type == 'SNAFFLE':
                snaffles.append(Entity(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state))
            else:
                bludgers.append(Entity(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state))

    # Store snaffle's reference in wizard entity if it was captured
    for s in snaffles:
        if s.state == 1:
            for w in my_wizards + op_wizards:
                if (w.location == s.location).all():
                    w.captured_snaffle = s

    actions: List[str] = []
    thrust, power = 150, 500

    """ Try to flipendo free snaffles """
    available_wizards: List[Entity] = my_wizards[:]
    flipendo_candidates: List[Tuple[Entity, Entity]] = [(s, w) for s in snaffles for w in available_wizards if s.state == 0 and s.x > w.x and s.is_aligned(wizard=w, target_goal_x=op_goal_x)]

    while my_magic > FLIPENDO_COST and available_wizards and flipendo_candidates:
        wizard = available_wizards.pop()
        snaffle_candidates: List[Entity] = [s for s, w in flipendo_candidates if w == wizard]
        if snaffle_candidates:
            # snaffle = max(snaffle_candidates, key=lambda s: s.distance_to_goal(op_goal_x))
            snaffle = max(snaffle_candidates, key=lambda s: s.distance_to_goal(op_goal_x) / s.distance(wizard.location) ** 2)
            snaffle.state = 1  # lock snaffle
            wizard.action = f'FLIPENDO {snaffle.id}'
            my_magic -= FLIPENDO_COST
        flipendo_candidates: List[Tuple[Entity, Entity]] = [(s, w) for s in snaffles for w in my_wizards if s.state == 0 and s.x > w.x and s.is_aligned(wizard=w, target_goal_x=op_goal_x)]

    """ Throw captured snaffles """
    throw_candidates: List[Tuple[Entity, array]] = [(w, w.throw(goal_x=op_goal_x)) for w in my_wizards if not w.action and w.state == 1]
    for wizard, throw_dest in throw_candidates:
        wizard.action = f'THROW {throw_dest[0]} {throw_dest[1]} {power}'
    available_snaffles: List[Entity] = [s for s in snaffles if s.state == 0]

    # """ Exclude snaffles targeted by opponent wizards in first choice """
    # available_snaffles_targeted_by_opponent: List[Entity] = []
    # op_wizards_lurking_for_snaffles: List[Entity] = [w for w in op_wizards if e.state == 0]
    # for snaffle in available_snaffles:
    #     snaffle_is_targeted = False
    #     for op_wizard in op_wizards_lurking_for_snaffles:
    #         if op_wizard.aims_to(snaffle):
    #             snaffle_is_targeted = True
    #     if snaffle_is_targeted:
    #         available_snaffles_targeted_by_opponent.append(snaffle)
    # available_snaffles = [s for s in available_snaffles if s not in available_snaffles_targeted_by_opponent] if available_snaffles_targeted_by_opponent else available_snaffles

    available_wizards: List[Wizard] = [w for w in my_wizards if w.state == 0 and not w.action]
    i = 0
    while available_wizards and available_snaffles:
        # i += 1
        # debug(f'STEP #{i}')
        # for s in available_snaffles:
        #     debug(s)
        if len(available_wizards) == 2:
            moves_candidates: List[Tuple[Entity, Entity]] = assign_moves(player_wizards=my_wizards, snaffles=available_snaffles)
            for w, s in moves_candidates:
                debug(f'wizard #{w.id} move to snaffle #{s.id}')
            while moves_candidates and available_snaffles:
                wizard, snaffle = moves_candidates.pop()
                wizard.action = f'MOVE {snaffle.x} {snaffle.y} {thrust}'
                # try:
                #     available_snaffles.remove(snaffle)
                # except ValueError:
                #     debug(f'snaffle {snaffle.id} not found in available snaffles')
                #     for s in available_snaffles:
                #         debug(s)
        elif len(available_wizards) == 1:
            my_wizard: Entity = available_wizards[0]
            snaffle: Entity = min(available_snaffles, key=lambda s: s.distance(my_wizard.location))
            my_wizard.action = f'MOVE {snaffle.x} {snaffle.y} {thrust}'
            # available_snaffles.remove(snaffle)
        available_snaffles = [s for s in snaffles if s.state == 0]
        available_wizards: List[Entity] = [w for w in my_wizards if w.state == 0 and not w.action]

    available_wizards: List[Wizard] = [w for w in my_wizards if not w.action]
    op_wizards_with_snaffles = [w for w in op_wizards if w.state == 1]
    # accio_candidates: List[Tuple[Wizard, Wizard]] = [(op_w, w) for op_w in op_wizards for w in available_wizards if op_w.state == 1 and op_w.distance_to_goal(goal_x=my_goal_x) < w.distance_to_goal(goal_x=my_goal_x)]
    accio_candidates: List[Tuple[Entity, Wizard]] = [(s, w) for s in snaffles for w in available_wizards if s.distance_to_goal(goal_x=my_goal_x) < w.distance_to_goal(goal_x=my_goal_x)]

    # op_wizards_accio_targeted: List[Wizard] = []
    snaffles_accio_targeted: List[Entity] = []
    while my_magic > ACCIO_COST and available_wizards and accio_candidates:
        # op_wizard, wizard = min(accio_candidates, key=lambda x: x[0].distance_to_goal(goal_x=my_goal_x))
        snaffle, wizard = min(accio_candidates, key=lambda x: x[0].distance_to_goal(goal_x=my_goal_x))
        wizard.action = f'ACCIO {snaffle.id}'
        my_magic -= ACCIO_COST
        # op_wizards_accio_targeted.append(op_wizard)
        snaffles_accio_targeted.append(snaffle)
        available_wizards: List[Wizard] = [w for w in my_wizards if not w.action]
        # op_wizards_with_snaffles = [w for w in op_wizards if w.state == 1 and w not in op_wizards_accio_targeted]
        # accio_candidates: List[Wizard] = [(op_w, w) for op_w in op_wizards for w in available_wizards if
        #                                   op_w.state == 1 and op_w.distance_to_goal(goal_x=my_goal_x) < w.distance_to_goal(goal_x=my_goal_x)]
        accio_candidates: List[Tuple[Entity, Wizard]] = [(s, w) for s in snaffles for w in available_wizards if s not in snaffles_accio_targeted and s.distance_to_goal(goal_x=my_goal_x) < w.distance_to_goal(goal_x=my_goal_x)]

    op_wizards_with_snaffles = [w for w in op_wizards if w.state == 1]
    if available_wizards:
        if op_wizards_with_snaffles:
            for wizard in available_wizards:
                target: Entity = min(op_wizards_with_snaffles, key=lambda w: w.distance(wizard.location))
                wizard.action = f'MOVE {target.x} {target.y} {thrust}'
        else:
            for wizard in available_wizards:
                target_x, target_y = random.randint(0, FIELD_LENGTH_X), random.randint(0, FIELD_LENGTH_Y)
                wizard.action = f'MOVE {target_x} {target_y} {thrust}'

    available_wizards: List[Wizard] = [w for w in my_wizards if not w.action]
    if available_wizards:
        for wizard in available_wizards:
            target_x, target_y = random.randint(0, FIELD_LENGTH_X), random.randint(0, FIELD_LENGTH_Y)
            wizard.action = f'MOVE {target_x} {target_y} {thrust}'

    for i in range(2):
        w: Entity = [w for idx, w in enumerate(my_wizards) if idx == i][0]
        print(w.action)
