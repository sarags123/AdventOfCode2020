##description of whole program


from io import BufferedReader
import os
from bitstring import BitArray
#################### Read CCSDS Packet Header ###########################
##Assumptions and Conditions: Stream is positioned at the beginning of the packet 
##
## Input: 
##      
##      AppId: number which will identify packet
##      PacketStream: the packet stream that is being read 
##
## Returns: 
##
##      A 6 byte array with the first 6 bytes of the CCSDS Space packet (the primary header)
##
###########################################################################

def readCCSDSHeader ( AppID1: int, packetStream):
    f = packetStream[0]
    try:
        packetHeaderFull = bytearray(f.read(6))
    except:
        print("end of file")
    return( packetHeaderFull )

#################### Parse CCSDS Packet Header ###########################
##Assumptions and Conditions: The byte array has already been read
##
## Input: 
##
##      header: A byte array containing the first 6 bytes of a CCSDS 
##      Space Packet which is the packet header.
##
## Returns: (intVersion, intType, intSecondaryHeader, intAppId, intGrouping, intCount, intLength)
##
##      Version Number: The version number value is always 0b000. (3 bits)
##
##      Type Indicator: 0b1, indicating telemetry. (1 bit)
##
##      Secondary Header Flag: Always (0b1), secondary header is present. (1 bit)
##
##      AppId: Application Identifier. Indicates the nature and structure of the data. (11 bits)
##      (returned as an integer)
##
##      Grouping Flags: 0 –  0b00 - intermediate packet
##                      1 –  0b01 - first packet in group
##                      2 –  0b10 - last packet in group
##                      3 –  0b11 - not part of group (2 bits)
##
##      Sequence Count: Increments modulo 16,384 within a particular AppId. Indicates dropped packets.
##                      (14 bits)
##
##      Packet Data Length: Number of bytes of packet data (including secondary header).
##                          
##                          (16 bits)
##
###########################################################################

def parseCCSDSHeader(headerParse: bytearray):
    bitHeader = BitArray( headerParse ) #turn 6 byte header into a bit array
    try:
        bitVersion = bitHeader[0:3] #version field to bitarray
        intVersion = bitVersion.uint #turning bitarray into integer 
    except:
        return print("end of file")
         
    bitType = bitHeader[3:4] #Type indicator field to bitarray
    intType = bitType.uint 

    bitSecondaryHeader = bitHeader[4:5] #packet secondary header field to bitarray
    intSecondaryHeader = bitSecondaryHeader.uint 

    bitAPI = bitHeader[5:16] #Application Process Identifier field to bitarray
    intAPI = bitAPI.uint 

    bitGrouping = bitHeader[16:18] #Grouping Flags field to bitarray
    intGrouping = bitGrouping.uint

    bitCount = bitHeader[18:32] #Source Sequence Count field to bitarray
    intCount = bitCount.uint

#length of packet is packet length - 1 but add 1 for user convienence
    bitLength = bitHeader[32:48] #Packet Data Length field to bitarray
    intLength = bitLength.uint
    intLength = intLength + 1 #real length of packet is one more

    return(intVersion, intType, intSecondaryHeader, intAPI, intGrouping, intCount, intLength) #read the full oacket header with sections into tuple

#################### Open Packet Stream ###########################
##Assumptions and Conditions: AppID and time range of desired packet stream is known
##
## Input: 
##      
##      AppId: number which will identify packet
##
##      Priority: downlink priority assigned to the data used to locate data in the file system
##
##      SCLCK Start Time:
##
##      SCLCK End Time:
##
## Returns: 
##
##      A file f with all the packets within the given time range (only true for prototype)
##
###########################################################################

def openPacketStream(APPId : int, priority, SCLCKStart : int, SCLCKEnd : int):
    #input takes in the AppId and a time range (found from the secondary header)
    #returns all the packets within that time range
    f = open("test.bin", "rb")
    return (f, APPId, priority, SCLCKStart, SCLCKEnd)

#################### Read CCSDS Secondary Header ###########################
##Assumptions and Conditions: The primary header has already been read and the secondary header exists and packet stream positioned at secondary header
##
## Input: 
##      
##      The ppacket stream and AppID for packet
##
## Returns: 
##
##      The 6 bytes following the CCSDS Packet primary header 
##
###########################################################################

def readCCSDSSecondary(packetStream):
    f = packetStream[0]
    secondaryHeader = bytearray(f.read(8)) #reads the next six bytes
    
    return secondaryHeader

