satellite_list = []
tags = {}

# class blob_class:
#     def __init__(self, blob, blob_store, metadata, tags, blob_id):
# 
#         self._metadata = metadata
#         self._tags = {}
#         self._blobstore = blobstore
#         self._blob_id = blob_id
# 
#     #can create multiple getters and setters inside the blob class and use the class to create our own
#     #functions that can be used while creating the blob and trying to upload data to it and retrieve data
#     # Getter for file 
def get_blob(blob_id): #return the string test
    return "this is blob " + str(blob_id)
def get_metadata(blob_id):
    return "meta"
def get_tags(blob_id): #blob_id, key, value
    return (key, value, blob_id)
#setter for file
def put_blob(blob_id, data): #return the string test
    blobs[blob_id] = data

def set_metadata(blob_id, metadata):
    return metadata


def set_tags(blob_id, key, value): #blob_id, key and value for input and put into lookup table
    global tags
    blob_id_list = find_blobs((key, value))
    blob_id_list.append(blob_id)
    tags[(key, value)] = blob_id_list
    
    
    
    

def find_blobs(key): 
    global tags
    
    if key in tags :
        blob_id_list = tags[key]
    else:
        blob_id_list = []
    
    return blob_id_list #return blob id
    
#hash table/function research    
    
    
#radio class
# class radio_class:
#     def __init__(self, rx_file, tx_file, sat_file): 
#         self._rx_file = rx_file
#         self._tx_file = tx_file
#         self._sat_file = sat_file
#         self._satellite_id = sat_file.read(1)
#         
#         #self._satellite_id = first satellite id in file
#         

class Satellite:


    def __init__( self ):
        self.satellite_list = []
        self.receiver = (103,101,102,103,104,105)
 
        #read satellite id from sat file
        #update internal satellite id
        self.satellite_file = open("satellite_id.txt", "r")

        self.satellite_line = self.satellite_file.readlines()
        
        self.satellite_list = self.satellite_line[0].split(" ")
    

    def get_satellite_id(self, sequence):
        self.satellite_list
        #read satellite id from sat file
        #update internal satellite id

        
        return self.satellite_list[sequence]

    def radio_read(self, sequence):
        # Read data from satellite and return sel
        # receive
        # rx_file to get data from the satellite and return data
        #instead of opening the file name use self.rx_file
        data = "test"
        return (data, self.receiver[sequence])

    def radio_send(self, receiver, data):
        # Write data to satellite
        # Return True if successful, False otherwise
        #use tx_file instead to return new data to satellite
        #instead use the tx_file self.tx_file
    #     tx_file.write(data)
    #     tx_file.close()
        print(" radio sent ",  data , " to " , receiver)
    #     success = True
    #     return success

#MAIN
# cog_router = blob_class("blob store", "metadata", "tags") #create cognitive router in the blob class
# radio = radio_class("rx.bin", "tx.bin", "sat.bin")
#tags = {}
blobs = {}
sat_id = 0
receiver = 30
blob_id = 4212023
send_blob_id = 0

satellites = Satellite()

for i in range(0, 5):
    

    sat_id = int(satellites.get_satellite_id(i))
#    print(sat_id)
    (data, receiver) = satellites.radio_read(i)
    set_tags(blob_id, "from", sat_id)
    set_tags(blob_id, "to", receiver)
    put_blob(blob_id, data)
    
    if ("to", sat_id) in tags :
        send_blob_id_list = find_blobs(("to", sat_id))
        if send_blob_id_list[0]:
#           print(send_blob_id_list)
           satellites.radio_send(sat_id, get_blob(send_blob_id_list))

#     print(tags)
#     print(blobs)
    blob_id = blob_id + 1
