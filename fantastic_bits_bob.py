#
#   fantastic_bits_bob.py
#   Fantastic bits / Broomstick Flyers
#
#   Created by philRG on 16/04/2022
#   Copyright © 2022 philRG. All rights reserved.
#
import sys
from dataclasses import dataclass, field
from typing import List

from numpy import array, linalg


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
        self.location = array([self.x, self.y], dtype=int)
        self.velocity = array([self.x, self.y], dtype=int)

    def distance(self, other_location: array):
        return linalg.norm(other_location - self.location)

@dataclass
class Wizard(Entity):
    goal_x: int
    action: str = field(init=False)
    goal: array = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.action = None
        self.goal = array([self.goal_x, 3500])

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

"""
    for each player
        done = false
        if player has a snaffle
               throw to center of goal at max power
               done = true
        if not done
               find snaffle closest to player
               move to the snaffle’s position at max thrust
"""

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
idebug(my_team_id)

goal_x: int = 16000 if my_team_id == 0 else 0

MAX_THRUST, MAX_POWER = 150, 500

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    idebug(my_score, my_magic)
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    idebug(opponent_score, opponent_magic)
    entities_count = int(input())  # number of entities still in game
    idebug(entities_count)

    entities: List[Entity] = []
    my_wizards: List[Wizard] = []
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
            my_wizards.append(Wizard(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state, goal_x=goal_x))
        else:
            entities.append(Entity(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state))

    snaffles: List[Entity] = [e for e in entities if e.type == 'SNAFFLE']
    for wizard in my_wizards:
        done: bool = False
        if wizard.state == 1:
            dest_x, dest_y = wizard.goal
            wizard.action = f'THROW {dest_x} {dest_y} {MAX_POWER}'
            done = True
        if not done:
            snaffle: Entity = min(snaffles, key=lambda s: s.distance(wizard.location))
            dest_x, dest_y = snaffle.location + snaffle.velocity
            wizard.action = f'MOVE {dest_x} {dest_y} {MAX_THRUST}'

        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        print(wizard.action)
