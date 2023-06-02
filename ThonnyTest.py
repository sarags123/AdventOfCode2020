from io import BufferedReader
import os
from bitstring import BitArray
#################### Read CCSDS Packet Header ###########################
##Assumptions and Conditions: Starts at the beginning of the packet 
##
## Input: 
##      
##      AppId: number which will identify packet
##      File: the file that is being read 
##
## Returns: 
##
##      A 6 byte array with the first 6 bytes of the CCSDS Space packet (the primary header)
##
###########################################################################

def readCCSDSHeader ( AppID1: bytearray, inFile: BufferedReader):
    packetHeaderRest = bytearray(f.read(4))
    packetHeaderFull = AppID1 + packetHeaderRest
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
##      Packet Data Length: Number of bytes of packet data (including secondary header) minus one.
##                          A value of 0 indicates 1 byte of data.
##                          (16 bits)
##
###########################################################################

def parseCCSDSHeader(headerParse: bytearray):
    bitHeader = BitArray( headerParse ) #turn 6 byte header into a bit array
    bitVersion = bitHeader[0:3] #version field to bitarray
    intVersion = bitVersion.uint #turning bitarray into integer 

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
##      SCLCK Start Time:
##
##      SCLCK End Time:
##
## Returns: 
##
##      A file f with all the packets within the given time range (only true for prototype)
##
###########################################################################

def openPacketStream(APPId : int, SCLCKStart : int, SCLCKEnd : int):
    #input takes in the AppId and a time range (found from the secondary header)
    #returns all the packets within that time range
    return (f, APPId, SCLCKStart, SCLCKEnd)

#################### Read CCSDS Secondary Header ###########################
##Assumptions and Conditions: The primary header has already been read and the secondary header exists
##
## Input: 
##      
##      The primary header byte array which is the first 6 bytes of a packet
##
## Returns: 
##
##      The 6 bytes following the CCSDS Packet primary header 
##
###########################################################################

def readCCSDSSecondary(file, primaryHeader: bytearray):
    secondaryHeader = bytearray(f.read(6))
    
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
    bitSCLKSeconds = bitSecondary[48:80] #SCLCK Seconds field to bitarray
    intSCLKSeconds = bitSCLKSeconds.uint #turning bitarray into integer 

    bitSCLKSubSeconds = bitHeader[80:88] #SCLCK Subseconds field to bitarray
    intSCLKSubSeconds = bitSCLKSubSeconds.uint 

    bitReserved = bitHeader[88:96] #reserved field to bitarray
    intReserved = bitReserved.uint 

    return (intSCLKSeconds, intSCLKSubSeconds, intReserved)

#################### Read CCSDS Packet Data ###########################
##Assumptions and Conditions: Packet Length is already known from primary header,
##                            primary and secondary header have been read, start from 96 biy
##
## Input: 
##      
##      packet length from end of primary header
##      packet
##
## Returns: 
##
##      Data: all packet data following the 96 bit until the end of the (packet length + 1)
##
###########################################################################

def readData(packetLength: int , file):
        
    
    
    return data

#################### Read CCSDS Packet ###########################
##Assumptions and Conditions: primary header, secondary header, and packet data already read
##
## Input: 
##      
##      primary header, secondary header, data
##
## Returns: 
##
##      tuple with primary header, secondary header, data
##
###########################################################################
def readPacket(primaryHeader, secondaryHeader, data):
    packetData = (primaryHeader, secondaryHeader, data)
    return packetData

with open("0x54e.bin", "rb") as f: #opening file as f
    byte = bytearray(f.read(1)) #reads one byte from file
    while ( byte ): #checks to make sure not the end of the file

        header = readCCSDSHeader( byte, f) #reads the header
        (version, Type, secondaryHeader, API, grouping, count,  length) = parseCCSDSHeader( header )
        sortedHeader = (version, Type, secondaryHeader, API, grouping, count,  length)  
        packetData = bytearray(f.read(length))   #read the data into variable
        print(sortedHeader)
        
        if(sortedHeader[2] == 1):
            secondaryHeader = readCCSDSSecondary(f, sortedHeader)
            (seconds, subSecs, reserved) = parseCCSDSSecondary(secondaryHeader)
            sortedSecondary = (seconds, subSecs, reserved)
            print( sortedSecondary)
        
        byte = bytearray(f.read(1))  #resets the byte to check condition again for following bytes
        

