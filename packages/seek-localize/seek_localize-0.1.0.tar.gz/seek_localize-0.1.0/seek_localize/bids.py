import json
import os
import platform
import warnings
from collections import OrderedDict
from pathlib import Path
from typing import Union, List

import numpy as np
from mne.utils import run_subprocess
from mne_bids import get_entities_from_fname, BIDSPath
from mne_bids.config import BIDS_COORDINATE_UNITS
from mne_bids.tsv_handler import _from_tsv
from mne_bids.utils import _write_json, _write_tsv

from seek_localize.electrodes import Sensors


def _suffix_chop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def _match_dig_sidecars(bids_path):
    """Match the sidecar files that define iEEG montage.

    Returns the filepath to ``electrodes.tsv`` and
    ``coordsystem.json`` files.
    """
    electrodes_fnames = BIDSPath(
        subject=bids_path.subject,
        session=bids_path.session,
        suffix="electrodes",
        extension=".tsv",
        root=bids_path.root,
    ).match()

    if len(electrodes_fnames) != 1:
        raise ValueError(
            f"Trying to load electrodes.tsv "
            f"file using {bids_path}, but there "
            f"are multiple files "
            f"electrodes.tsv. Please "
            f"uniquely specify it using additional "
            f"BIDS entities."
        )
    elec_fname = electrodes_fnames[0]
    coord_fname = elec_fname.copy().update(suffix="coordsystem", extension=".json")
    if not coord_fname.fpath.exists():
        raise ValueError(
            f"Corresponding coordsystem.json file does not exist "
            f"for {elec_fname}. Please check BIDS dataset."
        )
    return elec_fname, coord_fname


def _read_elecs_tsv(elecs_fname, as_dict=False):
    """Read electrodes.tsv file in.

    Only reads in ch names and coordinates.
    """
    # read in elecs_fname
    elecs_tsv = _from_tsv(elecs_fname)

    x, y, z = [], [], []
    ch_names = []
    x_coord = elecs_tsv["x"]
    y_coord = elecs_tsv["y"]
    z_coord = elecs_tsv["z"]
    for idx, ch_name in enumerate(elecs_tsv["name"]):
        ch_names.append(ch_name)
        x.append(x_coord[idx])
        y.append(y_coord[idx])
        z.append(z_coord[idx])

    if as_dict:
        ch_coords = {
            ch_name: (_x, _y, _z) for ch_name, _x, _y, _z in zip(ch_names, x, y, z)
        }
        return ch_coords

    return ch_names, x, y, z


def _read_coords_json(coordsystem_fname):
    """Read coordsystem.json file in.

    Only reads in the ``iEEGCoordinateSystem``.
    TODO: add better checking for coordinate system and frames
    from MNE <-> BIDS
    """
    with open(coordsystem_fname, "r") as fin:
        coordsystem_json = json.load(fin)
    coord_system = coordsystem_json["iEEGCoordinateSystem"]
    unit = coordsystem_json["iEEGCoordinateUnits"]
    # if coord_frame not in ACCEPTED_MNE_COORD_FRAMES:
    #     raise ValueError(f'Coord frame {coord_frame} '
    #                      f'from mne-python is not supported yet... '
    #                      f'Please make sure coordinate frame is one of '
    #                      f'{ACCEPTED_MNE_COORD_FRAMES}.')

    # convvert coordinate frame to coordinate system string
    # coord_system = MNE_TO_BIDS_FRAMES.get(coord_frame)
    return coord_system, unit


