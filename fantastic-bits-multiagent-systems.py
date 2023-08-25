import sys
import math
from random import random, uniform

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
x_goal = 16000 if my_team_id == 0 else 0
x_def = 700 if my_team_id == 0 else 15300

def get_entities_dist(entity_1, entity_2):
    x1, y1 = entity_1['position']
    x2, y2 = entity_2['position']
    return math.hypot(x1 - x2, y1 - y2)

def get_closest_entity(some_entity, targets_dict, except_ids = None):
    closest = None
    for id, target in targets_dict.items():
        if(len(targets_dict) > 1 and except_ids is not None and id in except_ids):
            continue
        target['dist'] = get_entities_dist(some_entity, target)
        if(closest is None or target['dist'] < closest['dist']):
            closest = target
    
    return closest

def throw_snaffle(wizard, x, y, power):
    set_action(wizard, f'THROW {x} {y} {power}')

def move_wizard(wizard, x, y, velocity):
    set_action(wizard, f'MOVE {x} {y} {velocity}')    

def is_in_defense_area(x):
    if (my_team_id == 0 and x - x_def < 1000) or (my_team_id == 1 and x_def - x < 1000):
        return True
    return False

def set_action(wizard, action):
    if 'action' not in wizard or len(wizard['action']) == 0:
        wizard['action'] = action
        return action
    return ''

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    n_entities = int(input())  # number of entities still in game
    entities = {}
    my_wizards = {}
    snaffles = {}
    bludgers = {}
    opponents = {}
    for i in range(n_entities):
        inputs = input().split()
        entity_id = int(inputs[0])  # entity identifier
        entity_type = inputs[1]  # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        x = int(inputs[2])  # position
        y = int(inputs[3])  # position
        vx = int(inputs[4])  # velocity
        vy = int(inputs[5])  # velocity
        state = int(inputs[6])  # 1 if the wizard is holding a Snaffle, 0 otherwise
        entities[entity_id] = {
            'entity_id': entity_id,
            'entity_type': entity_type,
            'position': (x, y),
            'velocity': (vx, vy),
            'isHoldingSnaffle': state
        }
        if(entity_type == 'WIZARD'):
            my_wizards[entity_id] = entities[entity_id]
        elif(entity_type == 'SNAFFLE'):
            snaffles[entity_id] = entities[entity_id]
        elif(entity_type == 'BLUDGER'):
            bludgers[entity_id] = entities[entity_id]
        elif(entity_type == 'OPPONENT_WIZARD'):
            opponents[entity_id] = entities[entity_id]
    
    w1_id, w2_id = my_wizards
    w1 = my_wizards[w1_id]
    w2 = my_wizards[w2_id]
    b1 = get_closest_entity(w1, bludgers)
    b2 = get_closest_entity(w2, bludgers)
    enemy1 = get_closest_entity(w1, opponents)
    enemy2 = get_closest_entity(w2, opponents)

    # wizard 1 logic
    if w1['isHoldingSnaffle']:
        x = x_goal
        y = 3750 + int(1300 * uniform(-1, 1))
        power = 500
        throw_snaffle(w1, x, y, power)
    else:        
        snaffle1 = get_closest_entity(w1, snaffles)
        x, y = snaffle1['position']
        v = 150
        move_wizard(w1, x, y, v)


    # wizard 2 logic
    x_w2, y_w2 = w2['position']
    if w2['isHoldingSnaffle']:            
        x = x_goal
        y = 3750 + int(1300 * uniform(-1, 1))
        power = 500
        throw_snaffle(w2, x, y, power)
    else:            
        snaffle2 = get_closest_entity(w2, snaffles, [snaffle1['entity_id']])
        x, y = snaffle2['position']
        if random() > 2500/(snaffle2['dist'] + 1):
            x = x_def
        v = 150
        move_wizard(w2, x, y, v)
    
    print(w1['action'])
    print(w2['action'])

    #for i in range(2):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        #print("MOVE 8000 3750 100")
