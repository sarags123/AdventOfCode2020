# Helper file to convert FITS data into a *.h asset for use in C code
# Created for the New Horizons Mission
#
# Author: Amanda Voegtlin, SIE-3, September 2020, amanda.voegtlin@jhuapl.edu
# 
# Usage:    python convert_fit_to_c.py [directory of FITS files]
# Example:  python convert_fit_to_c.py quaoar_133g_L1_30s_first10
# 
# Note: The output file is named for the third argument, 
#   so it is preferable to run this program from the same directory where the *.fit file 
#   directories are kept.

import fitsio
from fitsio import FITS,FITSHDR
import numpy as np
import os
import sys
from bitstring import BitArray

# ----------- Helper functions -----------

# Retrieve all fits file names from the directory and return an array of their names
def get_fit_files_from_dir(dir_name):
    file_list = []
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".fit"):
                file_list.append(os.path.join(root, file))
    # Ensure that file list is returned in sorted order
    file_list.sort()
    for file in file_list:
        print file         
    return file_list

# Detect instrument type from first file in directory, returns instrument type identifier
def get_instrument_type(src_file): 
    header = fitsio.read_header(src_file)
    instrument = header.get('INSTRU')
    if "lor" in instrument:
        print ("LORRI instrument type detected")
        instrument_type = "LORRI_DT2"
        IMAGE_X_LEN = 257
        IMAGE_Y_LEN = 256

    elif "mvic" in instrument: # TODO: this is a STUB. Confirm all facts about MVIC, this is copy of LORRI
        print ("MVIC instrument type detected")
        instrument_type = "MVIC_DT4"
        IMAGE_X_LEN = 257
        IMAGE_Y_LEN = 256
    else: 
        print "Unknown instrument type: " + str(instrument) + ", this program will convert LORRI or MVIC images only."
        sys.exit()
    return instrument_type, IMAGE_X_LEN, IMAGE_Y_LEN     

# Create or clobber a new file, place its header information, then reopen in append mode and process all files
def create_c_header_from_fits_files(src_file_list, directory_name, IMAGE_X_LEN, IMAGE_Y_LEN, instrument_type):
    file_name = directory_name + ".h"
    f = open(file_name, "w") # create or overwrite file
    # Assemble the struct dimensions from the number of files, then the expected [x][y] from the instrument type
    c_str = ""
    c_str += '#include "globaldef.h"\n'
    c_str += "#define IMAGE_X_LEN " + str(IMAGE_X_LEN) + "\n"
    c_str += "#define IMAGE_Y_LEN " + str(IMAGE_Y_LEN) + "\n"
    c_str += "#define IMAGE_COUNT " +  str(len(src_file_list)) + "\n"
    c_str += "#define INSTRUMENT_TYPE " + instrument_type + "\n"
    c_str += '\n'
    c_str += '\n'
    c_str += 'Int16u Images [IMAGE_COUNT][IMAGE_Y_LEN][IMAGE_X_LEN] =\n' # [image] [scanline] [column]
    c_str += '{\n'
    f.seek(0) # set to start of file to overwrite if file exists
    f.write(c_str) # Place this header information into the file once
    f.close()
    f = open(file_name, "a") # henceforth, append to that file
    for image_number, src_file in enumerate(src_file_list):
        # read both data and header
        data, header = fitsio.read(src_file, header=True)
        # Create and open a .h file to output the scanlines to
        output = data_to_c(data, image_number)
        # Write once per file
        f.write(output)
    # finished appending all images from all files in directory, close file
    f.write('};\n')
    f.close()

# process all the fit file data into a string for writing out
def data_to_c(data, image_number):
    indent = 3
    c_str = ""
    c_str += (" " * indent) + '{\n'
    for index, item in enumerate(data, start=0): # for each scanline in that file
        for (idx,image) in enumerate(data[index < 256]):
            c_str += '// Now starting scanline %d of image %d\n' % (index, image_number)
            c_str += (" " * indent * 2) + '{\n' # beginning of scanline 
            for (pixel, scanline) in np.ndenumerate(data[index]): #pixel is a tuple containing our index, scanline is a single data point
                if (pixel[0] is not 256):
                    # If this is not the last pixel...
                    c_str += (" " * indent * 3) + ("0x%04X,\t\t// pixel %d\n" % (np.uint16(scanline), pixel[0]))
                else:
                    # Else this is the last pixel, don't put a comma into the file after it
                    c_str += (" " * indent * 3) + ("0x%04X \t\t// pixel %d\n" % (np.uint16(scanline), pixel[0]))
            c_str += (" " * indent * 2) + '},\n' # end of scanline
    c_str += (" " * indent) + '},\n'
    # return the stringified info for writing to the outfile 
    return c_str

# ----------- Main program execution -----------

directory_name = sys.argv[1] # get name of directory containing the files
# Create list of FITS file names
fit_files_list = get_fit_files_from_dir(directory_name)
# Get stats about the instrument
instrument_type, IMAGE_X_LEN, IMAGE_Y_LEN  = get_instrument_type(fit_files_list[0])
# send list of filenames in for processing
create_c_header_from_fits_files(fit_files_list, directory_name, IMAGE_X_LEN, IMAGE_Y_LEN, instrument_type) 

# -----------    END PROGRAM    ---------------