def read_dig_bids(elecs_fname, coordsystem_fname, intended_for: str = None):
    """Read electrode coordinates from BIDS files.

    TODO: improve to error check coordinatesystem.

    Parameters
    ----------
    elecs_fname : str | pathlib.Path
        File path to the electrodes.tsv file.
    coordsystem_fname : str | pathlib.Path
        File path to the coordsystem.json file.
    intended_for : str | None
        Optional parameter to tell function path of the Nifti image
        to interpret sensor coordinates for.

    Returns
    -------
    sensors : seek_localize.Sensors
        A data class containing the electrode sensors.
    """
    # read in elecs_fname
    ch_names, x, y, z = _read_elecs_tsv(elecs_fname)

    # read in the coordinate system json
    # coord_system, unit = _read_coords_json(coordsystem_fname)
    with open(coordsystem_fname, "r") as fin:
        coordsystem_json = json.load(fin)
    coord_system = coordsystem_json["iEEGCoordinateSystem"]
    unit = coordsystem_json["iEEGCoordinateUnits"]

    # get the BIDS root
    entities = get_entities_from_fname(elecs_fname)
    elecs_bids_path = BIDSPath(**entities, datatype="ieeg", extension=".tsv").fpath
    root = _suffix_chop(str(elecs_fname), str(elecs_bids_path))

    # try to get the BIDS Path to the image file that
    # the coordinates are intended to be interpreted for
    intended_for_fname = coordsystem_json.get("IntendedFor")
    if intended_for_fname:
        entities = get_entities_from_fname(intended_for_fname)
        intended_img_path = BIDSPath(**entities, root=root)
    elif intended_for is not None:
        intended_img_path = intended_for
    else:
        raise RuntimeError(
            f"IntendedFor inside {coordsystem_fname} "
            f"is not available, and ``intended_for`` "
            f"kwarg is not set. Please set "
            f"``intended_for``."
        )

    # get the coordinates and set
    # montage_coords = montage.get_positions()
    # ch_pos = montage_coords.get('ch_pos')
    # for ch_name, coord in ch_pos.items():
    #     ch_names.append(ch_name)
    #     x.append(coord[0])
    #     y.append(coord[1])
    #     z.append(coord[2])

    # get the coordinate frame in mne
    # XXX: Possible coordframes subject to change in mne
    # mri=FIFF.FIFFV_COORD_MRI,
    # mri_voxel=FIFF.FIFFV_MNE_COORD_MRI_VOXEL,
    # head=FIFF.FIFFV_COORD_HEAD,
    # mni_tal=FIFF.FIFFV_MNE_COORD_MNI_TAL,
    # ras=FIFF.FIFFV_MNE_COORD_RAS,
    # fs_tal=FIFF.FIFFV_MNE_COORD_FS_TAL,
    # coord_frame = ch_pos.get('coord_frame')
    sensors = Sensors(
        ch_names,
        x,
        y,
        z,
        coord_system=coord_system,
        elecs_fname=elecs_fname,
        coordsystem_fname=coordsystem_fname,
        coord_unit=unit,
        intended_for=intended_img_path,
    )
    return sensors


def bids_validate(bids_root):
    """Run BIDS validator."""
    shell = False
    bids_validator_exe = ["bids-validator", "--config.error=41", "--conwfig.error=41"]
    if platform.system() == "Windows":
        shell = True
        exe = os.getenv("VALIDATOR_EXECUTABLE", "n/a")
        if "VALIDATOR_EXECUTABLE" != "n/a":
            bids_validator_exe = ["node", exe]

    def _validate(bids_root):
        cmd = bids_validator_exe + [bids_root]
        run_subprocess(cmd, shell=shell)

    return _validate(bids_root)


def write_coordsystem_json(
    fname: Union[str, Path],
    unit: str,
    coordsystem: str = None,
    img_bids_path: str = None,
    coordsystem_description: str = None,
    overwrite: bool = True,
    verbose: bool = True,
):
    """Write coordsystem.json dictionary contents to disc.

    Parameters
    ----------
    fname : str | pathlib.Path
        Filepath for the ``*coordsystem.json`` file. Must
        follow BIDS-naming conventions.
    unit : str
        Units of the _electrodes.tsv, MUST be "m", "mm", "cm" or "pixels".
        Corresponds to ``iEEGCoordinateUnits`` in iEEG-BIDS.
    coordsystem : str
        The coordinate system of the sensors. Corresponds to
        ``iEEGCoordinateSystem`` in iEEG-BIDS. For example, it might be
        ``'ACPC'``, or ``'Other'``, or ``'Image'``. If it is ``'Other'``,
        then ``coordsystem_description`` must not be ``None``.
        If it is ``'Image'``, then ``img_fname`` must not be None.
    img_bids_path : str | None
        The relative BIDS filepath of the associated image for the
        coordinates. Corresponds to ``IntendedFor`` in iEEG-BIDS.
        For example: ``sub-<label>/ses-<label>/anat/sub-01_T1w.nii.gz``.
    coordsystem_description : str | None
        The description of the coordinate system. Corresponds to
        ``iEEGCoordinateSystemDescription`` in iEEG-BIDS.
    overwrite : bool
        Whether to overwrite an existing file, or not.
    verbose : bool
        Verbosity.

    Notes
    -----
    coordsystem_description could be "FreeSurfer Coordinate System derived
    from the CT, or T1 MRI scan."
    """
    if unit not in BIDS_COORDINATE_UNITS:
        raise ValueError(
            f"Units of the sensor positions must be one "
            f"of {BIDS_COORDINATE_UNITS}. You passed in "
            f"{unit}."
        )

    if coordsystem == "Other" and coordsystem_description is None:
        raise RuntimeError(
            'If coordsystem is "Other", then coordsystem_description '
            "must be passed in describing the coordinate system "
            "in Free-form text. May also include a link to a "
            "documentation page or paper describing the system in "
            "greater detail."
        )

    if coordsystem == "Image" and img_bids_path is None:
        raise RuntimeError(
            'If coordsystem is "Image", then img_fname '
            "must be passed in as the filename of the corresponding "
            "image the data is in. For example"
        )

    # check that filename adheres to BIDS naming convention
    entities = get_entities_from_fname(fname, on_error="raise")

    processing_description = "SEEK-algorithm (thresholding, cylindrical clustering and post-processing), or manual labeling of contacts using FieldTrip Toolbox."

    # if img_bids_path is not None:
    #     # load in image and determine coordinate system
    #     img = nb.load(img_bids_path)
    # axcodes = nb.orientations.aff2axcodes(img.affine)
    # coordsystem_name = "".join(axcodes)
    if img_bids_path is None:
        img_bids_path = "n/a"
        warnings.warn(
            "Image filename not passed in... Defaulting to MRI coordinate system."
        )

    # write the JSON
    fid_json = {
        "IntendedFor": img_bids_path,
        "iEEGCoordinateSystem": coordsystem,  # MRI, Pixels, or ACPC
        "iEEGCoordinateUnits": unit,  # m (MNE), mm, cm , or pixels
        "iEEGCoordinateSystemDescription": coordsystem_description,
        "iEEGCoordinateProcessingDescription": processing_description,
        "iEEGCoordinateProcessingReference": "See DOI: https://zenodo.org/record/3542307#.XoYF9tNKhZI "
        "and FieldTrip Toolbox: doi:10.1155/2011/156869",
    }
    _write_json(fname, fid_json, overwrite, verbose)


