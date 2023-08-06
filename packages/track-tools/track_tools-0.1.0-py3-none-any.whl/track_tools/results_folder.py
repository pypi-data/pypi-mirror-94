from typing import Tuple
import os
import json
import pandas as pd
from .tracking_parameters import TrackingParameters


def get_results_folder(fname_data: str) -> str:
    fname_wo_ext = os.path.splitext(fname_data)[0]
    results_folder = fname_wo_ext + "_track_results"
    if not os.path.exists(results_folder):
        os.mkdir(results_folder)
    return results_folder


def load_parameter_csv(results_folder: str) -> pd.DataFrame:
    fname_param = os.path.join(results_folder, 'parameters.csv')
    if os.path.exists(fname_param):
        return pd.read_csv(fname_param, index_col=0)
    param_df = pd.DataFrame(columns=['diameter',
                                     'mass', 'memory',
                                     'max_distance',
                                     'trajectory_min_frames'])
    return param_df


def save_parameter_csv(params: pd.DataFrame, results_folder):
    fname_param = os.path.join(results_folder, 'parameters.csv')
    params.to_csv(fname_param)


def load_conversion_parameters(results_folder: str) -> Tuple[float, float]:
    fname_conv_params = os.path.join(results_folder, 'conversion_params.json')
    with open(fname_conv_params, 'rt') as fp:
        j = json.load(fp)
    return j['microns_per_pixel'], j['frames_per_second']


def save_conversion_parameters(results_folder: str, microns_per_pixel: float,
                               frames_per_second: float):
    fname_conv_params = os.path.join(results_folder, 'conversion_params.json')
    j = {'microns_per_pixel': microns_per_pixel,
         'frames_per_second': frames_per_second}
    with open(fname_conv_params, 'wt') as fp:
        json.dump(j, fp)


def add_tracking_parameters(params: pd.DataFrame,
                            tp: TrackingParameters) -> int:
    params.loc[len(params)] = [tp.diameter,
                               tp.mass,
                               tp.memory,
                               tp.max_distance,
                               tp.traj_min_n_frames]
    return len(params)-1


def load_last_tracking_parameters(params: pd.DataFrame) -> TrackingParameters:
    if len(params):
        p = params.loc[len(params)-1]
        t = TrackingParameters(int(p['diameter']), p['mass'],
                               int(p['memory']), p['max_distance'],
                               int(p['trajectory_min_frames']),
                               invert=False)
        return t
    return TrackingParameters.load_from_default_file()


def get_analysis_folder(results_folder: str, idx: int):
    ana_folder = os.path.join(results_folder, 'analysis_{:03}'.format(idx))
    if not os.path.exists(ana_folder):
        os.mkdir(ana_folder)
    return ana_folder
