"""
#   Christopher Adleson, SIE, November 2020 for New Horizons mission
#
#   This script converts txt files containgin pixel data int the form of tuples (x, y, value) and saves the image to a fits file
#
#   Usage:          python txt_to_fits.py -d my_txt_files
#                   python txt_to_fits.py --help
# 
#   Usage Example:   python fit_to_binary.py -d directory_of_txt -o my_output_dir

"""

from __future__ import print_function
import fitsio
from fitsio import FITS,FITSHDR
import numpy as np
import os
import sys
import argparse
import glob
from ast import literal_eval


## ------------- Parse Args ------------- ##
DIR = 'dir'
PATHS = 'paths'
OUTDIR = 'outdir'

parser = argparse.ArgumentParser(description='Convert txt files to fits files.')
parser.add_argument('-d', '--%s' % DIR, help='Specify directory where txt files live.', metavar='')
parser.add_argument('-p', '--%s' % PATHS, help='Specify one or more paths for specific txt files.', metavar='', nargs='+')
parser.add_argument('-o', '--%s' % OUTDIR, help='Specify output directory. By default, files are written to the current \
    working directory.', metavar='', default=os.getcwd())
args = parser.parse_args()

if not getattr(args, PATHS) and not getattr(args, DIR):
     print('Please enter either a directory or file path(s)')
     sys.exit()

## ------------- Functions ------------- ##

def validate_paths(dir=None, paths=None):
    
    good_paths, bad_paths = [], []

    if dir is not None:
        if os.path.isdir(dir):
            paths = glob.glob('%s/*.txt' % dir)
        else: 
            raise IOError('Directory \'%s\' does not exist' % dir)

    for p in paths:
        good_paths.append(p) if os.path.exists(p) else bad_paths.append(p)

    return good_paths, bad_paths

def txt_to_fits(paths, outdir):

    for p in sorted(paths):
        # Read tuples from txt file
        with open(p) as tups:
            try:
                # Evaluate tuple strings as tuple type and pack in np array
                data_arr = np.array([literal_eval(tup) for tup in tups])
                
                # Infer image dimensions from x and y counts
                x_dim = int(max(data_arr[:,1])) + 1
                y_dim = int(max(data_arr[:,0])) + 1
                img_data = data_arr[:,2]

                # Reshape image data to x & y dims
                image_arr = np.reshape(img_data, (x_dim,y_dim))
                
                # Write data to fits file
                file_name = '%s/%s.fits' % (outdir, os.path.basename(p)[:-4])
                fitsio.write(file_name, image_arr)
                print('Wrote to %s' % file_name)
            except:
                print('Could not read file: \'%s\'' % p)


## ------------- Main ------------- ##
if __name__ == "__main__":
    good_paths, bad_paths = validate_paths(getattr(args, DIR), getattr(args, PATHS))
    outdir = getattr(args, OUTDIR)

    if bad_paths:
        print('These paths do not exist:', *bad_paths, sep='\n    ')
        cont = raw_input('Continue with valid paths? (y/n): ')
        if cont.lower() == 'n':
            sys.exit()

    if good_paths:
        if outdir is None:
            outdir = os.path.dirname(good_paths[0])
        elif not os.path.isdir(outdir):
            print('Output dir \'%s\' does not exist' % outdir)
            sys.exit()

        txt_to_fits(paths=good_paths,
                    outdir=outdir)