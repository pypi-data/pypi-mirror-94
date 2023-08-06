import argparse
from typing import Tuple, Union, List
import glob
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
import pandas as pd
import pims
import trackpy as tp
from .. import results_folder as rf
from ..tracking_parameters import TrackingParameters
from ..region_of_interest import load_rois, apply_rois

Frames = Union[pims.ImageSequence, pims.TiffStack]


def main():
    parser = argparse.ArgumentParser(
        description=("Extract trajectories of moving particles from"
                     " tiff sequence.")
    )
    parser.add_argument("file_pattern", metavar="file-pattern")
    parser.add_argument("-o", "--output-dir", default=None,
                        help=("save results in this folder " 
                              "instead of one deduced from the file name"))
    parser.add_argument("-i", "--invert", action='store_true',
                        help="Invert brightness")
    parser.add_argument('-r', '--rois', nargs='+')
    args = parser.parse_args()
    file_pattern = args.file_pattern
    output_dir = args.output_dir
    rois = args.rois

    print("{:=^80}".format(" track-tools-extract-trajectories "))
    mpl.rc('figure', figsize=(10, 8))
    mpl.rc('image', cmap='gray')

    files, frames = load_frames(file_pattern)

    if rois is not None:
        rois = load_rois(rois)
        frames = apply_rois(frames, rois)

    if output_dir is None:
        results_folder = rf.get_results_folder(files[0])
    else:
        results_folder = output_dir
        os.makedirs(output_dir, exist_ok=True)
    param_log, parameters = _set_initial_parameters(results_folder, invert=args.invert)

    param_finder = InteractiveParameterFinder(parameters)
    param_finder.start(frames)
    parameters.save_to_default_file()

    print()
    txt = "set parameters to:\n{}"
    print(txt.format(parameters.as_string()))

    choice = input("track trajectories now with these parameters? [Y/n]: ")
    if not choice:
        choice = 'y'
    print()
    if choice.lower().strip() != 'y':
        return

    idx_analysis = rf.add_tracking_parameters(param_log, parameters)
    ana_folder = rf.get_analysis_folder(results_folder, idx_analysis)
    parameters.save_to_file(os.path.join(ana_folder, 'tracking_parameters.json'))
    rf.save_parameter_csv(param_log, results_folder)
    fname_traj = os.path.join(ana_folder, 'trajectories.csv')

    if os.path.exists(fname_traj):
        choice = input(' '.join(["Trajectory file for your set of parameters already exits.\n",
                                 "Continue and overwrite? [y/N]: "]))
        if choice.lower().strip() != 'y':
            return
    print("tracking particles ... ", end='')

    trajectories = extract_trajectories(frames, parameters)

    print('done')
    print("got {} trajectories".format(trajectories['particle'].nunique()))
    print("")
    print("saving to file '{}'".format(fname_traj))
    trajectories.to_csv(fname_traj)


def extract_trajectories(frames, tracking_parameters) -> pd.DataFrame:
    tparams = tracking_parameters
    features = tp.batch(frames, tparams.diameter,
                        minmass=tparams.mass, invert=tparams.invert,
                        engine='numba')
    traj = tp.link_df(features, tparams.max_distance,
                      memory=tparams.memory)

    trajectories = tp.filter_stubs(traj, tparams.traj_min_n_frames)
    return trajectories


def _set_initial_parameters(
        results_folder, diameter=None,
        mass=None, memory=None,
        max_distance=None,
        traj_min_n_frames=None,
        invert: bool=False
) -> Tuple[pd.DataFrame, TrackingParameters]:
    param_log = rf.load_parameter_csv(results_folder)
    last_params = rf.load_last_tracking_parameters(param_log)

    if diameter is None:
        diameter = last_params.diameter
    if mass is None:
        mass = last_params.mass
    if memory is None:
        memory = last_params.memory
    if max_distance is None:
        max_distance = last_params.max_distance
    if traj_min_n_frames is None:
        traj_min_n_frames = last_params.traj_min_n_frames

    parameters = TrackingParameters(diameter, mass,
                                    memory, max_distance, traj_min_n_frames,
                                    invert)
    return param_log, parameters


