from typing import List

from rs.calculator.hand_state import HandState, Play
from rs.calculator.helper import pickle_deepcopy


class PlayPath:
    def __init__(self, plays: List[Play], state: HandState):
        self.plays: List[Play] = plays
        self.state: HandState = state

    def end_turn(self):
        self.state.end_turn()


def get_paths(path: PlayPath, paths: dict[str, PlayPath]):
    path_state = path.state.get_state_hash()
    if path_state in paths:
        return
    paths[path_state] = path
    for play in path.state.get_plays():
        new_state: HandState = pickle_deepcopy(path.state)
        new_state.transform_from_play(play)
        new_plays: List[Play] = path.plays.copy()
        new_plays.append(play)
        new_path: PlayPath = PlayPath(new_plays, new_state)
        get_paths(new_path, paths)