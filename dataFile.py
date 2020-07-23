from typing import List
import urllib3
import numpy as np
import pandas as pd


class dataFile():   
    """
    This is the class for the basic data file containing all the information taking from the GLCFS database

    You pass the URL of the file that you want and it will download it and give it to you as a series of pandas dataframes, one for each timestep, as well as the plaintext
    """

    def __init__(self, fileUrl: str):
        """
        This function creates your data file object and requires the URL where the file is hosted

        Args:
            fileUrl (string): [The URL of the file hosting in string format]
        """
        self.fileUrl = fileUrl
        self._parseData()

    def _parseData(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.fileUrl)
        self.dataRaw = r.data.decode("utf-8")
        self._generateDataFrames()
        
    def _generateDataFrames(self):
        rows = self.dataRaw.split("\n")
        currentRow = 0
        titles = []
        data = []
        while(True):
            if(currentRow) >= len(rows) or rows[currentRow] == "":
                break

            splitRow = rows[currentRow].split()
            titles.append(f"{splitRow[0]}-{splitRow[1]}-{splitRow[2]}")

            rowsToParse = int(rows[currentRow].split()[-1])
            frame = pd.DataFrame(
                [x.split() for x in rows[currentRow + 1: currentRow + 1 + rowsToParse]])
            frame.set_index(0, inplace=True)
            data.append(frame)

            currentRow += rowsToParse + 1
        self.dataFrames = pd.Series(data, titles)

    

    def setDataframesTitle(self, titles: List[str], index:str=None):
        """Allows you to change the titles of all the dataframes
        This is useful if you will be working with the dataframes and would like them to be organized

        Args:
            titles (List[str]): A list of title that you want to use
            index (str, optional): An optional title to change the index title. Defaults to None.
        """

        if(len(titles) != len(self.dataFrames[0].columns)):
            return
        
        titlesDict = {}
        for title, column in zip(titles, self.dataFrames[0].columns):
            titlesDict[column] = title

        if index == None:
            for dataFrame in self.dataFrames:
                dataFrame.rename(columns=titlesDict, inplace=True)
        else:
            self.dataFrames[0].index.name = "hello there"
            for dataFrame in self.dataFrames:
                dataFrame.index.name = index
                dataFrame.rename(columns=titlesDict, inplace=True)
                pass
        print(self.dataFrames[0][:10])
        


if __name__ == "__main__":
    f = dataFile("https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/FCAST/s202020512.0.wav")
    f.setDataframesTitle(["Waves", "Angle", "frequency"], 4)
    

