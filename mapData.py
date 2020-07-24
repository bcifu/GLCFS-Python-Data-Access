from enum import Enum
import pickle
import pandas as pd
import urllib3
import os
import io

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
    @staticmethod
    def CreateAllMaps():
        '''Builds map pickle files for all 5 great lakes
        '''
        MapData.CreateMapTable(
            Lake.MICHIGAN, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/michigan2km.map")
        MapData.CreateMapTable(
            Lake.ERIE, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/erie2km.map")
        MapData.CreateMapTable(
            Lake.HURON, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/huron2km.map")
        MapData.CreateMapTable(
            Lake.SUPERIOR, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/superior10km.map")
        MapData.CreateMapTable(
            Lake.ONTARIO, "https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/map_files/ontario5km.map")

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
        table = pd.read_csv(io.StringIO(data), delim_whitespace=True, header=None, index_col=0, names=['Sequence Num', 'Col', 'Row', 'Lat', 'Lon', 'Depth'])
        #print(lake.value)
        if not os.path.isdir("maps"):
            os.makedirs("maps")
        pickle.dump(table, open(lake.value, "wb"))
        

if __name__ == "__main__":
    MapData.CreateAllMaps()
    
    
