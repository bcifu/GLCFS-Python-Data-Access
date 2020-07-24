from enum import Enum
import pickle
import pandas as pd
import urllib3
import os
import io
import math

#Note, the I, J for square columns are 1-indexed

class Lake(Enum):
    """An Enum for each lake's file location

    Args:
        Enum (The lake): The lake for this enum and then the file name for that pickled map data
    """
    MICHIGAN = "maps/michigan.pickle"
    HURON = "maps/huron.pickle"
    ERIE = "maps/erie.pickle"
    ONTARIO = "maps/ontario.pickle"
    SUPERIOR = "maps/superior.pickle"

class MapData():
    """
    A class that handles the lake Michigan map to conver coordinates to the i, j coordinate plane used in some files, and the indexing for regions used in others.
    """
    def __init__(self, lake: Lake):
        '''Creates a MapData object to do coordinate work with, loading the pickle file.

        Args:
            lake (Lake): Lake enum of which lake this object is
        '''
        self.data = pickle.load(open(lake.value, "rb"))

    #There is probably a more efficient way to do this method, I just have yet to work it out, probably use group by but we will go with the slow for now      
    def decodeCoords(self, lat, lon):
        '''Using the data frame for this object, uses the latitude and longitude to decode the square sequence number, column and row to be used in other classes.     

        Returns the series for the correct row in the data table

        Lat and lon are forced to positive because that is how the data is stored :/ 

        Args:
            self ([type]): [description]
            int ([type]): [description]
            int ([type]): [description]
        '''
        lat = abs(lat)
        lon = abs(lon)

        dist = math.inf
        seq = 1

        for row in self.data.iterrows():
            val = ((row[1]['Lat'] - lat) ** 2) + ((row[1]['Lon'] - lon) ** 2) #These numbers may look off if you are looking at a map to try to match them up, that is because this numbering is using FORTRAN numbering which is 1 indexed            
            if val < dist:
                dist = val
                seq = row[0]
        return(self.data.loc[seq])
            
    @staticmethod
    def RowToSequenceNum(r: pd.Series):
        '''Extract the sequence number from a row returned from decoding coordinates

        Args:
            r (pd.Series): The series from the table to extract the row from

        Returns:
            [int]: The sequence number, can be used in other things
        '''
        return r.name

    @staticmethod
    def RowToIJ(r: pd.Series) -> tuple:
        '''Extract the col and row numbers from a row returned from decoding coordinates

        Args:
            r (pd.Series): The series from the table to extract the row and cols from

        Returns:
            [tuple]: A two value tuple with the column (I) in the first spot and the row (J) in the second, fortran 1-indexed numbering
        '''
        return (r["Col"], r["Row"])

    @staticmethod
    def CreateAllMaps():
        '''Builds map pickle files for all 5 great lakes
        '''
        #using _all is recommended because then it includes some of the edge case shore tiles, but may not work so double check if you want.
        MapData.CreateMapTable(
            Lake.MICHIGAN, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/michigan2km_all.map")
        MapData.CreateMapTable(
            Lake.ERIE, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/erie2km_all.map")
        MapData.CreateMapTable(
            Lake.HURON, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/huron2km_all.map")
        MapData.CreateMapTable(
            Lake.SUPERIOR, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/superior10km_all.map")
        MapData.CreateMapTable(
            Lake.ONTARIO, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/ontario5km_all.map")

    @staticmethod
    def CreateMapTable(lake: Lake, source: str):
        '''A static method to create a new datatable for a lake and save it to that lakes location.
        This method should only be used when a map needs to be updated or changed, probably never.

        Args:
            lake (Lake): The lake to update, and this includes the file name
            source (str): The URL where to get the data from
        '''
        data = urllib3.PoolManager().request('GET', source).data.decode("utf-8") #create the request manager, execute the request, then decode it from binary to utf-8
        #data = re.sub(r'[^\S\r\n]+', " ", data)
        table = pd.read_csv(io.StringIO(data), delim_whitespace=True, header=None, index_col=0, names=['Seq', 'Col', 'Row', 'Lat', 'Lon', 'Depth'])
        #print(lake.value)
        if not os.path.isdir("maps"):
            os.makedirs("maps")
        pickle.dump(table, open(lake.value, "wb"))
        

if __name__ == "__main__":
    # MapData.CreateAllMaps()
    mi = MapData(Lake.MICHIGAN)
    print(MapData.RowToSequenceNum(mi.decodeCoords(41.790308, -87.572686)))

    # print(mi.data.head(500))
    # ontario = MapData(Lake.ONTARIO)
    # ontario.decodeCoords(43.468444, 79.056817)
    
    
