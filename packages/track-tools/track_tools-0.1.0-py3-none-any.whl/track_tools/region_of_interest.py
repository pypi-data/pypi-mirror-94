from typing import Dict, Any, Union, Tuple, List
import os
import glob
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Ellipse
import pims
from read_roi import read_roi_file, read_roi_zip


Roi = Dict[str, Any]
Frames = Union[pims.ImageSequence, pims.TiffStack]
BooleanArray = np.ndarray


def load_rois(files: List[str]) -> List[Roi]:

    valid_files = []
    for f in files:
        g = glob.glob(f, recursive=True)
        if len(g) == 0:
            raise KeyError(f"File or pattern '{f}' "
                           "did not match any files.")
        valid_files += g

    rois = []

    for f in valid_files:
        ext = os.path.splitext(f)[1]
        if ext == '.roi':
            rois += _load_roi(f)
        elif ext == '.zip':
            rois += _load_zipped_rois(f)
        else:
            raise KeyError("ROI files have to either end on "
                           ".roi (single roi) or have to be a "
                           "set of ROI files in a .zip folder. "
                           f"Your file '{f}' does not match.")

    return rois



def apply_rois(frames: Union[np.ndarray, Frames],
               rois: List[Roi]) -> np.ndarray:

    new_frames = np.array(frames)
    mask = get_roi_include_mask(new_frames[0].shape, rois)
    new_frames[:, ~mask] = 0
    return new_frames


def get_roi_include_mask(frame_shape: Tuple[int, int],
                         rois: List[Roi]) -> BooleanArray:

    mask = np.zeros(frame_shape, dtype=int)
    grid = np.mgrid[0:frame_shape[1], 0:frame_shape[0]]
    all_pixels = grid.transpose().reshape(frame_shape[0] * frame_shape[1], 2)

    for roi in rois:
        if roi['type'] == 'polygon' or roi['type'] == 'freehand':
            mask_roi = _get_roi_include_mask_polygon(roi, all_pixels, frame_shape)
        elif roi['type'] == 'oval':
            mask_roi = _get_roi_include_mask_oval(roi, all_pixels, frame_shape)
        else:
            raise NotImplementedError("Can only handle polygon, freehand or oval ROIs, "
                                      f"can't handle '{roi['type']}'")
        mask += mask_roi

    return mask.astype(bool)


def _get_roi_include_mask_polygon(roi: Roi, all_pixels,
                                  frame_shape) -> BooleanArray:
    path = Path([p for p in zip(roi['x'], roi['y'])])
    result = path.contains_points(all_pixels)
    mask_roi = result.reshape(frame_shape[0], frame_shape[1])
    return mask_roi


def _get_roi_include_mask_oval(roi: Roi, all_pixels,
                               frame_shape) -> BooleanArray:
    center = (roi['left'] + 0.5 * roi['width'],
              roi['top'] + 0.5 * roi['height'])
    oval = Ellipse(center, roi['width'], roi['height'])
    result = oval.contains_points(all_pixels)
    mask_roi = result.reshape(frame_shape[0], frame_shape[1])
    return mask_roi


def _load_roi(roi_file: str) -> List[Roi]:
    rois = []
    roi = read_roi_file(roi_file)
    for key in roi.keys():
        rois.append(roi[key])
    return rois


def _load_zipped_rois(zip_file: str) -> List[Roi]:
    roi_dict = read_roi_zip(zip_file)
    return [roi for roi in roi_dict.values()]
