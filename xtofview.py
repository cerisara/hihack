import pathlib
import os
import matplotlib.pyplot as plt
import numpy as np
from nle.dataset import dataset
import nle.dataset as nld
from nle.dataset import db
from nle.dataset import populate_db
from nle.nethack import tty_render
base_path = str(pathlib.Path().resolve())
HIHACK_PATH = os.path.join(base_path[:base_path.find('hihack')], 'hihack')
from hihack_ordinals import HIHACK_ORDINALS
from nle.nethack.actions import ACTIONS

ORDINAL_BACKMAP = {
    v: k for (k, v) in HIHACK_ORDINALS.items()
}

NH_ACTION_IDX_TO_STR = {int(ACTIONS[i]): str(ACTIONS[i]) for i in range(len(ACTIONS))}


if not nld.db.exists():
    nld.db.create()
    # NB: Different methods are used for data based on NLE and data from NAO.
    nld.add_nledata_directory("./data", "nld-aa-v0")

toy_ds = nld.TtyrecDataset("nld-aa-v0", batch_size=1)

if True:
    import time
    game_ttyrecs = toy_ds.get_ttyrecs([1], chunk_size=1)
    for t in range(2000):
        tty_chars = game_ttyrecs[t]['tty_chars'][0, 0]
        tty_colors = game_ttyrecs[t]['tty_colors'][0, 0]
        tty_cursor = game_ttyrecs[t]['tty_cursor'][0, 0]
        print(tty_render(tty_chars, tty_colors, tty_cursor))
        time.sleep(1)
    exit()
 
def viz_example_ttyrecs_by_strategy(game_id=1):
    """
    Samples (uniformly at random) and prints visualizations of ttyrecs 
    corresponding to each of the strategies AutoAscend employed while 
    playing the game with id $GAME_ID in the loaded `NLD` dataset `toy_ds`.
    """
    
    game_ttyrecs = toy_ds.get_ttyrecs([1], chunk_size=1)
    
    game_strategies = np.array([game_ttyrecs[i]['strategies'][0, 0] for i in range(len(game_ttyrecs))])
    
    applied_strategies = np.unique(game_strategies)

    for strategy in applied_strategies:
        tty_idxs = np.arange(game_strategies.shape[0])[game_strategies == strategy]
        t = np.random.choice(tty_idxs)

        tty_chars = game_ttyrecs[t]['tty_chars'][0, 0]
        tty_colors = game_ttyrecs[t]['tty_colors'][0, 0]
        tty_cursor = game_ttyrecs[t]['tty_cursor'][0, 0]
        keypresses = game_ttyrecs[t]['keypresses'][0, 0]
        strategies = game_ttyrecs[t]['strategies'][0, 0]

        print(f'[game-id] {game_id}')
        print(f'[keypress-id] {t}')
        print(f'[strategy] {ORDINAL_BACKMAP[strategies]}')
        print(f'[keypress] {NH_ACTION_IDX_TO_STR[keypresses]}')
        print('-' * 80)

        print(tty_render(tty_chars, tty_colors, tty_cursor))
        print('=' * 80)

viz_example_ttyrecs_by_strategy()

exit()

import nle.dataset as nld

if not nld.db.exists():
    nld.db.create()
    # NB: Different methods are used for data based on NLE and data from NAO.
    nld.add_nledata_directory("./data", "nld-aa-v0")

dataset = nld.TtyrecDataset("nld-aa-v0", batch_size=1)
for d in dataset:
    print(d['tty_chars'])
    exit()