class InteractiveParameterFinder:

    def __init__(self, parameters):
        self.parameters = parameters
        self._current_frame = 0
        self.frames = None
        self.fig = None
        self.aximg = None
        self.axhist = None
        self.box_diameter = None
        self.box_mass = None

    def start(self, frames: Frames):
        self.frames = frames
        self.fig, (self.aximg, self.axhist) = plt.subplots(1, 2)
        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.42)
        self.fig.canvas.mpl_connect('button_press_event', self._onclick)
        # ====================== set up frame slider ===========================
        axcolor = 'salmon'
        axframe = self.fig.add_axes([0.15, 0.35, 0.65, 0.03], facecolor=axcolor)
        sframe = Slider(axframe, 'Frame', 0, len(self.frames), valstep=1, valfmt='%d',
                        color='lightblue')
        sframe.on_changed(self._set_current_frame)
        # ====================== set up diameter text box ======================
        axbox_d = self.fig.add_axes([0.15, 0.25, 0.3, 0.075])
        self.box_diameter = TextBox(axbox_d, 'diameter',
                                    initial=str(self.parameters.diameter))
        self.box_diameter.on_submit(self._set_diameter)
        # ====================== set up mass text box ==========================
        axbox_m = self.fig.add_axes([0.6, 0.25, 0.3, 0.075])
        self.box_mass = TextBox(axbox_m, 'mass', initial=str(self.parameters.mass))
        self.box_mass.on_submit(self._set_mass)
        # ====================== set up  boxes for memory and max_distance =====
        self.fig.text(0.1, 0.21, ' '.join(['The following values won\'t change the plots,',
                                           'but will be used for tracking later:']),
                      size=12, color='darkred')
        axbox_mem = self.fig.add_axes([0.15, 0.11, 0.3, 0.075])
        box_mem = TextBox(axbox_mem, 'memory', initial=str(self.parameters.memory))
        box_mem.on_submit(self._set_memory)
        axbox_md = self.fig.add_axes([0.6, 0.11, 0.3, 0.075])
        box_md = TextBox(axbox_md, 'max. dist.', initial=str(self.parameters.max_distance))
        box_md.on_submit(self._set_max_distance)
        # ====================== set up traj-min-nframes text box ==============
        axbox_trajn = self.fig.add_axes([0.35, 0.02, 0.3, 0.075])
        box_trajn = TextBox(axbox_trajn, 'traj. min. number of frames',
                            initial=str(self.parameters.traj_min_n_frames))
        box_trajn.on_submit(self._set_trajn)

        self.update()
        plt.show(block=True)

    def _onclick(self, event):
        ax = event.inaxes
        if ax is None:
            return
        if ax != self.axhist:
            return
        self.parameters.mass = event.xdata
        self.box_mass.set_val(self.parameters.mass)
        self.update()

    def _set_trajn(self, value_str):
        self.parameters.traj_min_n_frames = int(value_str)

    def _set_memory(self, value_str):
        self.parameters.memory = int(value_str)

    def _set_max_distance(self, value_str):
        self.parameters.max_distance = float(value_str)

    def _set_mass(self, value_str):
        self.parameters.mass = float(value_str)
        self.update()

    def _set_diameter(self, value_str):
        d = int(value_str)
        if d % 2 == 0:
            msg = "You set an even number for diameter, which is invalid! "
            msg += "It was now incremented by 1."
            print(msg)
            d += 1
            self.box_diameter.set_val(str(d))
        if d <= 1:
            msg = (f"You set diameter to {d}, but "
                   "diameter needs to be uneven and greater than 2. "
                   "Will set it to 3 now.")
            print(msg)
            d = 3
            self.box_diameter.set_val(str(d))
        self.parameters.diameter = d
        self.update()

    def _set_current_frame(self, value):
        self._current_frame = int(value)
        self.update()

    def update(self):
        frame = self.frames[self._current_frame]
        self.aximg.clear()
        self.axhist.clear()
        features = tp.locate(frame, self.parameters.diameter,
                             minmass=self.parameters.mass,
                             invert=self.parameters.invert)
        
        tp.annotate(features, frame, invert=self.parameters.invert, ax=self.aximg,
                    imshow_style={'origin': 'lower'})
        self.axhist.hist(features['mass'], bins=20)
        self.fig.canvas.draw()
        

def load_frames(file_pattern: str) -> Tuple[List[str], Frames]:
    files = sorted(glob.glob(file_pattern))
    if len(files) == 0:
        msg = "No files were found with file pattern or name '{}'"
        raise FileNotFoundError(msg.format(file_pattern))
    if len(files) == 1:
        if _is_tiff(files[0]):
            frames = pims.TiffStack(files[0])
        elif _is_video(files[0]):
            frames = pims.Video(files[0])
        else:
            msg = "File is not a tiff (allowed extensions = ['.tif', '.tiff']),\n"
            msg += "or a video (allowed extensions = ['avi']).\n"
            msg += "Other formats are not supported yet. Mail me to ikuhlem@gwdg.de "
            msg += "if you want your format added."
            raise RuntimeError(msg)
    else:
        frames = pims.ImageSequence(files)
    return files, frames


def _is_tiff(fname: str) -> bool:
    allowed_extensions = ['.tif', '.tiff']
    extension = os.path.splitext(fname)[1]
    if extension.lower() in allowed_extensions:
        return True
    return False


def _is_video(fname: str) -> bool:
    allowed_extensions = ['.avi']
    extension = os.path.splitext(fname)[1]
    if extension.lower() in allowed_extensions:
        return True
    return False
