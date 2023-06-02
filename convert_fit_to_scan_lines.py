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
        print(file)      
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
        sys.exit()
    return instrument_type, IMAGE_X_LEN, IMAGE_Y_LEN     

##############################################################################################################
## Read Images from FITS files, Write out Image Data CCSDS Packets
##############################################################################################################
def create_c_header_from_fits_files(src_file_list, directory_name, IMAGE_X_LEN, IMAGE_Y_LEN, instrument_type):


    file_name = directory_name + ".h"

    f = open(file_name, "wb") # create or overwrite file

    for image_number, src_file in enumerate(src_file_list):

        # read both data and header
        data, header = fitsio.read(src_file, header=True)

        # Create and open a .h file to output the scanlines to
        ccsdsData = data_to_c(data, image_number, f)

        # Write once per file
        #f.write(output)
        # print( ccsdsPrimaryHeader, ccsdsSecondaryHeader, ccsdsData)

        # exit()
    # finished appending all images from all files in directory, close file
    # f.write('};\n')
    # f.close()

###############################################################################################
## Format FITS file image data into CCSDS packets - one for each scan line
##
## "data" is the full data set from one FITS file.
## "image_number" is the count (zero based) of FITS files.
## 
## returns 
###############################################################################################
def data_to_c(data, image_number, f):
 

    # # Construct the primary header. 
    # ccsdsPrimaryHeader = [ccsdsVersion 0:3, ccsdsType 3:4, ccsdsSecHeader 4:5, ccsdsAppId 5:16, ccsdsGroup 16:18, ccsdsSequence 18:32, ccsdsLength 32:48 ]
    # Grouping indicator is set to 1st.
    ccsdsPrimaryHeader = BitArray('0b000011010100111001000000000000000000001000001001')

    # # Construct the secondary header.
    # ccsdsSecondaryHeader = [ ccsdsSecHdrMET, ccsdsSecHdrSciMET ]
    ccsdsSecondaryHeader = BitArray( '0x0000000100000001' )

    # # Construct the first packet, sans data
    # ccsdsPacket = [ ccsdsPrimaryHeader, ccsdsSecondaryHeader ]


 
    ###### For each scanline in the FITS file - assuming LORRI and 257 pixels per scan line (256 data, one dark)

    ###### For scan line in the FITS file put the data into a CCSDS packet. A LORRI binned image has 256 scan lines. LORROI scan 
    # lines are 257 pixels, 256 data and one dark column pixel. So we move through the data in 257 pixel increments. The
    # first and second for loop counts scan lines - "index" varies from 0 to 255 in the innermost "pixel" loop. The innermost
    # (third) four loop counts pixels - "pixel" varies from 0 to 257. The "scanline" variable has the value of the pixel. 
        #### 
    for index, item in enumerate(data, start=0):

        # print( "index =", index )

        # Set the grouping flags correctly for the current scan line. The scanline is indicated by the value of "index".
        if (index == 0):

            ccsdsPrimaryHeader[16:18] = ccsdsGrpFirst

        elif (index != 255):

            ccsdsPrimaryHeader[16:18] = ccsdsGrpContinue

        elif(index == 255):

            ccsdsPrimaryHeader[16:18] = ccsdsGrpEnd

        else:

            print("ERROR - Illegal value of index", index)
            exit()
        
        
        # Start a list for the next scan line's image data
        ImageScanline = []
        ImageBits = BitArray()
        ImagePacket = BitArray()

        #### For each scan line in the FITS file put the data into a CCSDS packet.
        #### LORROI scan lines are 257 pixels, 256 data and one dark column pixel. So we move through the data in 257 pixel increments.
        #### 

        for (idx,image) in enumerate( data[index < 256]):
          
            for (pixel, scanline) in np.ndenumerate(data[index]): #pixel is a tuple containing our index, scanline is a single data point

                ImageScanline.append(np.uint16(scanline))

                hexstr = "{0:04X}".format(np.uint16(scanline))
                pix = BitArray(hex=hexstr)
                ImageBits.append(pix)

            print( ImageScanline )
            exit()

            # Finalize the CCSDS Scan Line Packet

            # Set the length Secendary Header = 8, Data = (257 * 2), Minus one for zero based CCSDS length convention
            # ccsdsPrimaryHeader[33:49] = 8 + (257 * 2) - 1

            # Up the sequence count 
            sequence = ccsdsPrimaryHeader[18:32].uint
            sequence += 1 
            ccsdsPrimaryHeader[18:32] = sequence

            # print(ccsdsPrimaryHeader)
            # print(ImageBits)

            ImagePacket.append(ccsdsPrimaryHeader)
            ImagePacket.append(ccsdsSecondaryHeader)
            ImagePacket.append(ImageBits)

            # print(ImagePacket)

            # ImagePacket.tofile( f )

        
            #f.write(OutPacket)

    return

#################################################################################################
# ----------- Main program execution -----------
#################################################################################################

ccsdsGrpFirst = 1
ccsdsGrpContinue = 0
ccsdsGrpEnd = 3
ccsdsGrpNone = 4

ccsdsVersion = 0
ccsdsType = 0
ccsdsSecHeader = 1
ccsdsAppId = 1358
ccsdsGroup = ccsdsGrpFirst # First Packet
ccsdsSequence = 0
ccsdsLength = 0

ccsdsSecHdrMET = 0
ccsdsSecHdrSciMET = 0

pkt_hdr_version = 0
pkt_hdr_version_len = 3

pkt_hdr_type    = 1
pkt_hdr_type_len = 1

pkt_hdr_shdr    = 2
pkt_hdr_shdr_len = 1

pkt_hdr_apid    = 3
pkt_hdr_apid_len = 11

pkt_hdr_grp     = 4
pkt_hdr_grp_len = 2

pkt_hdr_count   = 5
pkt_hdr_count_len = 14

pkt_hdr_length  = 6
pkt_hdr_length_len = 16

pkt_primary_hdr = 0
pkt_secondary_hdr = 1
pkt_data = 2


directory_name = sys.argv[1] # get name of directory containing the files
# Create list of FITS file names
fit_files_list = get_fit_files_from_dir(directory_name)
# Get stats about the instrument
instrument_type, IMAGE_X_LEN, IMAGE_Y_LEN  = get_instrument_type(fit_files_list[0])
# send list of filenames in for processing
create_c_header_from_fits_files(fit_files_list, directory_name, IMAGE_X_LEN, IMAGE_Y_LEN, instrument_type) 

# -----------    END PROGRAM    ---------------