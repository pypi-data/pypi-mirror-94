from typing import Dict, Union, Tuple
import os
import json

ParamTuple = Tuple[int, float, int, float, int]

HOME = os.path.abspath(os.path.expanduser('~'))
GLOBAL_FOLDER = os.path.join(HOME, '.config', 'track-tools')
DEFAULT_PARAMS_FNAME = 'default_track_params.json'


class TrackingParameters:

    def __init__(self, diameter: int, mass: float,
                 memory: int, max_distance: float, traj_min_n_frames: int,
                 invert: bool):
        self.diameter = diameter
        self.mass = mass
        self.memory = memory
        self.max_distance = max_distance
        self.traj_min_n_frames = traj_min_n_frames
        self.invert = invert

    def save_to_file(self, fname: str):
        with open(fname, 'wt') as fp:
            json.dump(self.as_dict(), fp)

    def save_to_default_file(self):
        fname_default = os.path.join(GLOBAL_FOLDER, DEFAULT_PARAMS_FNAME)
        with open(fname_default, 'wt') as fp:
            json.dump(self.as_dict(), fp)

    def as_dict(self) -> Dict[str, Union[int, float]]:
        return {'diameter': self.diameter,
                'mass': self.mass,
                'memory': self.memory,
                'max_distance': self.max_distance,
                'traj_min_n_frames': self.traj_min_n_frames}

    def as_string(self) -> str:
        s = """diameter          = {}
mass              = {}
memory            = {}
max_distance      = {}
traj_min_n_frames = {}"""
        return s.format(self.diameter, self.mass,
                        self.memory, self.max_distance,
                        self.traj_min_n_frames)

    @staticmethod
    def load_from_file(fname: str):
        with open(fname, 'rt') as fh:
            params = json.load(fh)
        return TrackingParameters(params['diameter'], params['mass'],
                                  params['memory'], params['max_distance'],
                                  params['traj_min_n_frames'])

    @staticmethod
    def load_from_default_file():
        fname_default = os.path.join(GLOBAL_FOLDER, DEFAULT_PARAMS_FNAME)
        if not os.path.exists(fname_default):
            os.makedirs(GLOBAL_FOLDER, exist_ok=True)
            params = {'diameter': 11, 'mass': 800.0,
                      'memory': 20, 'max_distance': 10.0, 'traj_min_n_frames': 50}
            with open(fname_default, 'wt') as fp:
                json.dump(params, fp)
        return TrackingParameters.load_from_file(fname_default)

