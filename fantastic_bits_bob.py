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
    # return
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
        self.velocity = array([self.vx, self.vy], dtype=int)

    def distance(self, other_location: array):
        return linalg.norm(other_location - self.location)


@dataclass
class Wizard(Entity):
    accio_cooldown: int = 0
    team_id: int = None
    matching_opponent: int = field(init=False)
    action: str = field(init=False)
    goal: array = field(init=False)
    goal_x: int = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.action = None
        if self.team_id == 0:
            matching_dict = {0: 2, 1: 3}
            self.goal = array([16000, 3500])
            self.goal_x = 16000
            self.matching_opponent = matching_dict[self.id]
        else:
            matching_dict = {2: 0, 3: 1}
            self.goal = array([0, 3500])
            self.goal_x = 0
            self.matching_opponent = matching_dict[self.id]

    def update(self, x: int, y: int, vx: int, vy: int, state: int):
        self.x, self.y, self.vx, self.vy, self.state = x, y, vx, vy, state
        self.location = array([x, y])
        if self.accio_cooldown > 0:
            self.accio_cooldown -= 1


def get_wizard(wizard_id: int, wizards: List[Wizard]) -> Wizard:
    wizard_list: List[Wizard] = [w for w in wizards if w.id == wizard_id]
    return wizard_list[0] if wizard_list else None


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

""" Strat #2 (Bob)
    for each player
       done = false
       if player has a snaffle
           throw to center of goal at max power
           done = true

       if not done and mana >= 15 and player did not accio in the past 6 turns
           accio snaffle closest to “matching” opponent (0<->2, 1<->3)
           mana -= 15
           done = true

       if not done
           find snaffle closest to player
           move to the snaffle’s position at max thrust
"""

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
idebug(my_team_id)

op_team_id = (my_team_id + 1) % 2

MAX_THRUST, MAX_POWER = 150, 500
ACCIO_COST = 15

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
    op_wizards: List[Wizard] = []
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
            wizard: Wizard = get_wizard(wizard_id=i, wizards=my_wizards)
            if wizard:
                wizard.update(x=x, y=y, vx=vx, vy=vy, state=state)
            else:
                my_wizards.append(Wizard(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state, team_id=my_team_id))
        elif entity_type == 'OPPONENT_WIZARD':
            op_wizards.append(Wizard(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state, team_id=op_team_id))
        else:
            entities.append(Entity(id=entity_id, type=entity_type, x=x, y=y, vx=vx, vy=vy, state=state))

    snaffles: List[Entity] = [e for e in entities if e.type == 'SNAFFLE']
    for wizard in my_wizards:
        done: bool = False
        if wizard.state == 1:
            dest_x, dest_y = wizard.goal
            wizard.action: str = f'THROW {dest_x} {dest_y} {MAX_POWER}'
            done = True
        if not done and my_magic >= ACCIO_COST and not wizard.accio_cooldown:
            op_wizard: Wizard = [w for w in op_wizards if w.id == wizard.matching_opponent][0]
            snaffle: Entity = min(snaffles, key=lambda s: s.distance(op_wizard.location))
            wizard.action: str = f'ACCIO {snaffle.id}'
            my_magic -= ACCIO_COST
            done = True
        if not done:
            snaffle: Entity = min(snaffles, key=lambda s: s.distance(wizard.location))
            dest_x, dest_y = snaffle.location + snaffle.velocity
            wizard.action: str = f'MOVE {dest_x} {dest_y} {MAX_THRUST}'
            done = True

        print(wizard.action)
