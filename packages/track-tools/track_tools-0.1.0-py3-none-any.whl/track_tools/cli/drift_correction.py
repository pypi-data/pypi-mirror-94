import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import TextBox
import trackpy as tp
from trackpy.motion import compute_drift, subtract_drift


def main():
    parser = argparse.ArgumentParser(
        description=("Perform drift correction for trajectories in given "
                     "analysis folder (folder created by "
                     "track-tools-extract-trajectories)")
    )
    parser.add_argument('analysis_folder', metavar="analysis-folder")
    args = parser.parse_args()
    analysis_folder = args.analysis_folder

    print()
    print("track-tools drift correction")
    print("----------------------------")

    trajectory_file = os.path.join(analysis_folder, 'trajectories.csv')
    corrected_trajectory_file = os.path.join(analysis_folder,
                                             'drift_corrected_trajectories.csv')
    drift_smoothing_file = os.path.join(analysis_folder,
                                        'drift_smoothing.txt')

    if not os.path.exists(trajectory_file):
        msg = (f"Folder '{analysis_folder}', does not contain a file "
               "trajectories.csv => it is no valid analysis folder.")
        raise KeyError(msg)

    initial_smoothing = _load_drift_smoothing_value(drift_smoothing_file)

    trajectories = pd.read_csv(trajectory_file)

    corrector = _InteractiveDriftCorrector(trajectories, initial_smoothing)
    corrected_trajectories = corrector()

    print()
    print('corrected with smoothing =', corrector.smoothing)
    print()
    print(f'writing corrected trajectories to "{corrected_trajectory_file}"')

    corrected_trajectories.to_csv(corrected_trajectory_file)
    with open(drift_smoothing_file, 'wt') as fh:
        fh.write(str(corrector.smoothing))

    print()
    print("Done. OKTHXBYE")
    print("==============")


class _InteractiveDriftCorrector:

    def __init__(self, trajectories, smoothing):

        self.trajectories = trajectories
        self.smoothing = smoothing
        self.corrected_trajectories = None

        self.fig = None
        self.ax_drift = None
        self.ax_corrected = None
        self.box_smoothing = None

    def __call__(self) -> pd.DataFrame:
        return self.run()

    def run(self) -> pd.DataFrame:
        self.fig = plt.figure(figsize=(13, 8))
        ax_trajectories = self.fig.add_subplot(1, 3, 2)
        self.ax_drift = self.fig.add_subplot(1, 3, 1)
        self.ax_corrected = self.fig.add_subplot(1 ,3, 3,
                                                 sharex=ax_trajectories,
                                                 sharey=ax_trajectories)

        for axi in [ax_trajectories, self.ax_corrected]:
            axi.set_aspect('equal')

        ax_trajectories.set_title('trajectories')

        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.21, left=0.08, top=0.85)


        tp.plot_traj(self.trajectories, ax=ax_trajectories)

        ax_box = self.fig.add_axes([0.1, 0.05, 0.2, 0.075])
        self.box_smoothing = TextBox(ax_box, 'smoothing',
                                     initial=str(self.smoothing))
        self.box_smoothing.on_submit(self._set_smoothing)


        self.update()

        plt.show(block=True)
        return self.corrected_trajectories

    def _set_smoothing(self, value_str):
        s = int(value_str)
        self.smoothing = s
        self.update()

    def update(self):

        self.ax_drift.clear()
        self.ax_corrected.clear()

        drift = compute_drift(self.trajectories, self.smoothing)
        drift.plot(ax=self.ax_drift)

        self.corrected_trajectories = subtract_drift(self.trajectories, drift)
        tp.plot_traj(self.corrected_trajectories, ax=self.ax_corrected)

        self.ax_drift.set_title('drift')
        self.ax_corrected.set_title('corrected')

        self.fig.canvas.draw()



def _load_drift_smoothing_value(filename: str) -> int:
    if not os.path.exists(filename):
        return 0
    with open(filename, 'rt') as fh:
        s = int(fh.read())
    return s