#################### Parse CCSDS Secondary Header ###########################
##Assumptions and Conditions: The Secondary Header has already been read
##
## Input: 
##      
##      The second 6 bytes of the CCSDS Packet Header called the secondary header and the packet
##
## Returns: 
##
##      SCLK Seconds: Packet creation time in synchronized SCLK seconds. (32 bits)
##
##      SCLK SubSeconds: Packet creation time in synchronized SCLK subseconds (1/256) (8 bits)
##      
##      Reserved: Reserved, Value is 0x00. (8 bits)
##
###########################################################################

def parseCCSDSSecondary(secondaryHeader: bytearray):
    #input takes in a byte array containing the second 6 bytes of the
    #returns the (SCLK Seconds, SCLK SubSeconds, and Reserved) in a tuple format
    #SCLK Seconds- [48:80]
    #SCLK Sub Seconds- [80:88]
    #Reserved- [88:96]
    
    bitSecondary = BitArray( secondaryHeader ) #turn 6 byte header into a bit array
    bitSCLKSeconds = bitSecondary[0:32] #SCLCK Seconds field to bitarray
    intSCLKSeconds = bitSCLKSeconds.uint #turning bitarray into integer 

    bitSCLKSciSeconds = bitSecondary[32:64] #SCLCK Subseconds field to bitarray
    intSCLKSciSeconds = bitSCLKSciSeconds.uint 

   
    return (intSCLKSeconds, intSCLKSciSeconds )
#################### Read CCSDS Packet Data ###########################
##Assumptions and Conditions: Packet Length is already known from primary header,
##                            primary and secondary header have been read, packet stream positioned at beginning of data
##
## Input: 
##      packetstream
##      packet length from end of primary header
##      
##
## Returns: 
##
##      Data: all packet data following the 96 bit until the end of the (packet length + 1)
##
###########################################################################

def readData(packetStream, packetLength: int):
    f = packetStream[0]
    bitDataSection = bytearray(f.read(packetLength)) #QUESTION FOR MEETING: not sure how many bytes I should be reading to read data section is it just the packetLength?
    
    bitData = bitDataSection[0:packetLength + 1] #data field to bitarray
    
    return bitData

#################### Read CCSDS Packet ###########################
##Assumptions and Conditions: primary header, secondary header, and packet data already read
##
## Input: 
##      
##      packet stream tuple with (packet, APPId, priority, SCLCKStart, SCLCKEnd)
##
## Returns: 
##
##      tuple with primary header, secondary header, data
##
###########################################################################
def readPacket(packetStreamTuple):
    packetData = (primaryHeader, secondaryHeader, data)
    return packetData

#################### Publish CCSDS Packet ###########################
##Assumptions and Conditions: packet has been read and is ready to be published to software bus
##
## Input: 
##      
##      packet
##
## Returns: 
##      status
##      
##Side Effects:
##      packet is placed on the software bus (in version 0.0 printed to console)
##
###########################################################################
def publishPacket(packet, printFile):
#    binPacket = convertTupleToString(packet)
    for item in packet:
        printFile.write(bytes(item.__str__(),'utf8'))
#        print(item)
    return

#def convertTupleToString(tup):
        # initialize an empty string
#    s1 = []
#    i =0
#    for item in tup:
#        s1[i] = bin(item)
#        i=i+1
#    return s1
#def convertTupleToBinary(tup):
#    for item in tup:
#        item = item + bin(item)
#        binaryData = binaryData + item
#    return binaryData
# def convertInttoBin(version, Type, secondaryHeader, API, grouping, count,  length):
#     binVersion = bin(version)
#     binType = bin(Type)
#     binsecondaryHeader = bin(secondaryHeader)
#     binAPI = bin(API)
#     binGrouping = bin(grouping)
#     binCount = bin(count)
#     binLength = bin(length)
#     
#     return(binVersion, binType, binsecondaryHeader, binAPI, binGrouping, binCount, binLength)

##MAIN
printFile = open('printFile.bin', 'wb')
#printFile = open('printFile.txt', 'w')
pkt_hdr_version = 0
pkt_hdr_type    = 1
pkt_hdr_shdr    = 2
pkt_hdr_apid    = 3
pkt_hdr_grp     = 4
pkt_hdr_count   = 5
pkt_hdr_length  = 6

scanline = [0]*257
final_image = [scanline]*256

#call open packet stream instead
packetStream = openPacketStream(0,0,0,0)
# f = packetStream[0]
# print(f)

# byte = bytearray(f.read(1)) #reads one byte from file
# while ( byte ): #checks to make sure not the end of the file