def write_electrodes_tsv(
    fname: Union[str, Path],
    ch_names: Union[List, np.ndarray],
    coords: Union[List, np.ndarray],
    sizes: Union[List, np.ndarray] = None,
    hemispheres: Union[List, np.ndarray] = None,
    overwrite: bool = False,
    verbose: bool = True,
):
    """
    Create an electrodes.tsv file and save it.

    Parameters
    ----------
    fname : str | pathlib.Path
        Filepath for the ``*electrodes.tsv`` file. Must
        follow BIDS-naming conventions.
    names : list | np.ndarray
        Name of the electrode contact point. Corresponds to
        ``name`` in iEEG-BIDS for electrodes.tsv file.
    coords : list | np.ndarray
        List of sensor xyz positions. Corresponds to
        ``x``, ``y``, ``z`` in iEEG-BIDS for electrodes.tsv file.
    sizes : list | np.ndarray | None
        Size of the electrode contact point. Corresponds to
        ``size`` in iEEG-BIDS for electrodes.tsv file.
    hemispheres  : list | np.ndarray | None
        Hemisphere of the electrode contact point. Corresponds to
        ``hemisphere`` in iEEG-BIDS for electrodes.tsv file.
        Must be either ``'L'``, or ``'R'``.
    overwrite : bool
        Defaults to False.
        Whether to overwrite the existing data in the file.
        If there is already data for the given `fname` and overwrite is False,
        an error will be raised.
    verbose :  bool
        Set verbose output to true or false.
    """
    if len(ch_names) != len(coords):
        raise RuntimeError(
            "Number of channel names should match "
            "number of coordinates passed in. "
            f"{len(ch_names)} names and {len(coords)} coords passed in."
        )

    if sizes is not None:
        if len(sizes) != len(ch_names):
            raise RuntimeError(
                "Number of channel names should match "
                "number of sizes passed in. "
                f"{len(ch_names)} names and {len(sizes)} sizes passed in."
            )

    # check that filename adheres to BIDS naming convention
    entities = get_entities_from_fname(fname, on_error="raise")

    x, y, z, names = list(), list(), list(), list()
    for name, coord in zip(ch_names, coords):
        x.append(coord[0])
        y.append(coord[1])
        z.append(coord[2])
        names.append(name)

    if sizes is None:
        sizes = ["n/a"] * len(ch_names)
    if hemispheres is None:
        hemispheres = ["n/a"] * len(ch_names)

    data = OrderedDict(
        [
            ("name", names),
            ("x", x),
            ("y", y),
            ("z", z),
            ("size", sizes),
            ("hemisphere", hemispheres),
        ]
    )

    if verbose:
        print(f"Writing data to {fname}: ")
        print(data)

    _write_tsv(fname, data, overwrite=overwrite, verbose=verbose)
