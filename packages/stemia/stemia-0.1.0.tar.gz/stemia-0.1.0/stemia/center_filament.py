from pathlib import Path
import warnings

import numpy as np
from scipy.spatial.distance import cdist
from skimage.morphology import skeletonize, remove_small_objects
import click

from .utils import read_mrc, write_mrc, read_particle_star

from .functions import (
    binarise,
    to_positive,
    label_features,
    features_by_size,
    fourier_translate,
    rotations,
    crop_center,
    coerce_ndim,
)


def center_filament(img, n_filaments=2, percentile=85):
    """
    center an image containing one or more filaments, and rotate it vertically
    percentile: used for binarisation
    """
    dtype = img.dtype
    binarised = binarise(to_positive(img), percentile)
    labeled, by_size = features_by_size(binarised)
    threshold = by_size[n_filaments - 1].sum()
    clean = remove_small_objects(labeled, min_size=threshold)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=UserWarning)
        skel = skeletonize(clean, method='lee')

    # find centroid of all the "centers" of the filaments
    skel_labeled, count = label_features(skel)
    centers = []
    center = np.array(img.shape) / 2
    for lb in count:
        feature_indexes = np.stack(np.where(skel_labeled == lb), axis=1)
        closest = cdist(feature_indexes, [center]).argmin()
        centers.append(feature_indexes[closest])
    centroid = np.stack(centers).mean(axis=0)

    # translate image
    shift = center - centroid
    trans = fourier_translate(img, shift)

    # find best rotation
    best_rot = None
    best_peak = -1000
    best_angle = 0
    for angle, img_rot in rotations(trans, range(-90, 91)):
        rot_crop = crop_center(img_rot, 0.3, axis='y')
        parts = np.split(rot_crop, n_filaments, axis=1)     # may break with n > 3 and non-even spacing
        peaks = [part.sum(axis=0).max() for part in parts]
        peak = sum(peaks)
        peak = rot_crop.sum(axis=0).max()
        if peak > best_peak:
            best_rot = img_rot
            best_angle = angle
            best_peak = peak

    # back to original type?
    best_rot = best_rot.astype(dtype)

    return best_rot, shift, best_angle


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('input', type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.argument('output', type=click.Path(dir_okay=False, resolve_path=True), required=False)
@click.option('-s', '--update-star', 'starfile', type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help='a RELION .star file to update with new particle positions')
@click.option('--update-by', type=click.Choice(['class', 'particle']), default='class', show_default=True,
              help='whether to update particle positions by classes or 1 by 1. Only used if -s is passed')
@click.option('-f', '--overwrite', is_flag=True, help='overwrite output if exists')
@click.option('-n', '--n-filaments', default=2, help='number of filaments on the image', show_default=True)
@click.option('-p', '--percentile', default=85, help='percentile for binarisation', show_default=True)
def main(input, output, starfile, update_by, n_filaments, percentile, overwrite):
    """
    Center an mrc image containing filament(s). Can update particles in a RELION .star file accordingly.

    If OUTPUT is not given, default to INPUT_centered.mrc
    """
    # don't waste time processing if overwrite is off and output exists
    output = output or Path(input).stem + '_centered.mrc'
    if Path(output).is_file() and not overwrite:
        raise click.UsageError(f'{output} exists but "-f" flag was not passed')
    # make sure starfile is readable
    if starfile:
        df = read_particle_star(starfile)

    imgs, header = read_mrc(input)
    imgs = coerce_ndim(imgs, ndim=3)

    out_imgs = []
    shifts = []
    angles = []
    failed = []
    with click.progressbar(enumerate(imgs), label='Processing image slices', length=len(imgs)) as images:
        for i, img in images:
            try:
                centered, shift, angle = center_filament(img, n_filaments, percentile)
            except IndexError:
                failed.append(i)
                centered = img
                shift = angle = 0
            out_imgs.append(centered)
            shifts.append(shift)
            angles.append(angle)

    out_imgs = np.squeeze(np.stack(out_imgs))

    if failed:
        click.secho(f'WARNING: could not find {n_filaments} filaments in the following images:\n'
                    f'{failed}\nWill leave as is!', fg='red')


    if starfile:
        df
        breakpoint()

    write_mrc(out_imgs, output, overwrite=overwrite, from_header=header)