# header = readCCSDSHeader( 1358, packetStream) #reads the header
# (version, Type, secondaryHeader, API, grouping, count,  length) = parseCCSDSHeader( header )
# sortedHeader = (version, Type, secondaryHeader, API, grouping, count,  length)  
#packetData = bytearray(f.read(length))   #read the data into variable
#print(sortedHeader)

#print( sortedHeader[pkt_hdr_version], sortedHeader[pkt_hdr_type], sortedHeader[pkt_hdr_shdr], sortedHeader[pkt_hdr_apid], sortedHeader[pkt_hdr_grp], sortedHeader[pkt_hdr_count], sortedHeader[pkt_hdr_length] )

# secondaryHeader = readCCSDSSecondary(packetStream)
# (packetSecs, SciSecs) = parseCCSDSSecondary(secondaryHeader)
# sortedSecondary = (packetSecs, SciSecs)
#print( sortedSecondary)

# length = sortedHeader[pkt_hdr_length]
# sortedData = readData(packetStream, length - 8)
#print(sortedData)

f = packetStream[0]

temp = []
scanline = []
packet_counter = 0

scanline = [0] * 257
final_image = [ [0] * 257 ] * 256
image = [ [0] * 257 ] * 256

for iCount in range(10):

    image = []

    for sl in range(256):
        header = readCCSDSHeader( 1358, packetStream) #reads the header
        try:
            (version, Type, secondaryHeader, API, grouping, count,  length) = parseCCSDSHeader( header )
        except:
            printFile.close()
            print("end of file")
            break
                  
        sortedHeader = (version, Type, secondaryHeader, API, grouping, count,  length)
    #    sortedHeader = convertInttoBin(version, Type, secondaryHeader, API, grouping, count,  length)
    #    print(sortedHeader)
        
    #    try:
    ##    publishPacket(sortedHeader, printFile)
    #    printFile.write(sortedHeader)
    #    except:
    #        print("file problem")
        
        secondaryHeader = readCCSDSSecondary(packetStream)
        (packetSecs, SciSecs) = parseCCSDSSecondary(secondaryHeader)
        sortedSecondary = (packetSecs, SciSecs)
    #    print( sortedSecondary)

        length = sortedHeader[pkt_hdr_length]
        sortedData = readData(packetStream, length - 8)
    #    print(sortedData)


    #     
    #     byte = bytearray(f.read(1))  #resets the byte to check condition again for following bytes  
        # sortedData now contains the data from one CCSDS packet. This
        # is the data for one scanline of the image. sortedData is a 
        # byte string - 8 bit integers - while the image data is 16 bit 
        # integers. This section combines every two bytes into one 16 bit
        # integer.

        # item will be used for the next byte to be used. temp will be used
        # for two bytes that are to be combined. 
        # 
        # We use the mod "% 2" function to determine when we have two bytes
        # to combine. Because the mod function gives the sequence 0, 1, 0, 1, 
        # and we are looking for 0 when we have 2 bytes, we add one so the 
        # sequence is 1, 0, 1, 0...
        #
        # Once we have two bytes, the two are combined to make one 16 bit
        # value. We do this by "bit shifting" the first byte and then adding
        # in the second byte. To "bit shift" the first byte, we multiply
        # by 256. 256 is 2^8, so this shifts the byte by 8 bits, making it
        # the "high byte" of the 16 bit value.
        #
        # Each time we get a new 16 bit value we put it into the "scanline" list
        # until we have the complete scan line from this packet.


        # First, zero out temp and scanline
        temp = []
        scanline = []

        # Move through the sortedData, one byte at a time. index will be
        # the position of the byte in the sortedData, while item will be
        # the byte itself.
        for index, item in enumerate( sortedData):

            # We will use "counter" rather than index in the mod function.
            # This is to group the first two bytes together, the next two, 
            # etc. Without doing this, the grouping would be off on the first
            # byte and stays off afterwards.
            counter = index + 1

            # Decide if we have two bytes grouped into temp:
            if counter % 2 != 0:

                # We do not yet have two bytes - put this byte into the 
                # temp list.
                temp.append(item)

            else:

                # We now have two bytes. Put this one into the list, then
                # turn the two 8 bit bytes into one 16 bit value. We do
                # this at the same time we append the value to scanline.
                temp.append(item)
                scanline.append( (temp[0] * 256) + temp[1] )
                temp = []

        image.append(scanline)
    #add image to final image

    for i in range(len(final_image)):
        final_image[i] = [pi + pf for pi, pf in zip( final_image[i], image[i])]

    ###### END FOR image count 0 to 9

for i in range(256):
    for j in range(256):
        element = (i, j, (final_image[i][j] / 10))
        print( element )



